# Initialize tools

import unicodedata
import re

def remove_numbers(word):
    return re.sub(r'\d+', '', word)



def real_words_check_nested(min_list, letter_dict):

    for mot  in min_list:
        
        word_index = min_list.index(mot)
        copy_list = min_list
        first_letter = mot[0]
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
        if first_letter in ('ð', 'œ', 'ô', 'ö', 'õ', 'ø'):
            first_letter = 'o'
        if first_letter in ('ñ'):
            first_letter = 'n'
        if first_letter.isalpha():
            state = letter_dict[first_letter].get(mot)
            if state is None:
                #print("This word doesn't exist", mot)

                copy_list[word_index]= ""
            
    while("" in copy_list):
        copy_list.remove("")

    return copy_list





def remove_special_characters(word_list):
    # Define the regex pattern for special characters
    special_characters_pattern = r"[*,;:\.\-\?!'%$&@#^()\[\]{}<>|_/\\~`\"]"
    
    # # Function to remove numbers from a word
    # def remove_numbers(word):
    #     return re.sub(r'\d+', '', word)
    
    # Create a new list to hold the cleaned words
    cleaned_list = []
    
    for word in word_list:
        # Remove numbers first
        #word_no_numbers = remove_numbers(word)
        
        # Split the word by any special character
        parts = re.split(special_characters_pattern, word)
        
        # Filter out empty strings and extend the cleaned list with valid parts
        cleaned_list.extend(filter(None, parts))
    
    return cleaned_list



def precision_recall(manuscripted_image, result):
    # Split strings into word lists
    lst_manuscripted_image = manuscripted_image.split()
    lst_result = result.split()

    # Print the input lists for debugging
    print("Liste des mots du manuscrit :", lst_manuscripted_image)
    print("Liste des mots extraits :", lst_result)

    # Convert lists to sets to eliminate duplicates and allow for direct comparison
    set_manuscript = set(lst_manuscripted_image)
    set_result = set(lst_result)

    # Calculate true positives, false positives, and false negatives
    T_P = len(set_result & set_manuscript)  # Intersection of both sets
    F_P = len(set_result - set_manuscript)  # Words in result but not in manuscript
    F_N = len(set_manuscript - set_result)  # Words in manuscript but not in result

    # Compute precision, recall, and F-score with safeguards against division by zero
    precision = T_P / (T_P + F_P) if (T_P + F_P) > 0 else 0
    recall = T_P / (T_P + F_N) if (T_P + F_N) > 0 else 0
    f_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f_score



def normalize_word(word):
    # Remove accents for comparison
    return ''.join(
        c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn'
    )



def fuse_ocr_results(easyocr_list, paddleocr_list):
    # Normalize EasyOCR words
    normalized_easyocr = {normalize_word(word): word for word in easyocr_list}

    # Build the fusion list with EasyOCR words as priority
    fusion_list = easyocr_list.copy()
    for word in paddleocr_list:
        normalized_word = normalize_word(word)
        if normalized_word not in normalized_easyocr:
            # Add only words not already represented in EasyOCR
            fusion_list.append(word)

    return fusion_list


