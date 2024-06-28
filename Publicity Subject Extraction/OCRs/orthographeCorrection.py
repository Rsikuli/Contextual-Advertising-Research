
from easyOCRTextExtraction import easyOCR_extract
from common.tools import precision_recall, real_words_check_nested, special_caracters_remove
from typing import List, Any
from common.dictionariesCreation import letter_dict #type: ignore



#Easy0CR_results_list

precision_EasyOCR_init=0
recall_EasyOCR_init=0
f_score_EasyOCR_init=0

precision_EasyOCR_fin=0
recall_EasyOCR_fin=0
f_score_EasyOCR_fin=0


results_list:List[Any]=[]
counter = 0

with open("new_script.rtf", "rt") as myfile:
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
        origin = '/Users/ramisafi/Desktop/Research Journal Project/Publicity Subject Extraction/common/Images/raw_images'
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






        print("\n\n")

print("Before dictionary filtration")
print("Averages are : precision: ", (precision_EasyOCR_init/counter), "recall: ", (recall_EasyOCR_init/counter), "f_score: ",(f_score_EasyOCR_init/counter))

print("After dictionary filtration")
print("Averages are : precision: ", (precision_EasyOCR_fin/counter), "recall: ", (recall_EasyOCR_fin/counter), "f_score: ",(f_score_EasyOCR_fin/counter))

