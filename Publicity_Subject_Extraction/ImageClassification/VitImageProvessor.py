import torch  
import sys
import os
from transformers import ViTImageProcessor, ViTForImageClassification    # type: ignore
from PIL import Image   # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Publicity_Subject_Extraction.ImageClassification.img_tools import translator

# Google VitImageProvessor for single image classification

def VitImageProvessorImgClassify(IMAGE_PATH):
    """
    Classifies an image using the Vision Transformer (ViT) model.

    Args:
        IMAGE_PATH (str): The path to the image file to be classified.

    Returns:
        list: A list of translated words representing the top prediction.
    """
    # Open and convert the image to RGB
    image = Image.open(IMAGE_PATH).convert('RGB')

    # Load the pre-trained ViT image processor and model
    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

    # Process the image and get model outputs
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits

    # Apply softmax to obtain probabilities
    probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]

    # Get top predictions
    top_predictions = model.config.id2label
    sorted_predictions = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)

    # Display top predictions along with their probabilities (scores)
    for idx, score in sorted_predictions[:5]:  # Display top 5 predictions
        label = top_predictions[idx]
        print(f"{label}: {score.item():.3f}")

    # Get the top prediction in a list of words
    top_prediction = sorted_predictions[0]
    label_idx, score = top_prediction
    label = top_predictions[label_idx]

    lst = label.split(",")
    lst = [word.strip() for word in lst]
    for i in range(len(lst)):
        lst[i] = translator(lst[i])

    return lst