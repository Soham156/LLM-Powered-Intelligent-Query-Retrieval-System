import os
import numpy as np
import faiss
import logging
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Handles text embeddings and vector similarity search using FAISS.
    Provides semantic search capabilities for document chunks.
    """
    
    def __init__(self):
        self.model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.vector_dimension = int(os.getenv("VECTOR_DIMENSION", "384"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        
        # Initialize the embedding model
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        
        # FAISS index will be created when needed
        self.index = None
        self.chunk_metadata = []
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Create embeddings for a list of texts."""
        try:
            logger.info(f"Creating embeddings for {len(texts)} texts")
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            logger.info(f"Created embeddings with shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise Exception(f"Failed to create embeddings: {str(e)}")
    
    def build_vector_index(self, chunks: List[Dict[str, Any]]) -> None:
        """Build FAISS index from document chunks."""
        try:
            logger.info(f"Building vector index for {len(chunks)} chunks")
            
            # Extract text from chunks
            texts = [chunk['text'] for chunk in chunks]
            
            # Create embeddings
            embeddings = self.create_embeddings(texts)
            
            # Ensure embeddings are float32 for FAISS
            embeddings = embeddings.astype('float32')
            
            # Create FAISS index
            self.index = faiss.IndexFlatIP(self.vector_dimension)  # Inner product for cosine similarity
            
            # Normalize vectors for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add embeddings to index
            self.index.add(embeddings)
            
            # Store chunk metadata
            self.chunk_metadata = chunks
            
            logger.info(f"Successfully built vector index with {self.index.ntotal} vectors")
            
        except Exception as e:
            logger.error(f"Error building vector index: {str(e)}")
            raise Exception(f"Failed to build vector index: {str(e)}")
    
    def search_similar_chunks(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for chunks most similar to the query.
        Returns ranked results with similarity scores.
        """
        try:
            if self.index is None:
                raise Exception("Vector index not built. Call build_vector_index first.")
            
            logger.info(f"Searching for similar chunks to query: {query[:100]}...")
            
            # Create query embedding
            query_embedding = self.create_embeddings([query])
            query_embedding = query_embedding.astype('float32')
            
            # Normalize for cosine similarity
            faiss.normalize_L2(query_embedding)
            
            # Search the index
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.chunk_metadata)))
            
            # Prepare results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.chunk_metadata):  # Valid index
                    chunk = self.chunk_metadata[idx].copy()
                    chunk['similarity_score'] = float(score)
                    chunk['rank'] = i + 1
                    results.append(chunk)
            
            # Filter by similarity threshold
            filtered_results = [r for r in results if r['similarity_score'] >= self.similarity_threshold]
            
            logger.info(f"Found {len(filtered_results)} relevant chunks above threshold {self.similarity_threshold}")
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error searching similar chunks: {str(e)}")
            raise Exception(f"Failed to search similar chunks: {str(e)}")
    
    def get_contextual_chunks(self, query: str, max_chunks: int = 10) -> str:
        """
        Get the most relevant chunks for a query and combine them into context.
        Returns combined text that can be used for LLM processing.
        """
        try:
            # Search for similar chunks
            similar_chunks = self.search_similar_chunks(query, top_k=max_chunks)
            
            if not similar_chunks:
                logger.warning(f"No relevant chunks found for query: {query[:100]}...")
                return ""
            
            # Combine chunks into context
            context_parts = []
            for i, chunk in enumerate(similar_chunks):
                context_parts.append(
                    f"[Chunk {i+1} - Similarity: {chunk['similarity_score']:.3f}]\n"
                    f"{chunk['text']}\n"
                )
            
            combined_context = "\n".join(context_parts)
            
            logger.info(f"Created context from {len(similar_chunks)} chunks, "
                       f"total length: {len(combined_context)} characters")
            
            return combined_context
            
        except Exception as e:
            logger.error(f"Error getting contextual chunks: {str(e)}")
            raise Exception(f"Failed to get contextual chunks: {str(e)}")
    
    def analyze_query_relevance(self, query: str) -> Dict[str, Any]:
        """
        Analyze how well the query matches the indexed content.
        Returns statistics about relevance and coverage.
        """
        try:
            # Get top chunks
            similar_chunks = self.search_similar_chunks(query, top_k=10)
            
            if not similar_chunks:
                return {
                    'has_relevant_content': False,
                    'max_similarity': 0.0,
                    'avg_similarity': 0.0,
                    'relevant_chunk_count': 0,
                    'confidence': 'low'
                }
            
            # Calculate statistics
            similarities = [chunk['similarity_score'] for chunk in similar_chunks]
            max_sim = max(similarities)
            avg_sim = sum(similarities) / len(similarities)
            relevant_count = len([s for s in similarities if s >= self.similarity_threshold])
            
            # Determine confidence level
            if max_sim >= 0.8 and relevant_count >= 3:
                confidence = 'high'
            elif max_sim >= 0.6 and relevant_count >= 2:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            return {
                'has_relevant_content': relevant_count > 0,
                'max_similarity': max_sim,
                'avg_similarity': avg_sim,
                'relevant_chunk_count': relevant_count,
                'confidence': confidence,
                'top_chunks': similar_chunks[:3]  # Top 3 for analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing query relevance: {str(e)}")
            return {
                'has_relevant_content': False,
                'max_similarity': 0.0,
                'avg_similarity': 0.0,
                'relevant_chunk_count': 0,
                'confidence': 'low',
                'error': str(e)
            }
