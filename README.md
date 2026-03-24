# Trade Opportunities API

A production-grade FastAPI service designed to provide real-time, AI-driven investment insights into various Indian market sectors. This project implements industry-standard security patterns, highly optimized caching, and custom rate limiting.

---

## 📋 Table of Contents

- [INTRODUCTION](#introduction)
- [Detailed Implementation](#detailed-implementation)
    - [Application Flow Diagram](#application-flow-diagram)
    - [Technical Breakdown](#technical-breakdown)
    - [Summary Table](#summary-table)
- [Setup & Installation](#setup--installation)
- [Usage & API Flow](#usage--api-flow)
- [Core Logic Snippets](#core-logic-snippets)
- [Project Structure](#project-structure)

---

## INTRODUCTION

Hi Team, I have implemented a professional FastAPI application for market analysis reports as per the specified requirements. This service combines real-time data scraping with Generative AI to provide actionable investment reports.

I have focused on **Resilience** (handling AI quota limits via caching), **Security** (JWT tokens with hashed passwords), and **Performance** (sub-20ms response times for cached data).

---

## Detailed Implementation

### Application Flow Diagram

```mermaid
graph TD
    A[Client Request] --> B[POST /token - Login]
    B --> C{JWT Token issued}
    C --> D[Client stores token]
    
    D --> E1[GET /analyze/{sector}]
    D --> E2[GET /health]
    
    E1 --> F[Auth: Validate JWT Signature]
    F --> G[Custom Rate Limiter Check]
    G --> H{In-memory Cache Hit?}
    H -- Yes --> I[Return Cached Report]
    H -- No --> J[search_market_data - DuckDuckGo]
    J --> K[analyze_with_gemini - Gemini API]
    K --> L[Store in Cache & Return Markdown Report]
    
    E2 --> M[Return Health Status]
```

### Technical Breakdown

#### **Backend Framework (FastAPI)**
- **How it works**: Provides the core asynchronous engine for the API. It handles routing, automatic Pydantic validation, and dependency injection for security layers.

#### **Security & Authentication (JWT)**
- **Library**: `PyJWT`, `passlib[bcrypt]`
- **How it works**: We use stateless **JSON Web Tokens (JWT)**. On login, the server issues a signed token. Protected endpoints verify this signature using a secret key. Passwords are never stored in plain text.

#### **Performance & Caching**
- **Library**: `cachetools (TTLCache)`
- **How it works**: To stay within Gemini's free tier quotas and ensure extreme speed, we implement an in-memory sliding cache. If the same sector is requested within 5 minutes, the result is served in **~14ms** without hitting external APIs.

#### **Rate Limiting (Custom)**
- **Implementation**: Sliding Window algorithm.
- **How it works**: We track request timestamps in a per-user dictionary. If a user exceeds 5 requests per minute, the system rejects the call with a `429 Too Many Requests` status and a `Retry-After` header.

#### **AI/Data Sources**
- **LLM**: Google Gemini 1.5/2.x Flash.
- **Web Search**: DuckDuckGo Search API (`ddgs`).
- **Data Collection**: Real-time news is fetched, cleaned, and passed as context to the AI for professional synthesis.

---

### Summary Table

| Feature | Library / Model | How it Works (Short) |
| :--- | :--- | :--- |
| **FastAPI** | `fastapi` | Main API framework & async execution |
| **Authentication** | `PyJWT`, `passlib` | Stateless JWT tokens + password hashing |
| **Rate Limiting** | Custom Logic | Sliding window, per-IP, in-memory |
| **Caching** | `cachetools` | 5-min TTL cache for instant responses |
| **LLM (AI)** | `google-generativeai` | Gemini AI for report generation |
| **Web Search** | `duckduckgo-search` | Scrape real-time market trends |
| **Storage** | Python Dicts | In-memory only (stateless architecture) |

---

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/DsThakurRawat/Appscrip.git
   cd Appscrip
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_jwt_secret_key_here
   ```

---

## Usage & API Flow

### 1. Get Access Token
**Endpoint**: `POST /analyze/token`
```bash
curl -X POST http://127.0.0.1:8000/analyze/token
```

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

---

## Core Logic Snippets

### Input Validation & Safety
```python
@router.get("/{sector}", response_model=MarketReport)
async def analyze_sector(
    sector: str = Path(..., min_length=3, regex="^[a-zA-Z ]+$"),
    payload: dict = Depends(verify_jwt),
    _rate_limit: None = Depends(check_rate_limit)
):
    # Data is automatically validated by FastAPI/Pydantic here
    ...
```

### JWT Security Model
```python
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
```

---

## Project Structure

- `app/main.py`: Entry point with CORS and Router initialization.
- `app/api/`: Endpoint definitions and request/response handling.
- `app/core/`: Security (JWT), Config management, and Rate Limiting.
- `app/services/`: Business logic (Market Scraper & AI Analysis).
- `app/models/`: Pydantic schemas for data validation.
