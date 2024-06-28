from transformers import BlipProcessor, BlipForConditionalGeneration   # type: ignore
from PIL import Image  # type: ignore
from ImageClassification.tools import translator   # type: ignore

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


def blipProcessorImgClassify(IMAGE_PATH):
    image = Image.open(IMAGE_PATH).convert('RGB')

    # conditional image captioning
    inputs = processor(image, return_tensors="pt")

    out = model.generate(**inputs, max_new_tokens=50)
    decoded_text = processor.decode(out[0], skip_special_tokens=True, max_new_tokens=50)
    print(decoded_text)
    fr = translator(decoded_text)
    print(fr)
    ll = decoded_text.split(" ")
    return ll