# Trade Opportunities API

A professional FastAPI service that provides market analysis and trade opportunity insights for specific sectors in India using Google Gemini AI.

## Features
- **FastAPI**: Modern, fast (high-performance) web framework.
- **AI Analysis**: Powered by Google Gemini 1.5-flash for professional market reports.
- **Web Search**: Real-time data collection using DuckDuckGo Search.
- **Security**: Simple API Key authentication and Rate Limiting.
- **Documentation**: Auto-generated Swagger UI and Redoc.

## Prerequisites
- Python 3.8+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Appscrip
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   API_KEY=appscrip_dev_2024
   ```

## Running the Application

Start the server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Usage Example

### Analyze a Sector
**Endpoint**: `GET /analyze/{sector}`
**Header**: `X-API-KEY: appscrip_dev_2024`

Example with `curl`:
```bash
curl -H "X-API-KEY: appscrip_dev_2024" http://127.0.0.1:8000/analyze/pharmaceuticals
```

## Project Structure
- `app/main.py`: Entry point.
- `app/api/`: API routes.
- `app/services/`: Business logic (Scraping, AI Analysis).
- `app/core/`: Configuration and Security.
- `app/models/`: Pydantic schemas.
# Appscrip
