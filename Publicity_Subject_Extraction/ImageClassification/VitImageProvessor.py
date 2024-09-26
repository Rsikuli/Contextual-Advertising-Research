import torch  
from transformers import ViTImageProcessor, ViTForImageClassification    # type: ignore
from PIL import Image   # type: ignore



# Google VitImageProvessor for single image classification

def VitImageProvessorImgClassify(IMAGE_PATH):

    image = Image.open(IMAGE_PATH).convert('RGB')

    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

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


    # model predicts one of the 1000 ImageNet classes
    #predicted_class_idx = logits.argmax(-1).item()
    #print("Predicted class:", model.config.id2label[predicted_class_idx])

    #get the Top prediction in a list of words
    top_prediction = sorted_predictions[0]
    label_idx, score = top_prediction
    label = top_predictions[label_idx]

    lst = label.split(",")
    lst = [word.strip() for word in lst]

    #print(lst)
    #print(f"Top Prediction is {label} with score: {score.item(): .3f}")
    return lst