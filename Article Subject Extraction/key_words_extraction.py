import sys
import os
import csv
from transformers import pipeline
import spacy


# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load the pipeline for token classification with yanekyuk
pipe_yanekyuk = pipeline("token-classification", model="yanekyuk/camembert-keyword-extractor")

# Function to check if a string is alphanumeric
def is_alphanumeric(word):
    return word.isalnum()



# # Load the French language model
# nlp = spacy.load("fr_core_news_sm")

# def lemmatize_text(text):
#     doc = nlp(text)
#     return " ".join([token.lemma_ for token in doc if not token.is_stop])

# text = "licate putation ift ike Jon 2016 Ken ake len Calvin Harris Tom les ton Joe ift Gra Elizabeth Hur ley Gra Elizabeth Hur ley Divin Brown Gra 1995 Anna ber stein ing lan Hong Paul New man Whi ney Houston Bob Kri"
# lemmatized_text = lemmatize_text(text)
# print(lemmatized_text)  # Output: "ce être exemple montrer mot inutile"




# Function to extract keywords using the pipeline and filter for B-KEY and I-KEY
# Function to extract keywords using the pipeline and filter for B-KEY and I-KEY
def extract_keywords_v2(text):
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
    pipeline = pipe_yanekyuk
    results = pipeline(text)

    keywords = []
    current_keyword = ""

    for item in results:
        label = item['entity']
        word = item['word']

        # Process only B-KEY and I-KEY labels
        if label in ['B-KEY', 'I-KEY']:
            if label == 'B-KEY':
                # Remove the '▁' marker at the start of words
                if word.startswith('▁'):
                    word = word[1:]
                # If it's a new keyword, add the previous keyword to the list
                if current_keyword:
                    keywords.append(current_keyword)
                current_keyword = word  # Start a new keyword

            elif label == 'I-KEY':
                if word.startswith('▁'):
                    word = word[1:]
                    # Means a new word in the same keyword
                    current_keyword = current_keyword + " " + word
                else:
                    current_keyword = current_keyword + word

        else:
            # Add the completed keyword to the list and reset
            if current_keyword:
                keywords.append(current_keyword)
                current_keyword = ""

    # Add the last keyword if it exists
    if current_keyword:
        keywords.append(current_keyword)

    return ', '.join(keywords)



# # Read the CSV file
# input_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/processed_results.csv'
# output_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

# with open(input_csv_path, mode='r', encoding='utf-8') as infile, open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
#     reader = csv.DictReader(infile)
#     fieldnames = ['Headline', 'Caption', 'Subheadline', 'Summary', 'Keywords']  # Specify output fields
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
#     writer.writeheader()
    
#     for row in reader:
#         paragraph = row['Paragraph']
#         keywords = extract_keywords_v2(paragraph)
        
#         # Get other fields safely
#         caption = row.get('Caption', '')
#         headline = row.get('Headline', '')
#         subheadline = row.get('Subheadline', '')
#         summary = row.get('Summary', '')

#         # Write only the processed data to the output file
#         writer.writerow({
#             'Headline': headline,
#             'Caption': caption,
#             'Subheadline': subheadline,
#             'Summary': summary,
#             'Keywords': keywords
#         })

# print("Keywords extraction and CSV update completed.")





