import logging
from typing import List, Dict, Any
import asyncio

from .document_processor import DocumentProcessor
from .embedding_service import EmbeddingService
from .llm_service import LLMService

logger = logging.getLogger(__name__)

class QueryProcessor:
    """
    Main orchestrator for the query processing pipeline.
    Coordinates document processing, embedding search, and LLM generation.
    """
    
    def __init__(self, document_processor: DocumentProcessor, 
                 embedding_service: EmbeddingService, 
                 llm_service: LLMService):
        self.document_processor = document_processor
        self.embedding_service = embedding_service
        self.llm_service = llm_service
        
        # Cache for processed documents
        self.document_cache = {}
        
        logger.info("Initialized QueryProcessor")
    
    async def process_queries(self, document_url: str, questions: List[str]) -> List[str]:
        """
        Main entry point for processing a document and answering questions.
        
        Pipeline:
        1. Download and process document
        2. Create embeddings and build vector index
        3. For each question:
           - Find relevant chunks using semantic search
           - Generate context for LLM
           - Get answer from LLM
        4. Return structured responses
        """
        try:
            logger.info(f"Starting query processing for {len(questions)} questions")
            
            # Step 1: Process document (with caching)
            document_data = await self._get_or_process_document(document_url)
            
            # Step 2: Build vector index if not already built
            if not hasattr(self.embedding_service, 'index') or self.embedding_service.index is None:
                self.embedding_service.build_vector_index(document_data['chunks'])
            
            # Step 3: Process each question
            answers = []
            for i, question in enumerate(questions):
                logger.info(f"Processing question {i+1}/{len(questions)}: {question[:100]}...")
                
                try:
                    answer = await self._process_single_question(question, document_data)
                    answers.append(answer)
                    
                except Exception as e:
                    logger.error(f"Error processing question {i+1}: {str(e)}")
                    answers.append(f"Error processing question: {str(e)}")
            
            logger.info(f"Successfully processed all {len(questions)} questions")
            return answers
            
        except Exception as e:
            logger.error(f"Error in query processing pipeline: {str(e)}")
            raise Exception(f"Query processing failed: {str(e)}")
    
    async def _get_or_process_document(self, document_url: str) -> Dict[str, Any]:
        """Get document from cache or process it if not cached."""
        # Simple URL-based caching
        cache_key = document_url
        
        if cache_key in self.document_cache:
            logger.info("Using cached document data")
            return self.document_cache[cache_key]
        
        # Process document
        logger.info("Processing new document")
        document_data = await self.document_processor.process_document(document_url)
        
        # Cache the result
        self.document_cache[cache_key] = document_data
        
        return document_data
    
    async def _process_single_question(self, question: str, document_data: Dict[str, Any]) -> str:
        """Process a single question through the complete pipeline."""
        try:
            # Step 1: Analyze query relevance
            relevance_info = self.embedding_service.analyze_query_relevance(question)
            
            # Step 2: Get relevant context
            context = self.embedding_service.get_contextual_chunks(question, max_chunks=8)
            
            # Step 3: Fallback to full document if no relevant chunks found
            if not context or relevance_info['confidence'] == 'low':
                logger.warning(f"Low relevance for question, using broader context")
                # Use first few chunks of document as fallback
                fallback_chunks = document_data['chunks'][:5]
                context = '\n\n'.join([chunk['text'] for chunk in fallback_chunks])
            
            # Step 4: Generate answer using LLM
            answer = await self.llm_service.generate_answer(
                context=context,
                question=question,
                relevance_info=relevance_info
            )
            
            return answer
            
        except Exception as e:
            logger.error(f"Error processing single question: {str(e)}")
            return f"Error processing question: {str(e)}"
    
    async def process_queries_with_explanations(self, document_url: str, questions: List[str]) -> List[Dict[str, Any]]:
        """
        Enhanced version that returns detailed explanations for each answer.
        Useful for debugging and understanding the reasoning process.
        """
        try:
            # Process document
            document_data = await self._get_or_process_document(document_url)
            
            # Build vector index
            if not hasattr(self.embedding_service, 'index') or self.embedding_service.index is None:
                self.embedding_service.build_vector_index(document_data['chunks'])
            
            # Process questions with detailed explanations
            detailed_responses = []
            
            for i, question in enumerate(questions):
                logger.info(f"Processing question {i+1}/{len(questions)} with explanations")
                
                try:
                    # Get relevance analysis
                    relevance_info = self.embedding_service.analyze_query_relevance(question)
                    
                    # Get context
                    context = self.embedding_service.get_contextual_chunks(question, max_chunks=8)
                    
                    # Generate answer
                    answer = await self.llm_service.generate_answer(
                        context=context,
                        question=question,
                        relevance_info=relevance_info
                    )
                    
                    # Create explainable response
                    explanation = self.llm_service.create_explainable_response(
                        answer=answer,
                        context=context,
                        question=question,
                        relevance_info=relevance_info
                    )
                    
                    detailed_responses.append(explanation)
                    
                except Exception as e:
                    logger.error(f"Error processing question {i+1} with explanations: {str(e)}")
                    detailed_responses.append({
                        'question': question,
                        'answer': f"Error processing question: {str(e)}",
                        'error': str(e)
                    })
            
            return detailed_responses
            
        except Exception as e:
            logger.error(f"Error in detailed query processing: {str(e)}")
            raise Exception(f"Detailed query processing failed: {str(e)}")
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get statistics about the current processing state."""
        try:
            stats = {
                'documents_cached': len(self.document_cache),
                'vector_index_built': hasattr(self.embedding_service, 'index') and self.embedding_service.index is not None,
                'total_indexed_chunks': 0,
                'embedding_model': self.embedding_service.model_name,
                'llm_model': self.llm_service.model
            }
            
            if stats['vector_index_built']:
                stats['total_indexed_chunks'] = self.embedding_service.index.ntotal
            
            # Add document cache details
            if self.document_cache:
                cache_details = []
                for url, doc_data in self.document_cache.items():
                    cache_details.append({
                        'url': url,
                        'chunk_count': doc_data.get('chunk_count', 0),
                        'text_length': doc_data.get('text_length', 0),
                        'file_type': doc_data.get('file_type', 'unknown')
                    })
                stats['cached_documents'] = cache_details
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting processing statistics: {str(e)}")
            return {'error': str(e)}
    
    def clear_cache(self):
        """Clear the document cache and reset vector index."""
        try:
            self.document_cache.clear()
            self.embedding_service.index = None
            self.embedding_service.chunk_metadata = []
            logger.info("Cleared document cache and vector index")
            
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
