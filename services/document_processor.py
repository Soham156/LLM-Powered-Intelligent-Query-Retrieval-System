import os
import requests
import tempfile
import logging
from typing import List, Dict, Any
from urllib.parse import urlparse
import PyPDF2
from docx import Document
import io

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Handles document downloading, parsing, and text extraction.
    Supports PDF and DOCX formats.
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc']
    
    async def download_document(self, url: str) -> bytes:
        """Download document from URL and return content as bytes."""
        try:
            logger.info(f"Downloading document from: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Successfully downloaded document, size: {len(response.content)} bytes")
            return response.content
            
        except requests.RequestException as e:
            logger.error(f"Error downloading document: {str(e)}")
            raise Exception(f"Failed to download document: {str(e)}")
    
    def extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF content."""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise Exception(f"Failed to extract PDF text: {str(e)}")
    
    def extract_text_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX content."""
        try:
            docx_file = io.BytesIO(content)
            doc = Document(docx_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            logger.info(f"Extracted {len(text)} characters from DOCX")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {str(e)}")
            raise Exception(f"Failed to extract DOCX text: {str(e)}")
    
    def get_file_extension(self, url: str) -> str:
        """Get file extension from URL."""
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        for ext in self.supported_formats:
            if ext in path:
                return ext
        
        # Default to PDF if extension not clear
        return '.pdf'
    
    async def process_document(self, url: str) -> Dict[str, Any]:
        """
        Download and process document from URL.
        Returns extracted text and metadata.
        """
        try:
            # Download document
            content = await self.download_document(url)
            
            # Determine file type
            file_extension = self.get_file_extension(url)
            
            # Extract text based on file type
            if file_extension == '.pdf':
                text = self.extract_text_from_pdf(content)
            elif file_extension in ['.docx', '.doc']:
                text = self.extract_text_from_docx(content)
            else:
                raise Exception(f"Unsupported file format: {file_extension}")
            
            # Clean and process text
            cleaned_text = self.clean_text(text)
            
            # Split into chunks for better processing
            chunks = self.split_text_into_chunks(cleaned_text)
            
            return {
                'url': url,
                'file_type': file_extension,
                'raw_text': text,
                'cleaned_text': cleaned_text,
                'chunks': chunks,
                'chunk_count': len(chunks),
                'text_length': len(cleaned_text)
            }
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise Exception(f"Failed to process document: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                cleaned_lines.append(line)
        
        # Join lines with single newlines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive newlines
        while '\n\n\n' in cleaned_text:
            cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')
        
        return cleaned_text
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks for better semantic search.
        Each chunk contains text and metadata.
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                'text': chunk_text,
                'chunk_id': len(chunks),
                'start_word': i,
                'end_word': min(i + chunk_size, len(words)),
                'word_count': len(chunk_words)
            })
            
            # Break if we've reached the end
            if i + chunk_size >= len(words):
                break
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
