# Trade Opportunities API

A high-performance FastAPI service designed to analyze Indian market sectors using Generative AI (Gemini) and real-time web search.

## Key Features

- **FastAPI**: Modern, high-performance web framework.
- **JWT Authentication**: Secure, token-based access via `/token` endpoint.
- **Professional Caching**: 5-minute in-memory TTL cache for near-instant repeated requests (~14ms).
- **Custom Rate Limiting**: Built-in sliding-window protection (5 req/min) with `Retry-After` support.
- **AI-Driven Intelligence**: Powered by **Google Gemini 1.5/2.x Flash**.

## Setup & Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DsThakurRawat/Appscrip.git
   cd Appscrip
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment:

   Create a `.env` file in the root directory:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_jwt_secret_key
   ```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

## API Documentation

- **Interactive Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Usage & API Flow

### 1. Get Access Token

**Endpoint**: `POST /analyze/token`

```bash
curl -X POST http://127.0.0.1:8000/analyze/token
```

*Response*: `{"access_token": "...", "token_type": "bearer"}`

### 2. Analyze a Market Sector

**Endpoint**: `GET /analyze/{sector}`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:8000/analyze/technology
```

### 3. Health Check

**Endpoint**: `GET /analyze/health`

```bash
curl http://127.0.0.1:8000/analyze/health
```

## Project Structure

- `app/main.py`: Application entry point and middleware configuration.
- `app/api/`: REST API endpoints and routing logic.
- `app/services/`: Core logic for Data Scraping and AI Analysis.
- `app/core/`: Security protocols, rate limiting, and config management.
- `app/models/`: Pydantic data schemas for validation.
