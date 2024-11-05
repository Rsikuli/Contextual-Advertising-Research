import re
import csv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize the tokenizer and model
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def WHITESPACE_HANDLER(text):
    return re.sub('\s+', ' ', re.sub('\n+', ' ', text.strip()))

def clean_text(text):
    # Remove HTML tags and special characters
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'[\xa0]', '', text)  # Remove specific special characters
    text = re.sub(r'\u2009', ' ', text, flags=re.UNICODE)  # Replace \u2009 with a space
    text = re.sub(r'\[VIDÉO\]', '', text)  # Remove [VIDÉO]
    text = re.sub(r'\n\n\s*\*\*\*', '', text)  # Remove \n\n ***
    text = re.sub(r'\*\*\*', '', text)  # Remove ***
    text = re.sub(r'[«»]', '', text)  # Remove « and »
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

def summarize_text(text):
    input_ids = tokenizer(
        [WHITESPACE_HANDLER(text)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=716
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=128,
        no_repeat_ngram_size=2,
        num_beams=4
    )[0]

    summary = tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )

    return summary

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

# Extract paragraphs, captions, headlines, subheadlines, and summaries
paragraphs, captions, headlines, subheadlines, summaries = extract_paragraphs_from_file(file_path)

# Write the results to a CSV file
csv_file_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Paragraph', 'Caption', 'Headline', 'Subheadline', 'Summary'])
    for paragraph, caption, headline, subheadline, summary in zip(paragraphs, captions, headlines, subheadlines, summaries):
        csvwriter.writerow([paragraph, caption, headline, subheadline, summary])
