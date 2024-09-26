from transformers import BlipProcessor, BlipForConditionalGeneration   # type: ignore
from PIL import Image  # type: ignore
from Publicity_Subject_Extraction.ImageClassification.img_tools import translator

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

"""

"""
def blipProcessorImgClassify(IMAGE_PATH):
    image = Image.open(IMAGE_PATH).convert('RGB')

    # conditional image captioning
    inputs = processor(image, return_tensors="pt")

    out = model.generate(**inputs, max_new_tokens=50)
    decoded_text = processor.decode(out[0], skip_special_tokens=True, max_new_tokens=50)
    #print(decoded_text)
    french_decoded_text = translator(decoded_text)
    #print(fr)
    #ll = decoded_text.split(" ")
    return french_decoded_text