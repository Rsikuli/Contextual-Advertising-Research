import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import csv
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from Publicity_Subject_Extraction.ImageClassification.img_tools import translator

# Load the pretrained model and tokenizer
pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def blipProcessorImgClassify(IMAGE_PATH):
    """
    Classifies an image and translates the classification result to French.

    Args:
        IMAGE_PATH (str): The file path to the image to be classified.

    Returns:
        str: The classification result translated to French.

    Raises:
        FileNotFoundError: If the image file does not exist at the specified path.
        ValueError: If the image cannot be processed or classified.
    """
    image = Image.open(IMAGE_PATH).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_new_tokens=50)
    decoded_text = processor.decode(out[0], skip_special_tokens=True, max_new_tokens=50)
    french_decoded_text = translator(decoded_text)
    return french_decoded_text

script_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/script.rtf'
csv_file_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/Blip_results.csv'

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Description'])

    with open(script_path, "rt") as myfile:
        for line in myfile:
            index = line.find("=")
            if index == -1:
                continue

            title = line[:index].strip()
            manuscript = line[index+1:].strip()

            origin = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/common/Images/raw_images/'
            IMAGE_PATH = os.path.join(origin, title + '.png')

            if os.path.exists(IMAGE_PATH):
                description = blipProcessorImgClassify(IMAGE_PATH)
                csv_writer.writerow([title, description])
            else:
                print(f"Image {IMAGE_PATH} not found.")
