import pandas as pd
"""
This script reads OCR results, SAM-ViT results, and BLIP results from CSV files, 
concatenates their content, and saves the fused content into a new CSV file.

Modules:
    pandas: For data manipulation and analysis.
    sys: Provides access to some variables used or maintained by the interpreter.
    os: Provides a way of using operating system dependent functionality.

File Paths:
    ocr_results_path (str): Path to the OCR results CSV file.
    blip_path (str): Path to the BLIP results CSV file.
    sam_vit_path (str): Path to the SAM-ViT results CSV file.
    fused_output_path (str): Path to save the fused results CSV file.

DataFrames:
    ocr_results_df (DataFrame): DataFrame containing OCR results.
    sam_vit_df (DataFrame): DataFrame containing SAM-ViT results.
    blip_df (DataFrame): DataFrame containing BLIP results.
    fused_df (DataFrame): DataFrame containing the fused content from OCR, SAM-ViT, and BLIP results.

Raises:
    FileNotFoundError: If any of the input CSV files are not found.

Steps:
    1. Verify the existence of the input CSV files.
    2. Read the CSV files into DataFrames.
    3. Define representations for Publicity and Articles.
    4. Concatenate the content of the three sources.
    5. Remove any semicolons from the fused content.
    6. Create a DataFrame with the fused content.
    7. Save the fused content to a CSV file.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Define file paths
ocr_results_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/OCR_results.csv'
blip_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/Blip_results.csv'
sam_vit_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/SAM&Vit_results.csv'

if not os.path.exists(ocr_results_path):
    raise FileNotFoundError(f"File not found: {ocr_results_path}")
if not os.path.exists(sam_vit_path):
    raise FileNotFoundError(f"File not found: {sam_vit_path}")
if not os.path.exists(blip_path):
    raise FileNotFoundError(f"File not found: {blip_path}")

# Read the CSV files for publicity representations
ocr_results_df = pd.read_csv(ocr_results_path)
sam_vit_df = pd.read_csv(sam_vit_path)
blip_df = pd.read_csv(blip_path)

# Define representations for Publicity and Articles
publicity_representations = {
    "Title": ocr_results_df['Title'].tolist(),  # Assuming all CSVs have the same titles
    "OCR": ocr_results_df['Extracted Words'].tolist(),
    "SAM-ViT": sam_vit_df['Descriptions'].tolist(),
    "BLIP": blip_df['Description'].tolist(),
}
# Concatenate the content of the three sources
fused_content = [
    (title, f"{ocr} {sam_vit} {blip}")
    for title, ocr, sam_vit, blip in zip(
        publicity_representations["Title"],
        publicity_representations["OCR"],
        publicity_representations["SAM-ViT"],
        publicity_representations["BLIP"]
    )
]

# Remove any semicolons from the fused content
fused_content = [
    (title, content.replace(';', ''))
    for title, content in fused_content
]

# Create a DataFrame with the fused content
fused_df = pd.DataFrame(fused_content, columns=["Title", "Fused Content"])

# Define the output path for the fused CSV
fused_output_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/fused_results.csv'

# Save the fused content to a CSV file
fused_df.to_csv(fused_output_path, index=False)
