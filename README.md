# Trade Opportunities API

A high-performance FastAPI service designed to analyze Indian market sectors using Generative AI (Gemini) and real-time web search.

## Key Features

- **FastAPI**: Modern, high-performance web framework with automatic Swagger/OpenAPI documentation.
- **AI-Driven Intelligence**: Powered by **Google Gemini 1.5/2.x Flash** for professional-grade market analysis.
- **Real-time Insights**: Integrates DuckDuckGo Search to fetch the latest market trends and news from the Indian economy.
- **Secure & Robust**:
  - API Key authentication (`X-API-KEY` header).
  - Smart rate limiting (5 requests/minute) via `Slowapi`.
  - Built-in fallback mechanisms for maximum availability.

## Prerequisites

- Python 3.8+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

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
   API_KEY=appscrip_dev_2026
   ```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

## API Documentation

- **Interactive Documentation (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Usage & Examples

### Analyze a Market Sector

**Endpoint**: `GET /analyze/{sector}`

**Supported Sectors**: `pharmaceuticals`, `technology`, `banking`, `automotive`, `telecommunications`, `energy`, `healthcare`, `consumer goods`, `retail`, `real estate`, `media`, `agriculture`, `mining`, `textiles`, `chemicals`, `education`, `tourism`, `sports`, etc.

**Example Request (`curl`)**:
```bash
curl -H "X-API-KEY: appscrip_dev_2026" http://127.0.0.1:8000/analyze/technology
```

## Project Structure

- `app/main.py`: Application entry point and middleware configuration.
- `app/api/`: REST API endpoints and routing logic.
- `app/services/`: Core logic for Data Scraping and AI Analysis.
- `app/core/`: Security protocols, rate limiting, and config management.
- `app/models/`: Pydantic data schemas for validation.
