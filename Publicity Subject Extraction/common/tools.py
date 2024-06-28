



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
                print("This  word doesn't exist", mot)
                copy_list[word_index]= ""
            
    while("" in copy_list):
        copy_list.remove("")

    return copy_list

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


#Precision Recall fonction --> Needs Revision

def precision_recall(manuscripted_image, result):
    T_P = 0
    T_N = 0
    F_P = 0
    F_N = 0
    F_N2 = 0


    lst_manuscripted_image = manuscripted_image.split(" ")
    lst_result = result.split(" ")

    #all rslt to minuscule

    aux_rslt_lst = []
    for item in lst_result:
         aux_rslt_lst.append(item.lower())
    lst_result = aux_rslt_lst

    #all manuscript to minuscule
    aux_manus_lst = []
    for item in lst_manuscripted_image:
            aux_manus_lst.append(item.lower())
    lst_manuscripted_image = aux_manus_lst
    

    lst_manuscripted_image = special_caracters_remove(lst_manuscripted_image)


    

    l = len(lst_manuscripted_image)
    ll = len(lst_manuscripted_image[l-1])
    b = lst_manuscripted_image[l-1][:ll-1]

   # print(b, l, ll, len(b))
    lst_manuscripted_image = lst_manuscripted_image[:l-1]
    lst_manuscripted_image.append(b)
    print(lst_manuscripted_image)

    print("Liste des mots du manusript: ", lst_manuscripted_image)
    print("Liste des mots extraits: ", lst_result)
    #print("Longueur du manuscript: ", len(lst_manuscripted_image))
    #print("Longueur du result: ", len(lst_result))


    for word in lst_result:
        if (word in lst_manuscripted_image):
            T_P += 1
            #print("the word ", word ,"is in the manuscripted image")
            #print("T_P: ", T_P)
        else:
            #Check out for upperCase
            #check out for duplicates
            F_P += 1
            #print("the word ", word ,"is not in the manuscripted image")
            #print("F_P: ", F_P)
    #print("T_P: ", T_P)
    #print("F_P: ", F_P)
    precision = T_P/(T_P+F_P)


    for word in lst_manuscripted_image:
            if (word not in lst_result):
                F_N2 += 1
                #print("the word ", word ,"is not in the result")
                #print("F_N2: ", F_N2)

    F_N = len(lst_manuscripted_image) - T_P

    recall = T_P/(T_P+F_N)

    f_score = (2*precision*recall)/(precision+recall)


    return precision, recall, f_score,
                    