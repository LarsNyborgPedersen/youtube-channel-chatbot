# YouTube Channel Q&A Chatbot

A production-ready chatbot that can answer questions about any YouTube channel's content using Next.js, FastAPI, LangChain, Qdrant, and Ollama.

## Architecture

- **Frontend**: Next.js with TypeScript, Radix UI, and TailwindCSS
- **Backend**: FastAPI with Pydantic settings and structured logging
- **Vector DB**: Qdrant for transcript storage and retrieval
- **LLM**: Ollama for local language model inference
- **Transcripts**: youtube-transcript-api for fetching video transcripts

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+ with venv support
- Docker and Docker Compose (for Qdrant and Ollama)
- Yarn package manager

### 1. Clone and Setup

```bash
git clone <repository-url>
cd youtube-channel-chatbot
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env if needed (defaults work for local development)
# NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
# QDRANT_URL=http://localhost:6333
# OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Start Services

#### Option A: Full Stack (Recommended)

```bash
# Start Qdrant and Ollama via Docker Compose
docker-compose up -d qdrant ollama

# Backend setup with virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, install and start frontend
cd frontend
yarn install
yarn dev
```

#### Option B: Development Mode

```bash
# Terminal 1: Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2: Start Ollama
docker run -p 11434:11434 ollama/ollama

# Terminal 3: Backend with virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload

# Terminal 4: Frontend
cd frontend
yarn install
yarn dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Usage

1. **Enter Channel URL**: Go to the homepage and enter a YouTube channel URL
2. **Create Chatbot**: Click "Create Chatbot" to fetch and process transcripts
3. **Ask Questions**: Once loaded, ask questions about the channel's content
4. **Get AI Answers**: Receive intelligent responses based on the channel's transcripts

## API Endpoints

### Current (Step 2)
- `POST /api/transcripts/fetch` - Fetch transcripts from YouTube channel

### Upcoming (Steps 3-6)
- `POST /api/transcripts/store` - Store transcripts in vector database
- `GET /api/transcripts` - Retrieve stored transcripts
- `POST /api/retrieve` - Search for relevant transcript chunks
- `POST /api/ask` - Ask questions and get AI-powered answers

## Development

### Project Structure

```
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # UI components
│   │   └── lib/             # Utilities and API client
│   └── package.json
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── core/            # Settings and configuration
│   │   └── services/        # Business logic
│   └── requirements.txt
├── infra/                   # Docker Compose and infrastructure
├── docs/                    # Documentation
└── README.md
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_BACKEND_URL` | Backend API URL | `http://localhost:8000` |
| `APP_CORS_ALLOW_ORIGINS` | CORS allowed origins | `http://localhost:3000,http://127.0.0.1:3000` |
| `QDRANT_URL` | Qdrant vector database URL | `http://localhost:6333` |
| `QDRANT_COLLECTION_NAME` | Qdrant collection name | `youtube_transcripts` |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama2` |

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure `NEXT_PUBLIC_BACKEND_URL` matches your backend URL
2. **Backend Not Starting**: 
   - Check Python version (3.11+)
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` in activated venv
3. **Frontend Build Errors**: Run `yarn install` and check Node.js version (18+)
4. **Qdrant Connection**: Ensure Docker container is running on port 6333
5. **Ollama Connection**: Ensure Docker container is running on port 11434
6. **Virtual Environment Issues**: 
   - Make sure to activate venv before running backend
   - If packages not found, reinstall in activated environment

### Logs

- **Backend**: Check terminal output for FastAPI logs
- **Frontend**: Check browser console and terminal output
- **Qdrant**: `docker logs <container-id>`
- **Ollama**: `docker logs <container-id>`

## Contributing

1. Follow the project structure and naming conventions
2. Use TypeScript for frontend, Python 3.11+ for backend
3. Follow clean code principles and add docstrings
4. Update documentation when adding new features

## License

MIT License - see LICENSE file for details
