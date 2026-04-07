from typing import List
from sentence_transformers import SentenceTransformer

class Embedder: 
    #convert text chunks into vector embeddings using pretrained model

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        #loads pretrained embedding model
    def embed_texts(self, texts):
        #should take ["hello", "my name is", "aditya tiwari"] and turn into vector representation [ [0.12, -0.06, ...], [0.08, 0.15, ...], ... ]
        #generate embeddings for list of input texts, can compare query vectors later to these chunk vectors
        embed = self.model.encode(texts, show_progress_bar=True)
        return embed.tolist()
    