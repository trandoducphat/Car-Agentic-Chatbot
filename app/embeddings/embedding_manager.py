import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from langchain_core.documents import Document
from app.config.settings import DATA_DIR, EMBEDDINGS_DIR
from app.embeddings.document_loader import JSONLoader, load_policy_as_documents
from typing import List, Dict, Any, Tuple
import re
from sentence_transformers import SentenceTransformer
import numpy as np


###PROD_DOCS
prod_loader = JSONLoader(DATA_DIR/"raw"/"product.json")
PROD_DOCS = prod_loader.load()


###POL_DOCS
policy_filepath = DATA_DIR/"raw"/"customer_policy.txt"
POL_DOCS = load_policy_as_documents(policy_filepath)

###DICT INDEX FOR PRODUCTS
PROD_IDX = {p.metadata["brand"] + " " + p.metadata["model"]: p for p in PROD_DOCS}

###Class Embeddings
class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Model loaded successfully. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Error when loading model {self.model_name}: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not self.model:
            raise ValueError("Model is not available!")
        print(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"Generated embeddings with shape: {embeddings.shape}")
        return embeddings