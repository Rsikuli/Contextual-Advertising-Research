
import cv2
from typing import Dict

#addDictionnary definition
# Dictionary to store words by their first letter
letter_dict :Dict[str,Dict]= {
    'a': {}, 'b': {}, 'c': {}, 'd': {}, 'e': {},
    'f': {}, 'g': {}, 'h': {}, 'i': {}, 'j': {},
    'k': {}, 'l': {}, 'm': {}, 'n': {}, 'o': {},
    'p': {}, 'q': {}, 'r': {}, 's': {}, 't': {},
    'u': {}, 'v': {}, 'w': {}, 'x': {}, 'y': {}, 'z': {}
}

#UpperCase to LowerCase List --> lowerList(UPlist)
def lowerList(UPlist):
    lowList = []
    for mot in UPlist:
        lowList.append(mot.lower())
    return lowList


#Special caracters recognition 1

# need revision: you have to check out how you dealt  with duplicate special caracters 
special_caracters =["*", ",", ";", ":", ".", "-", "?", "!", "'", "$"]

def special_caracters_remove(min_list):
    for mot in min_list:
        word_index = min_list.index(mot)
        for sp_char in special_caracters:
            
            found = sp_char in mot
            if found:

                #print("oui")
                #try:
                
                #except ValueError as ve:
                #    break
                index=mot.index(sp_char)
            
                if index == 0 or index == len(mot) - 1:
                    
                    min_list[word_index] = mot.replace(sp_char, "")
                    #print("the word ", mot, "is replaced by ", mot[:index])
                    

                else:
                    min_list[word_index] = mot[:index]
                    #print("the word ", mot, "is replaced by ", mot[:index])
                    min_list.insert(word_index+1, mot[index+1:])
                    #print("the word ", mot, "is replaced by ", mot[index+1:])
                

    while("" in min_list):
        min_list.remove("")
    
    #print("lists special caracters has been removed")
    #print(min_list)
    return min_list


# Function to add words to the dictionary based on their first letter
def addDictionary(mot):
    first_letter = mot[0]
    
    if first_letter.isalpha():
        dictoch = {'a':['ä', 'á', 'à', 'æ', 'â', 'å'], 'e':['é', 'è', 'ê', 'ë'], 'i':['î', 'ï', 'í'], 'u':['ù', 'ü', 'û'], 'o':['ð', 'œ', 'ô', 'ö', 'õ', 'ø', 'ó'], 'c':['ç'], 'b':['ß'], 'n':['ñ']}
        #build a dictionnary for with key as the right letter and the values as all the other mutations this letter can take  
        if first_letter in ('ä', 'á', 'à', 'æ', 'â', 'å'):
            first_letter = 'a'
        if first_letter in ('é', 'è', 'ê', 'ë'):
            first_letter = 'e'
        if first_letter in ('î', 'ï', 'í'):
            first_letter = 'i'
        if first_letter in ('ù', 'ü', 'û'):
            first_letter = 'u'
        if first_letter in ('ç'):
            first_letter = 'c'
        if first_letter in ('ð', 'œ', 'ô', 'ö', 'õ', 'ø', 'ó'):
            first_letter = 'o'
        if first_letter in ('ß'):
            first_letter = 'b'
        if first_letter in ('ñ'):
            first_letter = 'n'
        if mot not in letter_dict[first_letter]:
            letter_dict[first_letter][mot] = 0
            print(f"'{mot}' is successfully added to the dictionary: {first_letter}")
        else:
            pass
            #print(f"'{mot}' is already in the dictionary.")
    else:
        mot2 = mot[1:len(mot)-1]
        if len(mot2) >2:
            first_letter = mot2[0]
            if first_letter in ('ä', 'á', 'à', 'æ', 'â', 'å'):
                first_letter = 'a'
            if first_letter in ('é', 'è', 'ê', 'ë'):
                first_letter = 'e'
            if first_letter in ('î', 'ï', 'í'):
                first_letter = 'i'
            if first_letter in ('ù', 'ü', 'û'):
                first_letter = 'u'
            if first_letter in ('ç'):
                first_letter = 'c'
            if first_letter in ('ß'):
                first_letter = 'b'
            if first_letter in ('ð', 'œ', 'ô', 'ö', 'õ', 'ø', 'ó'):
                first_letter = 'o'
            if first_letter in ('ñ'):
                first_letter = 'n'
            if first_letter.isalpha():
                if mot2 not in letter_dict[first_letter]:
                    letter_dict[first_letter][mot2] = 0
                    print(f"'{mot2}' is successfully added to the dictionary: {first_letter}")
                else:
                    pass
                    #print(f"'{mot2}' is already in the dictionary.")
        
        else:
            print(f"'{mot}' can't be added")


#create the nested dictionnaries 

with open("/Users/ramisafi/Desktop/Research Journal Project/Publicity Subject Extraction/common/Dictionnaries/Lst_Scr_min_sans_accent.txt", "rt") as myfile:
    for line in myfile:

        #index = line.find("=")
        #title = line[:index]
        #manuscript = line[index+1:]

        mot = line[:len(line)-1].lstrip()
        addDictionary(mot)
        


with open("/Users/ramisafi/Desktop/Research Journal Project/Publicity Subject Extraction/common/Dictionnaries/Nom.csv", 'r') as csvfile:
    lines = csvfile.readlines()
    for line in lines:
        data = line.strip().split(',')
        if len(data) > 1:  # Ensure there is at least a second element after splitting
            second_element = data[1]
            #print(second_element)
            if not second_element[:3].isnumeric():
                if len(second_element)>1:
                    
                    lstUP = second_element.split(' ')
                    #print(lstUP)
                    lst = lowerList(lstUP)
                    finalList = special_caracters_remove(lst)
                    
                    #print(finalList)
                    for item in finalList:
                        if len(item)>1:
                            addDictionary(item)
                    


#Custom Addition to dictionary
addition = ["hyundai", "hhyundai", "kona", "publicité", "tucson", "coops", "fierté",
             "incluant", "desjardins", "routière", "initiative", "inscrivez", "québec",
               "sécurité", "musée", "redessiné", "quebec", "débutez", "goûtez", "l", "prévention",
                 "débardeurs", "c'est", "société", "s'en", "scfr", "jusqu'à", "régulier", "modèles",
                   "sélectionnés", "apéros", "broadway", "mazda", "cx-5", "intégrale", "série", "québécoise",
                     "présentent", "l'information", "dès", "journées", "côtés", "derrière", "résidence", "complète",
                       "réalisàtion", "bien", "véhicules", "sans-frais", "blancs", "biologique", "biologiques"]

for mot in addition:
    addDictionary(mot)




