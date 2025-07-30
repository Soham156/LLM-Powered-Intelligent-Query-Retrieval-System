from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass
import logging

from services.document_processor import DocumentProcessor
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService
from services.query_processor import QueryProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM-Powered Intelligent Query-Retrieval System",
    description="An intelligent document analysis system for insurance, legal, HR, and compliance domains",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
API_KEY = os.getenv("API_KEY", "f7d45b808bec922345421d7ed8051230ee8a696d8d37fe10e543bec6cf691c53")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Request/Response Models
class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# Initialize services
try:
    document_processor = DocumentProcessor()
    embedding_service = EmbeddingService()
    llm_service = LLMService()
    query_processor = QueryProcessor(document_processor, embedding_service, llm_service)
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {str(e)}")
    # Create placeholder services for startup
    document_processor = None
    embedding_service = None
    llm_service = None
    query_processor = None

@app.on_event("startup")
async def startup_event():
    """Validate configuration and test services on startup."""
    try:
        logger.info("Starting up LLM-Powered Query-Retrieval System...")
        
        # Validate configuration
        from config import Config
        validation = Config.validate()
        
        if not validation['valid']:
            logger.warning(f"Configuration issues: {validation['issues']}")
        else:
            logger.info("Configuration validation passed")
        
        logger.info("System startup completed")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "LLM-Powered Intelligent Query-Retrieval System is running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "main": "/api/v1/hackrx/run",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def process_queries(
    request: QueryRequest,
    token: str = Depends(verify_token)
):
    """
    Process documents and answer questions using intelligent retrieval and LLM analysis.
    
    This endpoint:
    1. Downloads and processes the document from the provided URL
    2. Creates embeddings for semantic search
    3. Processes each question through clause matching
    4. Generates structured responses using LLM reasoning
    """
    try:
        # Check if services are initialized
        if query_processor is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Services not properly initialized. Please check configuration."
            )
        
        logger.info(f"Processing request with {len(request.questions)} questions")
        logger.info(f"Document URL: {request.documents}")
        
        # Process the document and questions
        answers = await query_processor.process_queries(
            document_url=request.documents,
            questions=request.questions
        )
        
        logger.info(f"Successfully processed {len(answers)} answers")
        
        return QueryResponse(answers=answers)
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
