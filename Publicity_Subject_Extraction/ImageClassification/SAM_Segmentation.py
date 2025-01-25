import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
import os
import sys
import csv

sys.path.append("..")

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from Publicity_Subject_Extraction.ImageClassification.VitImageProvessor import VitImageProvessorImgClassify

def show_anns(anns):
    """
    Display annotations on the image using matplotlib.

    Parameters:
    anns (list): List of annotations where each annotation is a dictionary containing 'segmentation' and 'area'.
    """
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)

def filter_image_by_resolution(cropped_image, width_org, height_org):
    """
    Filter images based on their resolution.

    Parameters:
    cropped_image (numpy.ndarray): The cropped image to be filtered.
    width_org (int): The original width of the image.
    height_org (int): The original height of the image.

    Returns:
    bool: True if the cropped image meets the resolution criteria, False otherwise.
    """
    width, height = cropped_image.shape[1], cropped_image.shape[0]
    minimum_resolution = 0.03 * width_org * height_org
    maximum_resolution = 0.75 * width_org * height_org

    if minimum_resolution <= width * height <= maximum_resolution and width <= 0.70 * width_org and height <= 0.70 * height_org:
        return True
    return False

# Path to the checkpoint file for the SAM model
CHECK_POINT = '/Users/ramisafi/Downloads/sam_vit_h_4b8939.pth'
sam = sam_model_registry["vit_h"](checkpoint=CHECK_POINT)
DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
sam.to(device=DEVICE)
mask_generator = SamAutomaticMaskGenerator(sam)

# Paths to the script and CSV file
script_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/script.rtf'
csv_file_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/SAM&Vit_results.csv'

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Descriptions'])

    with open(script_path, "rt") as myfile:
        for line in myfile:
            index = line.find("=")
            if index == -1:
                continue

            title = line[:index].strip()

            origin = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/common/Images/raw_images/'
            IMAGE_PATH = os.path.join(origin, title + '.png')

            if os.path.exists(IMAGE_PATH):
                # Perform segmentation
                image = cv2.imread(IMAGE_PATH)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                masks = mask_generator.generate(image)

                # Save the segmented images in an output folder
                image_base_name = title
                output_directory = os.path.join('/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/common/Images/segmentation_outputs/', image_base_name)
                os.makedirs(output_directory, exist_ok=True)

                width_org, height_org = image.shape[1], image.shape[0]
                descriptions = []


                for i in range(len(masks)):
                    print(title)

                    mask_content = masks[i]['segmentation']  # Binary mask
                    non_zero_ratio = (mask_content > 0).sum() / mask_content.size

                    # Filter based on content density
                    if non_zero_ratio < 0.05 or non_zero_ratio > 0.3:  # Adjusted thresholds
                        continue

                    x, y, width, height = masks[i]['bbox']
                    cropped_image = image[int(y):int(y+height), int(x):int(x+width)]
                    filename = os.path.join(output_directory, str(i) + '.png')
                    cv2.imwrite(filename, cropped_image)
                    print(f"Image '{str(i)}.png' meets resolution criteria and saved to '{output_directory}'.")


                    # Assuming VitImageProvessorImgClassify is a function that takes an image path and returns a description
                    description = VitImageProvessorImgClassify(filename)
                    if isinstance(description, list):
                        description = "; ".join(description)
                    descriptions.append(description)

                if descriptions:
                    # Convert each item in descriptions to a string and join them with a semicolon
                    csv_writer.writerow([title, "; ".join(map(str, descriptions))])
                else:
                    csv_writer.writerow([title, "No valid segments found"])
            else:
                print(f"Image {IMAGE_PATH} not found.")
