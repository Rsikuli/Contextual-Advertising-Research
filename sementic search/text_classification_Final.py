import pandas as pd
from transformers import pipeline
import os

# Load a multi-class classification pipeline
classifier = pipeline("text-classification", model="classla/multilingual-IPTC-news-topic-classifier", device=0, max_length=512, truncation=True)

# Define file paths
ocr_results_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/OCR_results.csv'
blip_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/Blip_results.csv'
sam_vit_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/SAM&Vit_results.csv'
fusion_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/fused_results.csv'
article_subjects_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

# Output paths
article_classifications_path = '/Users/ramisafi/Desktop/Classification Matching/article_classifications.csv'
publicity_classifications_path = '/Users/ramisafi/Desktop/Classification Matching/publicity_classifications.csv'
best_matches_path = '/Users/ramisafi/Desktop/Classification Matching/matched_results.csv'

# Check if the files exist
for path in [ocr_results_path, blip_path, sam_vit_path, fusion_path, article_subjects_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

# Read the CSV files for publicity representations
ocr_results_df = pd.read_csv(ocr_results_path)
sam_vit_df = pd.read_csv(sam_vit_path)
blip_df = pd.read_csv(blip_path)
fusion_df = pd.read_csv(fusion_path)

# Read the CSV file for article subjects
article_subjects_df = pd.read_csv(article_subjects_path)

# Prepare publicity representations
publicity_representations_with_titles = []
titles = ocr_results_df['Title'].tolist()
ocr_texts = ocr_results_df['Extracted Words'].tolist()
sam_vit_texts = sam_vit_df['Descriptions'].tolist()
blip_texts = blip_df['Description'].tolist()
fusion_texts = fusion_df['Fused Content'].tolist()

for i in range(len(titles)):
    publicity_representations_with_titles.append({
        "Title": titles[i],
        "OCR": ocr_texts[i] if i < len(ocr_texts) else None,
        "SAM-ViT": sam_vit_texts[i] if i < len(sam_vit_texts) else None,
        "BLIP": blip_texts[i] if i < len(blip_texts) else None,
        "Fusion": fusion_texts[i] if i < len(fusion_texts) else None
    })

article_representations = {
    "Headline": article_subjects_df['Headline'].tolist(),
    "Subheadline": article_subjects_df['Subheadline'].tolist(),
    "Caption": article_subjects_df['Caption'].tolist(),
    "Keywords": article_subjects_df['Keywords'].tolist(),
    "Summary": article_subjects_df['Summary'].tolist()
}

def classify_text(text):
    """
    Classifies the given text using a pre-defined classifier.

    Args:
        text (str): The text to be classified.

    Returns:
        The classification result from the classifier.
    """
    return classifier(text)

def get_all_classifications2(classifications):
    return list({classification['label'] for classification in classifications})

# Classify the article representations
article_classifications_per_article = []
for headline, subheadline, keywords, summary in zip(
    article_representations["Headline"],
    article_representations["Subheadline"],
    article_representations["Keywords"],
    article_representations["Summary"]
):
    if not isinstance(subheadline, str) or not isinstance(keywords, str) or not isinstance(summary, str):
        continue

    subheadline_classification_result = classify_text(subheadline)
    headline_classification_result = classify_text(headline)
    keywords_classification_result = classify_text(keywords)
    summary_classification_result = classify_text(summary)

    all_classifications = (
        subheadline_classification_result +
        headline_classification_result +
        keywords_classification_result +
        summary_classification_result
    )
    most_common_classifications = get_all_classifications2(all_classifications)

    article_classifications_per_article.append({
        "Headline": headline,
        "Subheadline": subheadline,
        "Classifications": most_common_classifications
    })

# Save article classifications to a CSV file
pd.DataFrame(article_classifications_per_article).to_csv(article_classifications_path, index=False)

# Classify the publicity representations with titles
publicity_classifications_per_title = []
for publicity in publicity_representations_with_titles:
    title = publicity["Title"]
    ocr = publicity["OCR"]
    classifications_per_title = []

    for representation_type in ["OCR", "SAM-ViT", "BLIP", "Fusion"]:
        text = publicity[representation_type]
        if not isinstance(text, str):
            continue

        classification_result = classify_text(text)
        classifications_per_title.extend(get_all_classifications2(classification_result))

    publicity_classifications_per_title.append({
        "Title": title,
        "OCR": ocr,
        "Classifications": list(set(classifications_per_title))
    })

# Save publicity classifications to a CSV file
pd.DataFrame(publicity_classifications_per_title).to_csv(publicity_classifications_path, index=False)

# Match each article to the best publicity based on IoU score
best_matches = []
for article in article_classifications_per_article:
    article_classifications = article['Classifications']
    best_publicity_title = None
    max_closer_classification = 0
    shared_classifications = set()
    total_classifications = set()

    for publicity in publicity_classifications_per_title:
        publicity_classifications = publicity['Classifications']
        intersection = set(article_classifications).intersection(publicity_classifications)
        union = set(article_classifications).union(publicity_classifications)

        # Calculate IoU
        closer_classification = len(intersection) / len(union) if union else 0

        # Update if this publicity has a higher IoU
        if closer_classification > max_closer_classification:
            max_closer_classification = closer_classification
            best_publicity_title = publicity['Title']
            best_publicity_ocr = publicity['OCR']
            shared_classifications = intersection
            total_classifications = union

    # Append the best match to results
    if best_publicity_title:
        best_matches.append({
            "Article Headline": article['Headline'],
            "Article Subheadline": article['Subheadline'],
            "Best Publicity Title": best_publicity_title,
            "OCR": best_publicity_ocr,
            "IoU Score": max_closer_classification,
            "Shared Classifications": list(shared_classifications),
            "Total Classifications": list(total_classifications)
        })

# Save matched results to a CSV file
pd.DataFrame(best_matches).to_csv(best_matches_path, index=False)


# /Users/ramisafi/Downloads/Research Journal Project/sementic search/text_classification_Final.py
