
#Translator Model and method
import os
from transformers import MarianMTModel, MarianTokenizer  # type: ignore
from PIL import Image  # type: ignore

# Load the pretrained model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-fr'
Translator_tokenizer = MarianTokenizer.from_pretrained(model_name)
Translator_model = MarianMTModel.from_pretrained(model_name)

# Text to translate
text_to_translate = "trailer truck, tractor trailer, trucking rig, rig, articulated lorry, semi, recreational vehicle, RV, R.V."

def translator(textToTranslate):
    """
    Translates the given text from English to French using a pretrained MarianMT model.

    Args:
        textToTranslate (str): The text to be translated from English to French.

    Returns:
        str: The translated text in French.

    Example:
        translated_text = translator("Hello, how are you?")
        print(translated_text)  # Bonjour, comment ça va?
    """
    # Tokenize input text
    inputs = Translator_tokenizer(textToTranslate, return_tensors="pt")
    
    # Translate text from English to French
    translated = Translator_model.generate(**inputs, max_length=128, num_beams=4, no_repeat_ngram_size=3, early_stopping=True)
    #The reaccuring problem with the translator is that the model it calls to generate the translated text is VITForImage bcz it's being reinitialized again in the next scope 


    # Decode the translated output
    translated_text = Translator_tokenizer.decode(translated[0], skip_special_tokens=True)

    return translated_text


def filter_images_by_resolution(name):
    """
    Filters images in a specified folder based on their resolution relative to an original image.
    This function reads an original image and calculates its width and height. It then iterates 
    through all images in a specified folder, checking if their resolution falls within a specified 
    range relative to the original image. If an image meets the criteria, it is saved to an output 
    folder.
    Args:
        name (str): The name of the original image file (without extension) and the subfolder 
                    containing images to be filtered.
    Raises:
        FileNotFoundError: If the original image file does not exist.
        OSError: If there is an error opening or saving an image file.
    Example:
        filter_images_by_resolution("example_image")
    """
    # Create a new folder if it doesn't exist
    folder_path = "/Users/ramisafi/Desktop/Research Journal Project/Publicity Subject Extraction/common/Images/segmentation_outputs/Output_" + name
    output_folder = "/Users/ramisafi/Desktop/Research Journal Project/Publicity Subject Extraction/common/Images/filtered_outputs/"+ name
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    
    with Image.open("/Users/ramisafi/Desktop/Research/outputs/"+name+".png") as org:
        width_org, height_org = org.size
        print(width_org)
        print(height_org)
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filepath.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Add more extensions if needed
            with Image.open(filepath) as img:
                width, height = img.size

                # width_min = 0.2*width
                # height_min = 0.2*height
                
                minimumResolution = 0.05*width_org*height_org
                maximumResolution = 0.4*width_org*height_org

                #minimum largeur et hauteur
                #max largeur et hauteur
                #chaq tt seul : largeur, hauteur 


                #if 0.02*width_org <= width <= 0.6*width_org and 0.02*height_org <= height <= 0.6*height_org:
                if minimumResolution <= width*height <= maximumResolution and width <= 0.88*width_org and height <= 0.88*height_org:
                    #if width <= 0.8*width_org:
                        # Save image to the output folder
                    output_path = os.path.join(output_folder, filename)
                    img.save(output_path)
                    
                    print(f"Image '{filename}' meets resolution criteria and saved to '{output_folder}'.")

# Set your folder path, resolution range, and output folder path


