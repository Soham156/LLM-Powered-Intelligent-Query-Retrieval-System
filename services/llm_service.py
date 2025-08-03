import os
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMService:
    """
    Handles LLM interactions for question answering and decision making.
    Uses Hugging Face router with Llama model for intelligent analysis and response generation.
    """
    
    def __init__(self):
        self.hf_token = os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise Exception("HF_TOKEN environment variable is required")
        
        if OpenAI is None:
            raise Exception("OpenAI package not installed. Please install with: pip install openai")
        
        # Initialize OpenAI client with Hugging Face router base URL
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=self.hf_token
        )
        self.model = os.getenv("LLM_MODEL", "meta-llama/Llama-3.2-1B-Instruct:novita")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.1"))
        
        logger.info(f"Initialized LLM service with Hugging Face model: {self.model}")
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for document analysis."""
        return """You are an expert document analysis assistant specializing in insurance, legal, HR, and compliance domains. Your task is to analyze document content and provide accurate, detailed answers to specific questions.

INSTRUCTIONS:
1. Analyze the provided document context carefully
2. Answer questions based ONLY on the information present in the document
3. Provide specific details, numbers, timeframes, and conditions when available
4. If information is not found in the document, clearly state "Information not found in the document"
5. Be precise and avoid speculation or assumptions
6. Include relevant clause references or section details when applicable
7. For complex conditions, break them down clearly
8. Use professional, clear language appropriate for the domain

RESPONSE FORMAT:
- Provide direct, factual answers
- Include specific details (amounts, timeframes, percentages, etc.)
- Mention conditions or limitations when they apply
- Be concise but comprehensive
- Ensure accuracy over brevity"""
    
    def create_user_prompt(self, context: str, question: str) -> str:
        """Create the user prompt with context and question."""
        return f"""DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

Please analyze the document context and provide a detailed, accurate answer to the question. Base your response strictly on the information provided in the document context above."""
    
    async def generate_answer(self, context: str, question: str, relevance_info: Dict[str, Any] = None) -> str:
        """
        Generate an answer to a question based on document context.
        Uses the relevance information to adjust response strategy.
        """
        try:
            logger.info(f"Generating answer for question: {question[:100]}...")
            
            # Check if we have relevant content
            if relevance_info and not relevance_info.get('has_relevant_content', True):
                return "Information not found in the document. The question does not appear to be covered in the provided document content."
            
            # Prepare messages for the LLM
            system_prompt = self.create_system_prompt()
            user_prompt = self.create_user_prompt(context, question)
            
            # Adjust approach based on confidence level
            confidence = relevance_info.get('confidence', 'medium') if relevance_info else 'medium'
            
            if confidence == 'low':
                # Add instruction for low confidence scenarios
                user_prompt += "\n\nNOTE: The semantic search indicates limited relevant content for this question. Please be extra careful to only state what is explicitly mentioned in the document."
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Make API call to Hugging Face router using OpenAI client format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Log token usage
            usage = response.usage if hasattr(response, 'usage') else {}
            total_tokens = usage.total_tokens if hasattr(usage, 'total_tokens') else 'unknown'
            logger.info(f"Generated answer with {total_tokens} tokens")
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return f"Error processing question: {str(e)}"
    
    async def batch_generate_answers(self, questions_contexts: List[Dict[str, Any]]) -> List[str]:
        """
        Generate answers for multiple questions in batch.
        Each item should have 'question', 'context', and optionally 'relevance_info'.
        """
        answers = []
        
        for i, item in enumerate(questions_contexts):
            logger.info(f"Processing question {i+1}/{len(questions_contexts)}")
            
            answer = await self.generate_answer(
                context=item['context'],
                question=item['question'],
                relevance_info=item.get('relevance_info')
            )
            
            answers.append(answer)
        
        return answers
    
    def extract_key_clauses(self, context: str, question: str) -> List[Dict[str, Any]]:
        """
        Extract key clauses relevant to the question from the context.
        This helps with explainability and traceability.
        """
        try:
            # This is a simplified version - in production, you might use
            # more sophisticated clause extraction techniques
            
            # Split context into sentences/clauses
            sentences = context.split('.')
            relevant_clauses = []
            
            # Simple keyword matching for clause identification
            question_keywords = set(question.lower().split())
            
            for i, sentence in enumerate(sentences):
                sentence = sentence.strip()
                if len(sentence) < 20:  # Skip very short sentences
                    continue
                
                sentence_words = set(sentence.lower().split())
                
                # Calculate simple word overlap
                overlap = len(question_keywords & sentence_words)
                
                if overlap >= 2:  # At least 2 matching words
                    relevant_clauses.append({
                        'clause_id': i,
                        'text': sentence,
                        'relevance_score': overlap / len(question_keywords),
                        'word_overlap': overlap
                    })
            
            # Sort by relevance score
            relevant_clauses.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return relevant_clauses[:5]  # Return top 5 relevant clauses
            
        except Exception as e:
            logger.error(f"Error extracting key clauses: {str(e)}")
            return []
    
    def create_explainable_response(self, answer: str, context: str, question: str, 
                                  relevance_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create an explainable response with reasoning and source traceability.
        """
        try:
            # Extract relevant clauses
            key_clauses = self.extract_key_clauses(context, question)
            
            # Create explanation
            explanation = {
                'answer': answer,
                'question': question,
                'confidence': relevance_info.get('confidence', 'medium') if relevance_info else 'medium',
                'key_clauses': key_clauses,
                'reasoning': {
                    'semantic_similarity': relevance_info.get('max_similarity', 0.0) if relevance_info else 0.0,
                    'relevant_chunks': relevance_info.get('relevant_chunk_count', 0) if relevance_info else 0,
                    'has_supporting_evidence': len(key_clauses) > 0
                },
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'model_used': self.model,
                    'processing_method': 'semantic_search_with_llm'
                }
            }
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error creating explainable response: {str(e)}")
            return {
                'answer': answer,
                'question': question,
                'error': str(e)
            }
