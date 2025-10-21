# AI Chat API - Modern LLM Application

A comprehensive backend API for document upload, processing, and AI-powered chat functionality using Large Language Models (LLMs). This application demonstrates modern AI concepts including transformers, embeddings, and Retrieval Augmented Generation (RAG).

## 🚀 Features

### Core AI Capabilities
- **Document Upload & Processing**: Upload PDF, DOCX, TXT, and MD files
- **Vector Database**: Store and search document embeddings using pgvector
- **RAG Chat**: Chat with AI using your uploaded documents as context
- **Text Summarization**: AI-powered text summarization
- **Sentiment Analysis**: Analyze text sentiment using AI

### Technical Features
- **FastAPI Backend**: Modern, fast Python web framework
- **PostgreSQL + pgvector**: Vector database for semantic search
- **OpenAI Integration**: GPT-3.5-turbo for chat and text processing
- **Hugging Face Models**: Sentence transformers for embeddings
- **LangChain**: Framework for LLM applications
- **Docker Support**: Easy deployment with Docker Compose

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   FastAPI API   │    │   PostgreSQL    │
│   (External)    │◄──►│   (Backend)     │◄──►│   + pgvector    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   + HuggingFace │
                       └─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- OpenAI API key
- Hugging Face account (optional, for additional models)

## 🛠️ Installation

### Option 1: Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd Phase-2-LLM
   ```

2. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database:**
   ```bash
   docker-compose exec app python scripts/setup_db.py
   ```

### Option 2: Local Development

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL with pgvector:**
   ```bash
   # Install PostgreSQL with pgvector extension
   # Or use Docker for just the database:
   docker run --name postgres-vector -e POSTGRES_PASSWORD=ai_password -e POSTGRES_DB=ai_chat_db -p 5432:5432 -d pgvector/pgvector:pg15
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database:**
   ```bash
   python scripts/setup_db.py
   ```

5. **Start the application:**
   ```bash
   python -m app.main
   ```

## 🔧 Configuration

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://ai_user:ai_password@localhost:5432/ai_chat_db
POSTGRES_USER=ai_user
POSTGRES_PASSWORD=ai_password
POSTGRES_DB=ai_chat_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Hugging Face Configuration (optional)
HUGGINGFACE_API_TOKEN=your_huggingface_token_here

# Application Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Vector Database Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Document Management
- `POST /documents/upload` - Upload a document
- `GET /documents/` - List all documents
- `GET /documents/{id}` - Get document details
- `DELETE /documents/{id}` - Delete a document

#### Chat Functionality
- `POST /chat/sessions` - Create a chat session
- `GET /chat/sessions` - List chat sessions
- `POST /chat/send` - Send a message
- `GET /chat/sessions/{id}/messages` - Get chat history

#### Text Processing
- `POST /text/summarize` - Summarize text
- `POST /text/sentiment` - Analyze sentiment

## 🧪 Testing

Run the test script to verify everything is working:

```bash
python scripts/test_api.py
```

Or test individual endpoints using curl:

```bash
# Health check
curl http://localhost:8000/health

# Summarize text
curl -X POST "http://localhost:8000/text/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "max_length": 100}'

# Analyze sentiment
curl -X POST "http://localhost:8000/text/sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this application!"}'
```

## 🔍 How It Works

### 1. Document Processing
1. User uploads a document (PDF, DOCX, TXT, MD)
2. Document is parsed and converted to text
3. Text is split into chunks using LangChain's text splitter
4. Each chunk is embedded using sentence transformers
5. Embeddings are stored in PostgreSQL with pgvector

### 2. Chat with RAG
1. User sends a message
2. Message is embedded using the same model
3. Similar document chunks are retrieved using vector similarity
4. Relevant chunks are used as context for the LLM
5. OpenAI GPT generates a response based on the context

### 3. Text Processing
- **Summarization**: Uses OpenAI GPT to create concise summaries
- **Sentiment Analysis**: Uses OpenAI GPT with structured prompts for sentiment classification

## 🏛️ Database Schema

### Documents Table
- `id`: UUID primary key
- `filename`: Original filename
- `content`: Full document text
- `file_type`: File extension
- `file_size`: Size in bytes
- `upload_date`: Timestamp
- `processed`: Boolean flag
- `metadata`: JSON metadata

### Document Chunks Table
- `id`: UUID primary key
- `document_id`: Foreign key to documents
- `chunk_index`: Order of chunk in document
- `content`: Chunk text content
- `embedding`: Vector embedding (384 dimensions)
- `metadata`: JSON metadata

### Chat Sessions Table
- `id`: UUID primary key
- `session_name`: Human-readable name
- `created_at`: Timestamp
- `last_activity`: Last activity timestamp
- `is_active`: Boolean flag

### Chat Messages Table
- `id`: UUID primary key
- `session_id`: Foreign key to chat sessions
- `role`: 'user' or 'assistant'
- `content`: Message content
- `timestamp`: Timestamp
- `metadata`: JSON metadata

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use secure environment variable management
2. **Database**: Use managed PostgreSQL with pgvector
3. **API Keys**: Store securely, never commit to version control
4. **Scaling**: Consider using Redis for caching and task queues
5. **Monitoring**: Add logging and monitoring solutions

### Docker Production Build

```bash
# Build production image
docker build -t ai-chat-api .

# Run with production settings
docker run -d \
  --name ai-chat-api \
  -p 8000:8000 \
  -e DATABASE_URL=your_production_db_url \
  -e OPENAI_API_KEY=your_api_key \
  ai-chat-api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify pgvector extension is installed

2. **OpenAI API Error**
   - Verify API key is correct
   - Check API quota and billing
   - Ensure internet connectivity

3. **Memory Issues**
   - Reduce `CHUNK_SIZE` in configuration
   - Use smaller embedding models
   - Increase Docker memory limits

4. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify virtual environment activation

### Getting Help

- Check the logs: `docker-compose logs app`
- Review API documentation at `/docs`
- Test individual endpoints using the test script

## 🎯 Learning Objectives

This project demonstrates:

1. **Transformers**: Understanding how transformer models work conceptually
2. **Embeddings**: Converting text to vector representations
3. **Vector Databases**: Storing and searching high-dimensional vectors
4. **RAG**: Retrieval Augmented Generation for context-aware responses
5. **LLM Integration**: Working with pre-trained language models
6. **API Design**: Building RESTful APIs with FastAPI
7. **Database Design**: Relational database with vector extensions

## 🔮 Future Enhancements

- [ ] WebSocket support for real-time chat
- [ ] File type support (images, audio, video)
- [ ] Multi-language support
- [ ] User authentication and authorization
- [ ] Advanced search and filtering
- [ ] Model fine-tuning capabilities
- [ ] Batch processing for large documents
- [ ] Caching layer for improved performance
# AI-knowlegde-chatbot
