import sys
import os
import csv
from transformers import pipeline

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load the pipeline for token classification with yanekyuk
pipe_yanekyuk = pipeline("token-classification", model="yanekyuk/camembert-keyword-extractor")

# Function to check if a string is alphanumeric
def is_alphanumeric(word):
    return word.isalnum()


# Function to extract keywords using the pipeline and filter for B-KEY and I-KEY
def extract_keywords_v2(text, pipeline):
    """
    Extracts keywords from the given text using the specified pipeline.

    This function processes the input text through a provided NLP pipeline to identify and extract keywords.
    It filters out words that are less than 3 characters long and only includes words labeled as 'B-KEY' or 'I-KEY'.

    Args:
        text (str): The input text from which to extract keywords.
        pipeline (callable): A callable NLP pipeline that processes the text and returns a list of entities.

    Returns:
        str: A comma-separated string of extracted keywords.
    """
    results = pipeline(text)
    words_and_labels = []

    for item in results:
        label = item['entity']
        word = item['word']

        if word.startswith('▁'):
            word = word[1:]

        if (label == 'B-KEY' or label == 'I-KEY') and len(word) > 2:
            words_and_labels.append(word)

    return ', '.join(words_and_labels)

# Read the CSV file
input_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results.csv'
output_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

with open(input_csv_path, mode='r', encoding='utf-8') as infile, open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Keywords']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        paragraph = row['Paragraph']
        keywords = extract_keywords_v2(paragraph, pipe_yanekyuk)
        row['Keywords'] = keywords
        print(f"Extracted keywords for paragraph: {keywords}")
        print()
        writer.writerow(row)

print("Keywords extraction and CSV update completed.")




