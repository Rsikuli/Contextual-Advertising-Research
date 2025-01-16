import pandas as pd
from transformers import pipeline
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load a multi-class classification pipeline - if the model runs on CPU, comment out "device"
classifier = pipeline("text-classification", model="classla/multilingual-IPTC-news-topic-classifier", device=0, max_length=512, truncation=True)

# Define file paths
ocr_results_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/OCR_results.csv'
blip_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/Blip_results.csv'
sam_vit_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/SAM&Vit_results.csv'
fusion_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/fused_results.csv'

article_subjects_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

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
        "Classifications": most_common_classifications
    })

# Classify the publicity representations with titles
publicity_classifications_per_title = []
for publicity in publicity_representations_with_titles:
    title = publicity["Title"]
    classifications_per_title = []

    for representation_type in ["OCR", "SAM-ViT", "BLIP", "Fusion"]:
        text = publicity[representation_type]
        if not isinstance(text, str):
            continue

        classification_result = classify_text(text)
        classifications_per_title.extend(get_all_classifications2(classification_result))

    publicity_classifications_per_title.append({
        "Title": title,
        "Classifications": list(set(classifications_per_title))
    })

# Match each article to the best publicity based on IoU score
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
            shared_classifications = intersection
            total_classifications = union

    # Print the best match for the article
    if best_publicity_title:
        print(f"Article: {article['Headline']}, Best Publicity: {best_publicity_title}, "
              f"IoU Score: {max_closer_classification:.2f}, "
              f"Shared: {shared_classifications}, Total: {total_classifications}")
