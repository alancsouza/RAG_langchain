# Finance Advisor Agent

A small toy project to learn AI techniques such as RAG (Retrieval-Augmented Generation) and MCP (Model Context Protocol).

This FastAPI application uses LangChain for agent operations, providing an intelligent finance advisor that can answer questions about financial documents using RAG techniques.

## Features

- **FastAPI REST API** for processing financial questions
- **LangChain integration** for AI agent operations
- **RAG implementation** for document-based question answering
- **Async processing** with background task handling
- **PDF document processing** using PyPDF
- **OpenAI embeddings** for semantic search

## Tech Stack

- **Package Manager**: UV (ultra-fast Python package manager)
- **Web Framework**: FastAPI
- **AI Framework**: LangChain + LangGraph
- **Vector Store**: In-memory vector store
- **Document Processing**: PyPDF
- **Embeddings**: OpenAI

## Setup

### Prerequisites

- Python 3.12+
- UV package manager
- OpenAI API key

### Installation

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository**:
```bash
git clone <repository-url>
cd RAG_langchain
```

3. **Create and activate UV environment**:
```bash
# Create a new virtual environment with Python 3.12+
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

4. **Install dependencies**:
```bash
uv sync
```

5. **Set up environment variables**:
```bash
# Copy and edit the .env file
cp .env.example .env
# Add your OpenAI API key to .env
echo 'OPENAI_API_KEY="your-api-key-here"' >> .env
```

## Running the Application

### Option 1: Local Development

#### Start the Development Server

```bash
uv run fastapi dev rag_finance/api/routes.py
```

### Option 2: Docker Compose (Recommended for Production)

#### Prerequisites
- Docker
- Docker Compose

#### Build and Run with Docker Compose

```bash
# Build and start the services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the services
docker-compose down
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

#### Docker Environment Variables

Make sure your `.env` file contains:
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

#### Docker Commands

```bash
# Rebuild the container
docker-compose build

# View running containers
docker-compose ps

# Execute commands inside the container
docker-compose exec rag-finance-api bash

# View application logs
docker-compose logs rag-finance-api

# Restart a specific service
docker-compose restart rag-finance-api
```

### API Endpoints

#### POST /message
Process a financial question and return a task ID for async processing.

**Request:**
```bash
curl -X POST "http://localhost:8000/message" \
     -H "Content-Type: application/json" \
     -d '{"question": "Quais foram os meus principais gastos este mês?"}'
```

**Response:**
```json
{
  "task_id": "140234567890123",
  "status": "processing"
}
```

## Testing

### End-to-End Tests

Run the comprehensive end-to-end tests that validate all sample questions:

```bash
# Make sure the development server is running first
uv run fastapi dev rag_finance/api/routes.py

# In another terminal, run the e2e tests
uv run python rag_finance/tests/end2end/sample_questions.py
```

The tests will:
- Send all sample questions to the `/message` endpoint
- Assert that all responses return HTTP 202 status
- Display detailed progress and results
- Provide a summary of test results

## Project Structure

```
rag_finance/
├── api/
│   └── routes.py          # FastAPI routes and endpoints
├── core/
│   ├── graph.py          # LangGraph workflow definition
│   ├── index.py          # Document loading and vector store
│   ├── models.py         # Pydantic models and LLM config
│   └── prompts.py        # Custom RAG prompts
├── data/                 # PDF documents (gitignored)
└── tests/
    └── end2end/
        └── sample_questions.py  # E2E test suite
```

## Development

### Adding New Questions

Add new sample questions in `rag_finance/tests/end2end/sample_questions.py`:

```python
SAMPLE_QUESTIONS = [
    "Your new question here?",
    # ... existing questions
]
```

### Modifying the RAG Pipeline

The main RAG logic is in `rag_finance/core/graph.py`. The pipeline includes:
1. **Document Retrieval**: Load and search relevant documents
2. **Context Generation**: Prepare context from retrieved documents  
3. **Answer Generation**: Generate answers using LLM with context

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## License

This project is for educational purposes and learning AI techniques.