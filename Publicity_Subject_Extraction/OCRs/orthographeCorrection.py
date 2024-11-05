import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from easyOCRTextExtraction import easyOCR_extract
from Publicity_Subject_Extraction.common.tools import precision_recall, real_words_check_nested, special_caracters_remove
from typing import List, Any
from Publicity_Subject_Extraction.common.dictionariesCreation import letter_dict #type: ignore


#Easy0CR_results_list

precision_EasyOCR_init=0
recall_EasyOCR_init=0
f_score_EasyOCR_init=0

precision_EasyOCR_fin=0
recall_EasyOCR_fin=0
f_score_EasyOCR_fin=0


results_list:List[Any]=[]
counter = 0
script_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/script.rtf'

# Open CSV file to write results
csv_file_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/OCR_results.csv'
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write header
    csv_writer.writerow(['Title', 'Extracted Words'])

    with open(script_path, "rt") as myfile:
        for line in myfile:
            
            if (counter >= 40):
                break
            counter +=1


            #print(line)
            index = line.find("=")
            #print (line[:index])
            #print(line[index+1:])

            title = line[:index]
            manuscript = line[index+1:]
            print(title)

            #Image Threshold
            origin = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/common/Images/raw_images/'
            IMAGE_PATH = origin + title + '.png'
            result = easyOCR_extract(IMAGE_PATH)

            # img_bgr = cv2.imread(IMAGE_PATH)
            # img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

            # result = reader.readtext(img_rgb, detail = 0, paragraph=True)
            # result = " ".join(result)

            
            precision, recall, f_score = precision_recall(manuscript, result)

            print("Before dictionnaries filtration: ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)

            precision_EasyOCR_init+= precision
            recall_EasyOCR_init+= recall
            f_score_EasyOCR_init+= f_score

            lst_result = result.split(" ")

            #for item in lst_result:
            #   item.lower()
            min_list=[]

            for item in lst_result:
                min_list.append(item.lower())


            #results_list +=lst_result
            print(min_list)
            min_list_check = special_caracters_remove(min_list)
            print(min_list_check)
            min_list_checked = real_words_check_nested(min_list_check, letter_dict)

            print("Liste des mots extraits aprés filtrage: ", min_list_checked)
            
            min_string_checked = " ".join(min_list_checked)

            precision, recall, f_score = precision_recall(manuscript, min_string_checked)
            print("After dictionnaries filtration ")
            print("Precision: ", precision, "recall: ", recall, "f_score: ", f_score)

            precision_EasyOCR_fin+= precision
            recall_EasyOCR_fin+= recall
            f_score_EasyOCR_fin+=f_score

            # Write to CSV
            csv_writer.writerow([title, min_string_checked])

            print("\n\n")

print("Results:")
print("Number of processed images: ", counter)
print()
print("Before dictionary filtration")
print("Averages are : precision: ", (precision_EasyOCR_init/counter), "recall: ", (recall_EasyOCR_init/counter), "f_score: ",(f_score_EasyOCR_init/counter))

print("After dictionary filtration")
print("Averages are : precision: ", (precision_EasyOCR_fin/counter), "recall: ", (recall_EasyOCR_fin/counter), "f_score: ",(f_score_EasyOCR_fin/counter))
