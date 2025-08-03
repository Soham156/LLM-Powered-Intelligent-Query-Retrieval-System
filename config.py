"""
Configuration settings for the LLM-Powered Query-Retrieval System
"""
import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # API Configuration
    API_KEY = os.getenv("API_KEY", "f7d45b808bec922345421d7ed8051230ee8a696d8d37fe10e543bec6cf691c53")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.1))
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", 384))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.3))
    
    # Processing Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    MAX_CHUNKS_PER_QUERY = int(os.getenv("MAX_CHUNKS_PER_QUERY", 8))
    
    # Timeout Configuration
    DOCUMENT_DOWNLOAD_TIMEOUT = int(os.getenv("DOCUMENT_DOWNLOAD_TIMEOUT", 30))
    LLM_REQUEST_TIMEOUT = int(os.getenv("LLM_REQUEST_TIMEOUT", 60))
    
    @classmethod
    def validate(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        
        if not cls.OPENAI_API_KEY:
            issues.append("OPENAI_API_KEY is required")
        
        if cls.VECTOR_DIMENSION <= 0:
            issues.append("VECTOR_DIMENSION must be positive")
        
        if not 0 <= cls.SIMILARITY_THRESHOLD <= 1:
            issues.append("SIMILARITY_THRESHOLD must be between 0 and 1")
        
        if not 0 <= cls.TEMPERATURE <= 2:
            issues.append("TEMPERATURE must be between 0 and 2")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'config': {
                'host': cls.HOST,
                'port': cls.PORT,
                'debug': cls.DEBUG,
                'llm_model': cls.LLM_MODEL,
                'embedding_model': cls.EMBEDDING_MODEL,
                'vector_dimension': cls.VECTOR_DIMENSION,
                'similarity_threshold': cls.SIMILARITY_THRESHOLD
            }
        }
