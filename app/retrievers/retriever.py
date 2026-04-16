import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.embeddings.embedding_manager import EmbeddingManager
from app.retrievers.vector_store import VectorStore
from typing import List, Dict, Any, Tuple


# class RAGRetriever:
#     def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
#         self.vector_store = vector_store
#         self.embedding_manager = embedding_manager
    
#     def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
#         print(f"Retrieving documents for query: {query}")
#         print(f"Top k: {top_k}, Score threshold: {score_threshold}")

#         query_embedding = self.embedding_manager.generate_embeddings([query])[0]
#         try:
#             results = self.vector_store.collection.query(
#                 query_embeddings=[query_embedding.tolist()],
#                 n_results=top_k
#             )
#             retrieved_docs = []
            
#             if results['documents'] and results['documents'][0]:
#                 documents = results['documents'][0]
#                 metadatas = results['metadatas'][0]
#                 distances = results['distances'][0]
#                 ids = results['ids'][0]

#                 for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
#                     similarity_score = 1 - distance
#                     if similarity_score >= score_threshold:
#                         retrieved_docs.append({
#                             'id': doc_id,
#                             'content': document,
#                             'metadata': metadata,
#                             'similarity_score': similarity_score,
#                             'distance': distance,
#                             'rank': i + 1
#                         })
#                 print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
            
#             else:
#                 print("No documents found")
#             return retrieved_docs
#         except Exception as e:
#             print(f"Error during retrieval: {e}")
#             return []

class RAGRetriever:
    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def _normalize(self, text: str) -> str:
        return text.lower().replace(" ", "").strip()

    def _keyword_filter(self, query: str, documents: List[Dict[str, Any]]):
        query_norm = self._normalize(query)

        filtered = []
        for doc in documents:
            content = self._normalize(doc.get("content", ""))
            metadata = doc.get("metadata", {})

            if query_norm in content:
                filtered.append(doc)
                continue

            for v in metadata.values():
                if isinstance(v, str) and query_norm in self._normalize(v):
                    filtered.append(doc)
                    break

        return filtered if filtered else documents

    def _vector_search(self, query_embedding, top_k):
        results = self.vector_store.collection.query(query_embeddings=[query_embedding.tolist()], n_results=top_k)

        docs = []
        if not results["documents"] or not results["documents"][0]:
            return docs

        for i in range(len(results["documents"][0])):
            distance = results["distances"][0][i]
            docs.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": distance,
                "score": 1 - distance,
                "rank": i + 1
            })

        return docs

    def retrieve(self, query: str, top_k: int = 3, score_threshold: float = 0.0) -> List[Dict[str, Any]]:

        query_embedding = self.embedding_manager.generate_embeddings([query])[0]

        raw_results = self._vector_search(query_embedding, top_k * 5)

        if not raw_results:
            return []

        filtered = self._keyword_filter(query, raw_results)

        final_docs = [d for d in filtered if d["score"] >= score_threshold]

        final_docs.sort(key=lambda x: x["score"], reverse=True)

        return final_docs[:top_k]
        
