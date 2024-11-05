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
    """
    Determines the most common classifications from a list of classification dictionaries.
    Args:
        classifications (list of dict): A list of dictionaries where each dictionary contains
                                        'label' (str) and 'score' (float) keys.
    Returns:
        list of str: A list containing the most common classification labels. The length of the
                     list can be 1 or 2 depending on the frequency and score of the classifications.
    The function works as follows:
    - Counts the occurrences of each classification label.
    - If the most common label appears 3 times, returns a list with that label.
    - If the most common label appears 2 times:
        - If there is another label that also appears 2 times, returns both labels.
        - Otherwise, returns the most common label and the label with the highest score if they are different.
    - If the most common label appears less than 2 times, returns a list with that label.
    """
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

article_classifications_per_article = []



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

    # Get the most common classifications for the article
    classifications_per_article = list(set(most_common_classifications))
    article_classifications_per_article.append({"Headline": headline, "Classifications": most_common_classifications})









# there's a problem here, we have to reaximne the way the two are matched, it only shows classifications for {'arts, culture, entertainment and media'}














    article_classifications.append({
        "Headline": headline,
        "Subheadline": subheadline,
        "Summary": summary,
        "Keywords": keywords,
        "Most Common Classifications": most_common_classifications
    })

    # Save each representation type and its classification to a CSV file
    representation_classifications = [
        {"Representation Type": "Headline", "Text": headline, "Classifications": get_all_classifications2(headline_classification_result)},
        {"Representation Type": "Subheadline", "Text": subheadline, "Classifications": get_all_classifications2(subheadline_classification_result)},
        {"Representation Type": "Keywords", "Text": keywords, "Classifications": get_all_classifications2(keywords_classification_result)},
        {"Representation Type": "Summary", "Text": summary, "Classifications": get_all_classifications2(summary_classification_result)}
    ]

    representation_classifications_df = pd.DataFrame(representation_classifications)
    representation_classifications_df.to_csv(f'/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/representations classifications per article/{headline[:50]}_representation_classifications.csv', index=False)


# Save article classifications to a CSV file
article_classifications_df = pd.DataFrame(article_classifications)
article_classifications_df.to_csv('/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/article_classifications.csv', index=False)

# Save article classifications per article to a CSV file
article_classifications_per_article_df = pd.DataFrame(article_classifications_per_article)
article_classifications_per_article_df.to_csv('/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/Organized__article_classifications_per_article.csv', index=False)

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

publicity_classifications_per_title = []


# Classify the publicity representations with titles and save the results to separate CSV files for each title
for publicity in publicity_representations_with_titles:
    title = publicity["Title"]
    classifications = []
    classifications_per_title = []

    for representation_type in ["OCR", "SAM-ViT", "BLIP", "Fusion"]:
        text = publicity[representation_type]
        if not isinstance(text, str):
            print(f"Skipping non-string text in {representation_type} for title {title}: {text}")
            continue

        classification_result = classify_text(text)

        classifications_per_title.extend(get_all_classifications2(classification_result))
        classifications_per_title = list(set(classifications_per_title))

        classifications.append({
            "Representation Type": representation_type,
            "Text": text,
            "Most Common Classifications": get_all_classifications2(classification_result)
        })
    
    publicity_classifications_per_title.append({"Title": title, "Classifications": classifications_per_title})
    
    # Save classifications to a CSV file
    classifications_df = pd.DataFrame(classifications)
    classifications_df.to_csv(f'/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/publicity classifications per article/{title[:50]}_classifications.csv', index=False)
# '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/publicity classifications per article'
 

# Save classifications to a CSV file
classifications_df = pd.DataFrame(publicity_classifications_per_title)
classifications_df.to_csv('/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/classifications_per_publicity.csv', index=False)


# All classifications of each article should be united --> dict : subheadline : classifications(union)   -->    article_classifications_per_article
# All classifications of each publicity should be united --> dict : title : classifications(union)     -->    publicity_classifications_per_title

for article in article_classifications_per_article:
    article_classifications = article['Classifications']
    max_closer_classification = 0
    best_publicities = []
    for publicity in publicity_classifications_per_title:
        publicity_classifications = publicity['Classifications']
        shared_classifications = set(article_classifications).intersection(publicity_classifications)
        total_classifications = set(article_classifications).union(publicity_classifications)
        if not shared_classifications:
            continue
        closer_classification = len(shared_classifications) / len(total_classifications)

        if closer_classification > max_closer_classification:
            max_closer_classification = closer_classification
            if max_closer_classification == 0.0:
                continue
            best_publicities = [publicity['Title']]
        elif closer_classification == max_closer_classification:
            if max_closer_classification == 0.0:
                continue
            best_publicities.append(publicity['Title'])

    for publicity_title in best_publicities:
        print(f"Article: {article['Headline']}, Publicity: {publicity_title}, Closer Classification: {max_closer_classification}, shared_classifications: {shared_classifications}, total_classifications: {total_classifications}")
# then we cross all, for each of the articles, we go check which one has the "closer classification"

# closer classification:  is the number of shared classifications between the article and the publicity devide by the total number of classifications of the article and the publicity



# Function to match each article representation with each publicity representation and save to separate CSV files
def match_and_save(article_classifications_path, publicity_classifications_path, output_dir):
    """
    Matches article classifications with publicity classifications and saves the results to CSV files.

    This function reads two CSV files containing article and publicity classifications, respectively. 
    It then compares the classifications and finds matches between articles and publicities based on 
    their classifications. The matching results are saved as CSV files in the specified output directory.

    Args:
        article_classifications_path (str): The file path to the CSV file containing article classifications.
        publicity_classifications_path (str): The file path to the CSV file containing publicity classifications.
        output_dir (str): The directory where the output CSV files will be saved.

    Returns:
        None

    Raises:
        FileNotFoundError: If any of the input file paths do not exist.
        ValueError: If there is an issue with reading the CSV files or processing the data.

    CSV File Structure:
        The article classifications CSV file should have the following columns:
            - "Headline": The headline of the article.
            - "Subheadline": The subheadline of the article.
            - "Keywords": Keywords associated with the article.
            - "Summary": A summary of the article.
            - "Most Common Classifications": A string representation of a list of classifications.

        The publicity classifications CSV file should have the following columns:
            - "Text": The text of the publicity.
            - "Most Common Classifications": A string representation of a list of classifications.

    Output:
        For each combination of article column and publicity column, a CSV file will be created in the 
        output directory. The CSV file will contain the following columns:
            - The article column (e.g., "Headline", "Subheadline", etc.)
            - "Article Classifications": The classifications of the article.
            - "Matching Publicities": A list of dictionaries containing matching publicity texts and their classifications.
    """
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
                        matching_publicities.append({
                            "Text": publicity_text,
                            "Classifications": publicity_classifications
                        })

                matching_results.append({
                    f"{article_col}": article_text,
                    "Article Classifications": article_classifications,
                    "Matching Publicities": matching_publicities
                })

            matching_results_df = pd.DataFrame(matching_results)
            output_path = os.path.join(output_dir, f"{article_col}_vs_{publicity_col}.csv")
            matching_results_df.to_csv(output_path, index=False)

# Create output directory if it doesn't exist
output_dir = '/Users/ramisafi/Downloads/Research Journal Project/Article_Publicity_Matches_WITH_CLASSIFICATIONS'
os.makedirs(output_dir, exist_ok=True)

# Match and save the results
match_and_save(
    '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/article_classifications.csv',
    '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/publicity_classifications.csv',
    output_dir
)
