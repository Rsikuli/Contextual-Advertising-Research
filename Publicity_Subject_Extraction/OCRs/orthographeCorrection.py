#extraction and csv files making 

import csv
from typing import List, Any
import sys
import os

# Add the parent directory of Publicity_Subject_Extraction to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from easyOCRTextExtraction import easyOCR_extract #type: ignore
from paddle_ocr_text_extraction import paddleOCR_extract #type: ignore
from common.tools import precision_recall, real_words_check_nested, fuse_ocr_results, remove_special_characters  #type: ignore
from Publicity_Subject_Extraction.common.dictionariesCreation import letter_dict #type: ignore
#extraction and csv files making 


# Paths for CSV files/Users/ramisafi/Downloads/OCR_results
csv_easyocr_path = '/Users/ramisafi/Downloads/OCR_results/EasyOCR_results.csv'
csv_paddleocr_path = '/Users/ramisafi/Downloads/OCR_results/PaddleOCR_results.csv'
csv_fusion_path = '/Users/ramisafi/Downloads/OCR_results/Fusion_results.csv'
csv_summary_path = '/Users/ramisafi/Downloads/OCR_results/Summary_results.csv'



# EasyOCR results
precision_EasyOCR_init = 0
recall_EasyOCR_init = 0
f_score_EasyOCR_init = 0

precision_EasyOCR_fin = 0
recall_EasyOCR_fin = 0
f_score_EasyOCR_fin = 0

# PaddleOCR results
precision_PaddleOCR_init = 0
recall_PaddleOCR_init = 0
f_score_PaddleOCR_init = 0

precision_PaddleOCR_fin = 0
recall_PaddleOCR_fin = 0
f_score_PaddleOCR_fin = 0

precision_fusion_fin = 0
recall_fusion_fin = 0
f_score_fusion_fin = 0

results_list: List[Any] = []
counter = 0
script_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/script.rtf'

# Open CSV file to write results
csv_file_path = '/Users/ramisafi/Desktop/Research/OCR_results.csv'
with open(csv_file_path, mode='w', newline='') as csv_file, \
    open(csv_easyocr_path, mode='w', newline='') as csv_easyocr_file, \
        open(csv_paddleocr_path, mode='w', newline='') as csv_paddleocr_file, \
            open(csv_fusion_path, mode='w', newline='') as csv_fusion_file, \
                open(csv_summary_path, mode='w', newline='') as csv_summary_file:
    csv_writer = csv.writer(csv_file)
    csv_easyocr_writer = csv.writer(csv_easyocr_file)
    csv_paddleocr_writer = csv.writer(csv_paddleocr_file)
    csv_fusion_writer = csv.writer(csv_fusion_file)
    csv_summary_writer = csv.writer(csv_summary_file)

    # Write header
    csv_writer.writerow(['Title', 'EasyOCR Extracted Words', 'PaddleOCR Extracted Words'])
    csv_easyocr_writer.writerow(['Title', 'Extracted Text', 'Precision', 'Recall', 'F-Score'])
    csv_paddleocr_writer.writerow(['Title', 'Extracted Text', 'Precision', 'Recall', 'F-Score'])
    csv_fusion_writer.writerow(['Title', 'Extracted Text', 'Precision', 'Recall', 'F-Score'])


    with open(script_path, "rt") as myfile:
        for line in myfile:
            if counter >= 300 :
                break
            counter += 1

            index = line.find("=")
            title = line[:index]
            manuscript = line[index + 1:]

            lst_manuscript = manuscript.split(" ")
            min_lst_manuscript = [item.lower() for item in lst_manuscript]
            min_lst_manuscript = [word.rstrip('\n') for word in min_lst_manuscript]
            lst_check_manuscript = remove_special_characters(min_lst_manuscript)
            refined_str_manuscript = " ".join(lst_check_manuscript)

            print(title)

            print("manuscript: ", manuscript)
            print("manuscript refined: ", refined_str_manuscript)

            # Image Threshold
            origin = '/Users/ramisafi/Desktop/Research Journal Project/Publicity_Subject_Extraction/common/Images/raw_images/'
            IMAGE_PATH = origin + title + '.png'

            # EasyOCR extraction
            result_easyocr = easyOCR_extract(IMAGE_PATH)

            lst_result_easyocr_before = result_easyocr.split(" ")
            lst_easyocr_before = [item.lower() for item in lst_result_easyocr_before]
            str_easyocr_before = " ".join(lst_easyocr_before)

            precision, recall, f_score = precision_recall(refined_str_manuscript, str_easyocr_before)
            print("EasyOCR Before dictionary filtration: ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)

            precision_EasyOCR_init += precision
            recall_EasyOCR_init += recall
            f_score_EasyOCR_init += f_score

            lst_result_easyocr = result_easyocr.split(" ")
            min_list_easyocr = [item.lower() for item in lst_result_easyocr]
            min_list_check_easyocr = remove_special_characters(min_list_easyocr)
            min_list_checked_easyocr = real_words_check_nested(min_list_check_easyocr, letter_dict)
            min_string_checked_easyocr = " ".join(min_list_checked_easyocr)

            precision, recall, f_score = precision_recall(refined_str_manuscript, min_string_checked_easyocr)
            print("EasyOCR After dictionary filtration ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)

            precision_EasyOCR_fin += precision
            recall_EasyOCR_fin += recall
            f_score_EasyOCR_fin += f_score

            csv_easyocr_writer.writerow([title, min_string_checked_easyocr, precision, recall, f_score])


            # PaddleOCR extraction
            result_paddleocr = paddleOCR_extract(IMAGE_PATH)

            lst_result_paddleocr_before = result_paddleocr.split(" ")
            lst_paddleocr_before = [item.lower() for item in lst_result_paddleocr_before]
            str_paddleocr_before = " ".join(lst_paddleocr_before)

            precision, recall, f_score = precision_recall(refined_str_manuscript, str_paddleocr_before)
            print("PaddleOCR Before dictionary filtration: ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)

            precision_PaddleOCR_init += precision
            recall_PaddleOCR_init += recall
            f_score_PaddleOCR_init += f_score

            lst_result_paddleocr = result_paddleocr.split(" ")
            min_list_paddleocr = [item.lower() for item in lst_result_paddleocr]
            min_list_check_paddleocr = remove_special_characters(min_list_paddleocr)
            min_list_checked_paddleocr = real_words_check_nested(min_list_check_paddleocr, letter_dict)
            min_string_checked_paddleocr = " ".join(min_list_checked_paddleocr)

            precision, recall, f_score = precision_recall(refined_str_manuscript, min_string_checked_paddleocr)
            print("PaddleOCR After dictionary filtration: ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)


            precision_PaddleOCR_fin += precision
            recall_PaddleOCR_fin += recall
            f_score_PaddleOCR_fin += f_score

            csv_paddleocr_writer.writerow([title, min_string_checked_paddleocr, precision, recall, f_score])





            # Fusion of EasyOCR and PaddleOCR

            fusion_list = fuse_ocr_results(min_list_checked_easyocr, min_list_checked_paddleocr)

            string_fusion = " ".join(fusion_list)
            precision, recall, f_score = precision_recall(refined_str_manuscript, string_fusion)

            print("Fusion of EasyOCR and PaddleOCR After dictionary filtration: ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)
            print("PaddleOCR: ", min_list_checked_paddleocr)
            print("EasyOCR: ", min_list_checked_easyocr)
            print("Fusion: ", fusion_list)
            print("Manuscript: ", manuscript)


            precision_fusion_fin += precision
            recall_fusion_fin += recall
            f_score_fusion_fin += f_score

            csv_fusion_writer.writerow([title, string_fusion, precision, recall, f_score])


            # Write to CSV
            csv_writer.writerow([title, min_string_checked_easyocr, min_string_checked_paddleocr])

            print("\n\n")

print("Results:")
print("Number of processed images: ", counter)
print()
print("EasyOCR Before dictionary filtration")
print("Averages are : precision: ", (precision_EasyOCR_init / counter), "recall: ", (recall_EasyOCR_init / counter), "f_score: ", (f_score_EasyOCR_init / counter))

print("EasyOCR After dictionary filtration")
print("Averages are : precision: ", (precision_EasyOCR_fin / counter), "recall: ", (recall_EasyOCR_fin / counter), "f_score: ", (f_score_EasyOCR_fin / counter))

print("PaddleOCR Before dictionary filtration")
print("Averages are : precision: ", (precision_PaddleOCR_init / counter), "recall: ", (recall_PaddleOCR_init / counter), "f_score: ", (f_score_PaddleOCR_init / counter))

print("PaddleOCR After dictionary filtration")
print("Averages are : precision: ", (precision_PaddleOCR_fin / counter), "recall: ", (recall_PaddleOCR_fin / counter), "f_score: ", (f_score_PaddleOCR_fin / counter))


print("Fusion of EasyOCR and PaddleOCR After dictionary filtration")
print("Averages are : precision: ", (precision_fusion_fin / counter), "recall: ", (recall_fusion_fin / counter), "f_score: ", (f_score_fusion_fin / counter))



