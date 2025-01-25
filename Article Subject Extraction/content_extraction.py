import re
from summarize_text import summarize_text
from key_words_extraction import extract_keywords_v2
import csv


def clean_text(text):
    # Remove HTML tags and special characters
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[\xa0]', '', text)  # Remove specific special characters
    text = re.sub(r'\u2009', ' ', text, flags=re.UNICODE)  # Replace \u2009 with a space
    text = re.sub(r'\[VIDÉO\]', '', text)  # Remove [VIDÉO]
    text = re.sub(r'\n\n\s*\*\*\*', '', text)  # Remove \n\n ***
    text = re.sub(r'\*\*\*', '', text)  # Remove ***
    text = re.sub(r'[«»]', '', text)  # Remove « and »
    text = re.sub(r'\\', '', text)  # Remove backslashes
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.strip()

def extract_content_and_caption(data_str):
    # Extract content elements
    content_matches = re.findall(r"'content':\s*'([^']*)'", data_str)
    content_paragraph = ' '.join(content_matches)

    # Extract caption
    caption_match = re.search(r"'caption':\s*'([^']*)'", data_str)
    caption = caption_match.group(1) if caption_match else 'No caption available'

    # Extract headlines and subheadlines
    headline_matches = re.findall(r"'headlines':\s*\{[^}]*'basic':\s*'([^']*)'", data_str)
    subheadline_matches = re.findall(r"'subheadlines':\s*\{[^}]*'basic':\s*'([^']*)'", data_str)
    
    headlines = ' '.join(headline_matches)
    subheadlines = ' '.join(subheadline_matches)

    # Clean the extracted text
    content_paragraph = clean_text(content_paragraph)
    caption = clean_text(caption)
    headlines = clean_text(headlines)
    subheadlines = clean_text(subheadlines)

    return content_paragraph, caption, headlines, subheadlines


def extract_paragraphs_from_file(file_path):
    """
    Extracts paragraphs, captions, headlines, subheadlines, and summaries from a given file.
    Args:
        file_path (str): The path to the file from which to extract content.
    Returns:
        tuple: A tuple containing five lists:
            - paragraphs (list of str): Extracted paragraphs.
            - captions (list of str): Extracted captions.
            - headlines_list (list of str): Extracted headlines.
            - subheadlines_list (list of str): Extracted subheadlines.
            - summaries (list of str): Summaries of the extracted paragraphs.
    Note:
        This function assumes the existence of the `extract_content_and_caption` and `summarize_text` functions.
    """
    paragraphs = []
    captions = []
    headlines_list = []
    subheadlines_list = []
    summaries = []
    seen_headlines = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                content_paragraph, caption, headlines, subheadlines = extract_content_and_caption(line)
                if headlines not in seen_headlines:
                    paragraphs.append(content_paragraph)
                    captions.append(caption)
                    headlines_list.append(headlines)
                    subheadlines_list.append(subheadlines)
                    seen_headlines.add(headlines)
                    
                    # Summarize the paragraph
                    summary = summarize_text(content_paragraph)
                    summaries.append(summary)

    return paragraphs, captions, headlines_list, subheadlines_list, summaries

# Path to the text file
file_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/1_article.rtf'

# # Extract paragraphs, captions, headlines, subheadlines, and summaries
# paragraphs, captions, headlines, subheadlines, summaries = extract_paragraphs_from_file(file_path)

# # Write the results to a CSV file
# csv_file_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results.csv'
# with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(['Paragraph', 'Caption', 'Headline', 'Subheadline', 'Summary'])
#     for paragraph, caption, headline, subheadline, summary in zip(paragraphs, captions, headlines, subheadlines, summaries):
#         csvwriter.writerow([paragraph, caption, headline, subheadline, summary])



def process_existing_csv(input_csv_path, output_csv_path):
    """
    Reads a CSV file containing content paragraphs, captions, headlines, and subheadlines,
    and writes a new CSV file with summaries and keywords added.

    Args:
        input_csv_path (str): Path to the input CSV file.
        output_csv_path (str): Path to the output CSV file.
    """
    with open(input_csv_path, 'r', encoding='utf-8') as infile, open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['Headline', 'Subheadline', 'Summary', 'Keywords']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            content_paragraph = row.get('Paragraph', '')
            headline = row.get('Headline', '')
            subheadline = row.get('Subheadline', '')

            # Generate summary
            summary = summarize_text(content_paragraph)

            # Extract keywords
            keywords = extract_keywords_v2(content_paragraph)

            # Write to the output CSV
            writer.writerow({
                'Headline': headline,
                'Subheadline': subheadline,
                'Summary': summary,
                'Keywords': ', '.join(keywords)
            })

# Input and output CSV file paths
input_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/extracted_articles.csv'
output_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/processed_results.csv'

with open(input_csv_path, mode='r', encoding='utf-8') as infile, open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Summary'] + ['Keywords']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        content_paragraph = row['Paragraph']  # Adjust to match actual column name

        # Generate summary
        summary = summarize_text(content_paragraph)
        row['Summary'] = summary
        print(f"Generated summary for paragraph: {summary}")

        # Extract keywords
        keywords = extract_keywords_v2(content_paragraph)
        row['Keywords'] = keywords

        print(f"Extracted keywords for paragraph: {keywords}")
        print()

        writer.writerow(row)

print("Keywords extraction and CSV update completed.")


print("Processing and writing to CSV completed successfully!")

