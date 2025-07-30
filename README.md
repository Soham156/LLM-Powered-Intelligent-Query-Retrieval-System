# 🤖 LLM-Powered Intelligent Query-Retrieval System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated document analysis system that processes PDFs and DOCX files to answer domain-specific questions using advanced semantic search and Large Language Models. Built for hackathon competition with production-ready architecture.

## 🎯 Features

- **Multi-format Document Processing**: Supports PDF and DOCX files
- **Semantic Search**: FAISS-powered vector embeddings for intelligent content retrieval
- **LLM-Powered Analysis**: GPT-4 integration for contextual question answering
- **Domain Expertise**: Specialized for insurance, legal, HR, and compliance documents
- **Explainable AI**: Provides reasoning and source traceability for answers
- **RESTful API**: FastAPI-based architecture with comprehensive endpoints
- **Production Ready**: Optimized for performance, scalability, and deployment

## 🏗️ System Architecture

```
Input Documents (PDF/DOCX) → Document Processor → Text Extraction
                                    ↓
Embedding Service ← Text Chunks ← Text Segmentation
       ↓
Vector Index (FAISS) → Semantic Search → Relevant Context
                           ↓
LLM Service (GPT-4) → Answer Generation → JSON Response
```

## 📋 API Specification

### Main Endpoint

**POST** `/api/v1/hackrx/run`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <api_key>
```

**Request Body:**
```json
{
    "documents": "https://example.com/policy.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What are the waiting periods for pre-existing diseases?"
    ]
}
```

**Response:**
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment...",
        "There is a waiting period of thirty-six (36) months..."
    ]
}
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API Key
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd llm-query-retrieval-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
```

4. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `API_KEY` | Bearer token for authentication | Generated |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DEBUG` | Debug mode | False |
| `EMBEDDING_MODEL` | Sentence transformer model | all-MiniLM-L6-v2 |
| `SIMILARITY_THRESHOLD` | Minimum similarity score | 0.7 |

## 🔧 Technical Details

### Document Processing Pipeline

1. **Download**: Secure document retrieval from URLs
2. **Parse**: Extract text from PDF/DOCX formats
3. **Segment**: Split text into overlapping chunks for better context
4. **Clean**: Normalize and prepare text for analysis

### Semantic Search Engine

- **Embeddings**: Uses sentence-transformers for high-quality text representations
- **Vector Store**: FAISS for efficient similarity search
- **Retrieval**: Cosine similarity matching with configurable thresholds
- **Context Assembly**: Intelligent chunk combination for LLM processing

### LLM Integration

- **Model**: GPT-4 for superior reasoning capabilities
- **Prompting**: Domain-specific system prompts for accuracy
- **Token Optimization**: Efficient context management
- **Error Handling**: Robust fallback mechanisms

## 📊 Performance Metrics

- **Accuracy**: Precision of query understanding and clause matching
- **Token Efficiency**: Optimized LLM usage for cost-effectiveness
- **Latency**: Sub-30-second response times
- **Scalability**: Supports concurrent request processing

## 🧪 Testing

### Manual Testing

```bash
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "documents": "https://example.com/sample.pdf",
    "questions": ["What is covered under this policy?"]
  }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🚀 Deployment

### Heroku Deployment

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Set environment variables**
```bash
heroku config:set OPENAI_API_KEY=your_key
heroku config:set API_KEY=your_bearer_token
```

3. **Deploy**
```bash
git push heroku main
```

### Other Platforms

- **Railway**: Supports direct GitHub deployment
- **Render**: Auto-deploy from repository
- **Vercel**: Serverless deployment option
- **AWS/GCP/Azure**: Container or serverless deployment

## 📁 Project Structure

```
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment configuration
├── runtime.txt           # Python version specification
├── services/             # Core business logic
│   ├── __init__.py
│   ├── document_processor.py    # Document parsing and processing
│   ├── embedding_service.py     # Vector embeddings and search
│   ├── llm_service.py          # LLM integration and prompting
│   └── query_processor.py      # Main orchestration pipeline
├── .env.example          # Environment variables template
└── README.md            # This file
```

## 🔒 Security Features

- **Bearer Token Authentication**: Secure API access control
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive exception management
- **Rate Limiting**: Configurable request throttling
- **HTTPS Ready**: SSL/TLS support for production

## 🎯 Domain Specialization

### Insurance Documents
- Policy terms and conditions
- Coverage details and exclusions
- Premium calculations and discounts
- Claim procedures and waiting periods

### Legal Documents
- Contract clauses and obligations
- Terms and conditions analysis
- Compliance requirements
- Risk assessments

### HR Documents
- Employee policies and procedures
- Benefits and compensation
- Leave and attendance policies
- Code of conduct

### Compliance Documents
- Regulatory requirements
- Audit procedures
- Risk management policies
- Standard operating procedures

## 🔧 Advanced Configuration

### Chunk Processing
```python
CHUNK_SIZE = 1000           # Words per chunk
CHUNK_OVERLAP = 200         # Overlap between chunks
MAX_CHUNKS_PER_QUERY = 8    # Maximum chunks for context
```

### Vector Search
```python
VECTOR_DIMENSION = 384      # Embedding dimension
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score
```

### LLM Settings
```python
MAX_TOKENS = 2000          # Maximum response tokens
TEMPERATURE = 0.1          # Response creativity (0.0-2.0)
```

## 📈 Monitoring and Observability

- **Structured Logging**: Comprehensive request/response logging
- **Performance Metrics**: Response time and accuracy tracking
- **Error Tracking**: Detailed error reporting and analysis
- **Usage Analytics**: Token consumption and cost monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation for common solutions
- Review the logs for detailed error information

## 🎯 Hackathon Submission

This project is specifically designed for the HackRX competition requirements:

- ✅ FastAPI backend with required `/hackrx/run` endpoint
- ✅ Bearer token authentication
- ✅ PDF/DOCX document processing
- ✅ Vector embeddings with FAISS
- ✅ GPT-4 integration
- ✅ Structured JSON responses
- ✅ Production-ready deployment configuration
- ✅ Comprehensive documentation

**Evaluation Criteria Met:**
- **Accuracy**: Domain-specific prompting and semantic search
- **Token Efficiency**: Optimized context management
- **Latency**: Sub-30-second response times
- **Reusability**: Modular, extensible architecture
- **Explainability**: Traceable decision reasoning
