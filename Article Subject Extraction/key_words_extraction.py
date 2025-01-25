import sys
import os
import csv
from transformers import pipeline
import spacy


# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load the pipeline for token classification with yanekyuk
pipe_yanekyuk = pipeline("token-classification", model="yanekyuk/camembert-keyword-extractor")

# Function to check if a string is alphanumeric
def is_alphanumeric(word):
    return word.isalnum()



# # Load the French language model
# nlp = spacy.load("fr_core_news_sm")

# def lemmatize_text(text):
#     doc = nlp(text)
#     return " ".join([token.lemma_ for token in doc if not token.is_stop])

# text = "licate putation ift ike Jon 2016 Ken ake len Calvin Harris Tom les ton Joe ift Gra Elizabeth Hur ley Gra Elizabeth Hur ley Divin Brown Gra 1995 Anna ber stein ing lan Hong Paul New man Whi ney Houston Bob Kri"
# lemmatized_text = lemmatize_text(text)
# print(lemmatized_text)  # Output: "ce être exemple montrer mot inutile"




# Function to extract keywords using the pipeline and filter for B-KEY and I-KEY
# Function to extract keywords using the pipeline and filter for B-KEY and I-KEY
def extract_keywords_v2(text):
    """
    Extracts keywords from the given text using the specified pipeline.

    This function processes the input text through a provided NLP pipeline to identify and extract keywords.
    It filters out words that are less than 3 characters long and only includes words labeled as 'B-KEY' or 'I-KEY'.

    Args:
        text (str): The input text from which to extract keywords.
        pipeline (callable): A callable NLP pipeline that processes the text and returns a list of entities.

    Returns:
        str: A comma-separated string of extracted keywords.
    """
    pipeline = pipe_yanekyuk
    results = pipeline(text)

    keywords = []
    current_keyword = ""

    for item in results:
        label = item['entity']
        word = item['word']

        # Process only B-KEY and I-KEY labels
        if label in ['B-KEY', 'I-KEY']:
            if label == 'B-KEY':
                # Remove the '▁' marker at the start of words
                if word.startswith('▁'):
                    word = word[1:]
                # If it's a new keyword, add the previous keyword to the list
                if current_keyword:
                    keywords.append(current_keyword)
                current_keyword = word  # Start a new keyword

            elif label == 'I-KEY':
                if word.startswith('▁'):
                    word = word[1:]
                    # Means a new word in the same keyword
                    current_keyword = current_keyword + " " + word
                else:
                    current_keyword = current_keyword + word

        else:
            # Add the completed keyword to the list and reset
            if current_keyword:
                keywords.append(current_keyword)
                current_keyword = ""

    # Add the last keyword if it exists
    if current_keyword:
        keywords.append(current_keyword)

    return ', '.join(keywords)



strin_2 = "Dans un pays quotidiennement meurtri par les fusillades et où les armes à feu prolifèrent, le président américain a annoncé avoir promis à la gouverneure démocrate de l’État du Michigan (nord) Gretchen Whitmer des effectifs supplémentaires de forces de l’ordre fédérales après qu’un tireur eut tué lundi soir trois étudiants et blessé cinq autres, avant de se suicider, sur le campus de l’Université d’État du Michigan (MSU). Lors d’une conférence de presse chargée en émotions, à Lansing, capitale de cet État des Grands Lacs frontalier du Canada, les autorités ont confirmé la mort de trois personnes et les graves blessures infligées par balles à cinq autres, lors d’une soirée cauchemardesque. Toutes ces victimes étaient des étudiants de MSU, a indiqué Chris Rozman, un des chefs de la police de cette université, l’une des plus prestigieuses du pays avec quelque 50 000 élèves. L’agent a précisé que le suspect de 43 ans, prénommé Anthony McRae, avait été retrouvé mort par balle sur place lundi vers minuit, qu’il n’avait aucune affiliation avec l’université, ni un étudiant, ni un employé de la faculté, aujourd’hui ou par le passé. Problème américain Lors de ce point de presse où des responsables ont fondu en larmes, la gouverneure Whitmer, très émue, a dénoncé un nouveau lieu du vivre-ensemble brisé par les balles et l’effusion de sang. Nous savons que c’est uniquement un problème américain (...) Nous ne pouvons pas continuer à vivre ainsi, a fustigé la dirigeante du Michigan. Le président Biden a enfoncé le clou dans deux communiqués successifs de la Maison-Blanche. Trop de communautés américaines ont été anéanties par la violence par arme à feu, a-t-il tonné, une nouvelle fois. J’ai agi pour combattre cette épidémie en Amérique, notamment par un nombre historique de décrets et la première loi de sécurité sur les armes à feu en 30 ans (...) Mais nous devons faire plus, a-t-il reconnu en rendant hommage à 17 jeunes et éducateurs tués à l’arme à feu dans un lycée à Parkland en Floride le 14 février 2018. Tous les Américains devraient s’exclamer +assez+ et exiger du Congrès qu’il agisse, a martelé le dirigeant démocrate de 80 ans. Avancées timides Malgré des avancées timides, Joe Biden réclame, en vain, au Congrès de rétablir l’interdiction nationale des fusils d’assaut, telle qu’elle existait de 1994 et 2004, mais il bute sur les républicains, lesquels se posent en défenseurs du droit constitutionnel à détenir des armes et qui ont une courte majorité depuis janvier à la Chambre des représentants. Le tireur de MSU a ouvert le feu lundi vers 20H30 dans un bâtiment de l’université, avant de se diriger vers un autre bâtiment où des coups de feu ont également été entendus, selon la police du campus. Je n’oublierai jamais les cris de mes camarades de classe, des cris de douleur pour appeler à l’aide, a témoigné dans la presse locale l’étudiante Claire Papoulias, qui s’est jetée à terre pour échapper aux balles du tueur surgissant dans une salle de cours. Vite arrivés, des centaines de membres des forces de l’ordre s’étaient lancés dans une chasse à l’homme en diffusant aussitôt des photos du suspect: un homme noir de petite taille portant une veste en jean, des chaussures rouges, une casquette de baseball et le visage à moitié dissimulé. Le policier Rozman s’est félicité de la réactivité des résidents du campus. Grâce à la publication rapide de la photo tirée des caméras de surveillance et (...) un tuyau de quelqu’un qui a appelé, (cela) a conduit les forces de l’ordre vers le suspect, a-t-il remercié, tout en disant n’avoir aucune idée du mobile de ses crimes. Les États-Unis paient un très lourd tribut à la dissémination des armes à feu sur leur territoire et à la facilité avec laquelle les Américains y ont accès. Le pays compte davantage d’armes individuelles que d’habitants, soit environ 400 millions: un adulte sur trois possède au moins une arme et près d’un adulte sur deux vit dans un foyer où se trouve une arme. La conséquence de cette prolifération est le taux très élevé de décès par arme à feu aux États-Unis, près de 50.000, dont la moitié environ sont des suicides."

# # Test the keyword extraction function
keys = extract_keywords_v2(strin_2)
print(keys)









# Read the CSV file
input_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/processed_results.csv'
output_csv_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

with open(input_csv_path, mode='r', encoding='utf-8') as infile, open(output_csv_path, mode='w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['Headline', 'Caption', 'Subheadline', 'Summary', 'Keywords']  # Specify output fields
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        paragraph = row['Paragraph']
        keywords = extract_keywords_v2(paragraph)
        
        # Get other fields safely
        caption = row.get('Caption', '')
        headline = row.get('Headline', '')
        subheadline = row.get('Subheadline', '')
        summary = row.get('Summary', '')

        # Write only the processed data to the output file
        writer.writerow({
            'Headline': headline,
            'Caption': caption,
            'Subheadline': subheadline,
            'Summary': summary,
            'Keywords': keywords
        })

print("Keywords extraction and CSV update completed.")





