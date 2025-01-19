import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class SemanticSearch:
    """
    A class to perform semantic search using Sentence Transformers and FAISS.

    Attributes:
        model (SentenceTransformer): The sentence transformer model used for generating embeddings.
        publicity_representations (dict): Dictionary to store publicity representations.
        article_representations (dict): Dictionary to store article representations.
    """

    def __init__(self):
        """
        Initializes the SemanticSearch class with a pre-trained sentence transformer model.
        """
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
        self.publicity_representations = {}
        self.article_representations = {}

    def load_data(self):
        """
        Loads data from CSV files and populates the publicity and article representations.

        Raises:
            FileNotFoundError: If any of the required CSV files are not found.
        """
        # Define file paths
        ocr_results_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/OCRs/OCR_results.csv'
        blip_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/Blip_results.csv'
        sam_vit_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/ImageClassification/SAM&Vit_results.csv'
        fusion_path = '/Users/ramisafi/Downloads/Research Journal Project/Publicity_Subject_Extraction/fused_results.csv'
        article_subjects_path = '/Users/ramisafi/Downloads/Research Journal Project/Article Subject Extraction/results_with_keywords.csv'

        # Check if the files exist
        for path in [ocr_results_path, blip_path, sam_vit_path, fusion_path, article_subjects_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"File not found: {path}")

        # Read the CSV files for publicity representations
        ocr_results_df = pd.read_csv(ocr_results_path)
        sam_vit_df = pd.read_csv(sam_vit_path)
        blip_df = pd.read_csv(blip_path)
        fusion_df = pd.read_csv(fusion_path)

        # Read the CSV file for article subjects
        article_subjects_df = pd.read_csv(article_subjects_path)

        # Define representations for Publicity and Articles
        self.publicity_representations = {
            "OCR": ocr_results_df['Extracted Words'].tolist(),
            "SAM-ViT": sam_vit_df['Descriptions'].tolist(),
            "BLIP": blip_df['Description'].tolist(),
            "Fusion": fusion_df['Fused Content'].tolist()
        }

        self.article_representations = {
            "Headline": article_subjects_df['Headline'].tolist(),
            "Caption": article_subjects_df['Caption'].tolist(),
            "Keywords": article_subjects_df['Keywords'].tolist(),
            "Summary": article_subjects_df['Summary'].tolist()
        }

    def perform_search(self):
        """
        Performs semantic search by creating FAISS indices and cross-testing each combination of publicity and article representations.
        Results are saved to text files.
        """
        # Create the FAISS index and perform the 16 tests
        output_path = '/Users/ramisafi/Downloads/Research Journal Project/sementic search/results.txt'
        with open(output_path, 'w') as file:
            file.write("Semantic Search Results\n")
            file.write("=" * 50 + "\n")
            
            # Define the combinations to test
            combinations = [
                ("Headline", "OCR"),
                ("Headline", "BLIP"),
                ("Headline", "SAM-ViT"),
                ("Headline", "Fusion"),
                ("Caption", "OCR"),
                ("Caption", "BLIP"),
                ("Caption", "SAM-ViT"),
                ("Caption", "Fusion"),
                ("Keywords", "OCR"),
                ("Keywords", "BLIP"),
                ("Keywords", "SAM-ViT"),
                ("Keywords", "Fusion"),
                ("Summary", "OCR"),
                ("Summary", "BLIP"),
                ("Summary", "SAM-ViT"),
                ("Summary", "Fusion")
            ]
            # Create a base directory for the results
            base_results_dir = '/Users/ramisafi/Downloads/Research Journal Project/sementic search/similarity_results'
            if not os.path.exists(base_results_dir):
                os.makedirs(base_results_dir)

            # Cross-test each combination of Publicity and Article representation
            for art_repr, pub_repr in combinations:
                article_data = self.article_representations[art_repr]
                pub_data = self.publicity_representations[pub_repr]
            
                # Generate embeddings for publicity representations (FAISS index creation)
                pub_embeddings = np.array(self.model.encode(pub_data))
                
                dim = pub_embeddings.shape[1]
                index = faiss.IndexFlatL2(dim)
                index.add(pub_embeddings)  # Add publicity embeddings to index

                # Generate embeddings for the queries (article representations)
                query_embeddings = np.array(self.model.encode(article_data))

                # Create a directory for each article representation
                art_repr_dir = os.path.join(base_results_dir, art_repr)
                if not os.path.exists(art_repr_dir):
                    os.makedirs(art_repr_dir)

                # Create a separate file for each combination
                combination_output_path = os.path.join(art_repr_dir, f'results_{art_repr}_{pub_repr}.txt')
                with open(combination_output_path, 'w') as file:
                    file.write(f"Semantic Search Results for {art_repr} with {pub_repr}\n")
                    file.write("=" * 50 + "\n")

                    # Search and log results
                    for i, query in enumerate(query_embeddings):
                        distances, indices = index.search(np.array([query]), 5)

                        # Write query and its results
                        file.write(f"Query: '{article_data[i]}'\n")
                        for j in range(5):
                            file.write(f"Match {j+1}: '{pub_data[indices[0][j]]}' (Distance: {distances[0][j]:.4f})\n")
                        file.write("-----\n")
                
                print(f"Results saved to {combination_output_path}")

if __name__ == "__main__":
    search = SemanticSearch()
    search.load_data()
    search.perform_search()
