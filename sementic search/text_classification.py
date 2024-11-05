import pandas as pd
from transformers import pipeline
import sys
import os
from collections import Counter

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


# Define representations for Publicity and Articles
publicity_representations = {
    "OCR": ocr_results_df['Extracted Words'].tolist(),
    "SAM-ViT": sam_vit_df['Descriptions'].tolist(),
    "BLIP": blip_df['Description'].tolist(),
    "Fusion": fusion_df['Fused Content'].tolist()
}


article_representations = {
    "Headline": article_subjects_df['Headline'].tolist(),
    "Subheadline": article_subjects_df['Subheadline'].tolist(),
    "Caption": article_subjects_df['Caption'].tolist(),
    "Keywords": article_subjects_df['Keywords'].tolist(),
    "Summary": article_subjects_df['Summary'].tolist()
}

def classify_text(text):
    return classifier(text)


def get_all_classifications(classifications):
    unique_labels = set()
    seen_labels = set()
    for classification in classifications:
        label = classification['label']
        if label not in seen_labels:
            unique_labels.add(label)
            seen_labels.add(label)
    return list(unique_labels)

def get_all_classifications2(classifications):
    return list({classification['label'] for classification in classifications})


def get_most_common_classifications(classifications):
    label_counter = Counter([classification['label'] for classification in classifications])
    most_common = label_counter.most_common()
    
    if most_common[0][1] == 3:
        return [most_common[0][0]]
    elif most_common[0][1] == 2:
        if len(most_common) > 1 and most_common[1][1] == 2:
            return [most_common[0][0], most_common[1][0]]
        else:
            highest_score_classification = max(classifications, key=lambda x: x['score'])
            if highest_score_classification['label'] == most_common[0][0]:
                return [most_common[0][0]]
            else:
                return [most_common[0][0], highest_score_classification['label']]
    else:
        return [most_common[0][0]]


# Classify the article representations and save the results to a CSV file
article_classifications = []

for headline, subheadline, keywords, summary in zip(article_representations["Headline"], article_representations["Subheadline"], article_representations["Keywords"], article_representations["Summary"]):
    if not isinstance(subheadline, str):
        print(f"Skipping non-string subheadline: {subheadline}")
        continue
    if not isinstance(keywords, str):
        print(f"Skipping non-string keywords: {keywords}")
        continue
    if not isinstance(summary, str):
        print(f"Skipping non-string summary: {summary}")
        continue

    subheadline_classification_result = classify_text(subheadline)
    headline_classification_result = classify_text(headline)
    keywords_classification_result = classify_text(keywords)
    summary_classification_result = classify_text(summary)

    all_classifications = subheadline_classification_result + headline_classification_result + keywords_classification_result + summary_classification_result

    # Get the most common classifications for the article
    most_common_classifications = get_all_classifications2(all_classifications)
    
    article_classifications.append({
        "Headline": headline,
        "Subheadline": subheadline,
        "Summary": summary,
        "Keywords": keywords,
        "Most Common Classifications": most_common_classifications
    })

# Save article classifications to a CSV file
article_classifications_df = pd.DataFrame(article_classifications)
article_classifications_df.to_csv('/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/article_classifications.csv', index=False)


# Classify the publicity representations and save the results to a CSV file
publicity_classifications = []

for representation_type, texts in publicity_representations.items():
    for text in texts:
        if not isinstance(text, str):
            print(f"Skipping non-string text in {representation_type}: {text}")
            continue

        classification_result = classify_text(text)
        publicity_classifications.append({
            "Representation Type": representation_type,
            "Text": text,
            "Most Common Classifications": get_all_classifications2(classification_result)
        })

# Save publicity classifications to a CSV file
publicity_classifications_df = pd.DataFrame(publicity_classifications)
publicity_classifications_df.to_csv('/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/publicity_classifications.csv', index=False)


# Function to match each article representation with each publicity representation and save to separate CSV files
def match_and_save(article_classifications_path, publicity_classifications_path, output_dir):
    article_classifications_df = pd.read_csv(article_classifications_path)
    publicity_classifications_df = pd.read_csv(publicity_classifications_path)

    article_columns = ["Headline", "Subheadline", "Keywords", "Summary"]
    publicity_columns = ["OCR", "SAM-ViT", "BLIP", "Fusion"]

    for article_col in article_columns:
        for publicity_col in publicity_columns:
            matching_results = []

            for _, article_row in article_classifications_df.iterrows():
                article_text = article_row[article_col]
                article_classifications = eval(article_row['Most Common Classifications'])

                matching_publicities = []

                for _, publicity_row in publicity_classifications_df.iterrows():
                    publicity_text = publicity_row['Text']
                    publicity_classifications = eval(publicity_row['Most Common Classifications'])

                    if set(article_classifications) == set(publicity_classifications):
                        matching_publicities.append(publicity_text)

                matching_results.append({
                    f"{article_col}": article_text,
                    "Matching Publicities": matching_publicities
                })

            matching_results_df = pd.DataFrame(matching_results)
            output_path = os.path.join(output_dir, f"{article_col}_vs_{publicity_col}.csv")
            matching_results_df.to_csv(output_path, index=False)


# Create output directory if it doesn't exist
output_dir = '/Users/ramisafi/Downloads/Research Journal Project/Article_Publicity_Matches'
os.makedirs(output_dir, exist_ok=True)

# Match and save the results
match_and_save(
    '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/article_classifications.csv',
    '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/publicity_classifications.csv',
    output_dir
)
