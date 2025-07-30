<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# LLM-Powered Query-Retrieval System - Copilot Instructions

This project is an intelligent document analysis system designed for a hackathon competition. When working on this codebase, please follow these guidelines:

## Project Context
- This is a FastAPI-based application for processing insurance, legal, HR, and compliance documents
- The system uses vector embeddings (FAISS) for semantic search and GPT-4 for intelligent question answering
- The main endpoint is `/api/v1/hackrx/run` which processes documents and returns structured JSON responses

## Architecture Guidelines
- **Modular Design**: Keep services separated in the `services/` directory
- **Error Handling**: Always implement comprehensive exception handling with meaningful error messages
- **Logging**: Use structured logging throughout the application for debugging and monitoring
- **Type Hints**: Use Python type hints for all function parameters and return types
- **Async/Await**: Prefer async operations for I/O-bound tasks like document processing and API calls

## Code Style
- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add docstrings to all classes and methods
- Keep functions focused and single-purpose
- Use constants for configuration values

## Domain-Specific Considerations
- When working with document processing, consider various file formats (PDF, DOCX)
- Implement robust text cleaning and chunking strategies
- Optimize embeddings for domain-specific terminology (insurance, legal, HR, compliance)
- Ensure LLM prompts are tailored for accurate document analysis
- Prioritize explainability and traceability in responses

## Performance Optimization
- Implement caching for processed documents
- Optimize vector search parameters for accuracy and speed
- Use efficient text chunking strategies with appropriate overlap
- Minimize LLM token usage while maintaining accuracy
- Consider batch processing for multiple questions

## Security & Authentication
- Validate all input data using Pydantic models
- Implement proper bearer token authentication
- Sanitize document URLs and content
- Handle sensitive information appropriately

## Testing & Deployment
- Write comprehensive tests for all core functionality
- Ensure compatibility with cloud deployment platforms (Heroku, Railway, Render)
- Optimize for production environment variables and configuration
- Implement health checks and monitoring endpoints

## API Design
- Follow RESTful principles
- Return consistent JSON response formats
- Implement proper HTTP status codes
- Provide clear error messages and debugging information
- Maintain backward compatibility for API changes

When suggesting code improvements or new features, prioritize:
1. Accuracy and reliability of document analysis
2. Performance optimization for real-time processing
3. Maintainability and code clarity
4. Deployment readiness and scalability
5. Comprehensive error handling and logging
