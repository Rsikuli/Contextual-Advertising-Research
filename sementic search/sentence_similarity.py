import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Initialize the Sentence Transformer model with CamemBERT
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# File paths for various datasets
ocr_results_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/OCR_results.csv'
blip_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/Blip_results.csv'
sam_vit_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/SAM&Vit_results.csv'
fusion_path = ''

article_subjects_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

# Check if the files exist
if not os.path.exists(article_subjects_path):
    raise FileNotFoundError(f"File not found: {article_subjects_path}")
if not os.path.exists(ocr_results_path):
    raise FileNotFoundError(f"File not found: {ocr_results_path}")

# Read the CSV files
article_subjects_df = pd.read_csv(article_subjects_path)
ocr_results_df = pd.read_csv(ocr_results_path)

# Extract the relevant columns
data = article_subjects_df['Headline'].tolist()
queries = ocr_results_df['Extracted Words'].tolist()

# Generate embeddings for each piece of data
embeddings = np.array(model.encode(data))

# Number of dimensions for the embeddings
dim = embeddings.shape[1]

# Create a FAISS index (L2 distance)
index = faiss.IndexFlatL2(dim)
index.add(embeddings)  # Add embeddings to index
print("dimensions: " + str(dim))

# Generate embeddings for the queries
query_embeddings = np.array(model.encode(queries))

# Output formatting
print("%-20s %s" % ("Query", "Best Match"))
print("-" * 50)

# Search the index
for i, query in enumerate(queries):
    # Perform search for the top 5 closest vectors
    distances, indices = index.search(np.array([query_embeddings[i]]), 5)
    
    # Display results
    print(f"Query: '{query}'\n")
    for j in range(5):
        print(f"Match {j+1}: '{data[indices[0][j]]}' (Distance: {distances[0][j]:.4f})")
    print("-----")

# Open a text file to write the results
output_path = '/Users/ramisafi/Downloads/Research Journal Project/sementic search/results.txt'
with open(output_path, 'w') as file:
    file.write("Semantic Search Results\n")
    file.write("=" * 50 + "\n")
    
    # Search the index and write results to the file
    for i, query in enumerate(queries):
        # Perform search for the top 5 closest vectors
        distances, indices = index.search(np.array([query_embeddings[i]]), 5)
        
        # Write query to the file
        file.write(f"Query: '{query}'\n")
        for j in range(5):
            file.write(f"Match {j+1}: '{data[indices[0][j]]}' (Distance: {distances[0][j]:.4f})\n")
        file.write("-----\n")
    
    print(f"Results saved to {output_path}")

