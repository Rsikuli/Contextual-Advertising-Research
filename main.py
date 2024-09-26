from Publicity_Subject_Extraction.ImageClassification.BlipProcessor import blipProcessorImgClassify


import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

all_blip_classification = []
counter = 0

with open("/Users/ramisafi/Desktop/Research Journal Project/Publicity_Subject_Extraction/common/scripts/new_script.rtf", "rt") as myfile:
    for line in myfile:
        
        if (counter >= 10):
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
        origin = '/Users/ramisafi/Desktop/Research/images/'
        IMAGE_PATH = origin + title + '.png'
        image_classification = blipProcessorImgClassify(IMAGE_PATH)
        print(image_classification)
        all_blip_classification.append(image_classification)

queries = ["un gros plan d'une voiture garée sur une rue avec une légende en français", "un gros plan d'une affiche avec une femme assise à une table", "un gros plan d'un panneau avec une planche de surf dessus", "un gros plan d'une couverture de livre jaune avec une image en noir et blanc", "il y a une affiche avec une photo d'un homme sur un skateboard","Arafed publicité pour un nouveau spectacle de voiture avec une femme debout à côté de lui", "un gros plan d'une voiture qui descend une route près d'un bois", "une affiche avec une photo d'un navire et une légende des mots", "une affiche rouge avec un texte blanc qui lit vos réseaux pas tout seul sur la route", "une affiche pourpre avec un texte blanc qui lit, vos netes pas tout seu sur la route"]


# Initialize the Sentence Transformer model with CamemBERT
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# model = SentenceTransformer("intfloat/multilingual-e5-base")
# Data to index (sample data in French)
data = [
    "Selon un sondage mené par l’Association canadienne des automobilistes (CAA ou Canadian Automobile Association), les deux tiers des Canadiens ignorent ce qu’il en coûte vraiment de posséder un véhicule.",
    "Un «tout-inclus» à 45 $ par jour pour une famille de quatre personnes. Une fois sur place, vous serez presque seul sur la plage de sable blanc, à observer les pêcheurs dans leurs embarcations rustiques et à écouter les vagues de la mer de Chine méridionale."
]

# Generate embeddings 
#  each piece of data
embeddings = np.array(model.encode(data))

# Number of dimensions for the embeddings
dim = embeddings.shape[1]
# Create a FAISS index (L2 distance)
index = faiss.IndexFlatL2(dim)
index.add(embeddings)  # Add embeddings to index
print("dimensions: " + str(dim))
# Queries to search (in French)

query_embeddings = np.array(model.encode(queries))

# Exemple d'utilisation avec plusieurs articles et publicités

# Output formatting
print("%-20s %s" % ("Query", "Best Match"))
print("-" * 50)

# Search the index
for i, query in enumerate(queries):
    # Perform search
    D, I = index.search(np.array([query_embeddings[i]]), 5)
    # print(D)
    # print(I)
      # Search for the top 1 closest vector
    if len(I[0]) > 0:
        best_match = data[I[0][0]]
        # print("%-20s %s" % (query, best_match))
        print(query)
        print(best_match)
        # print(I[0][0])
        print(D[0][0])
        # print(I[0])
        # print(D[0])
        print("-----")
    else:
        print("%-20s %s" % (query, "No match found"))
