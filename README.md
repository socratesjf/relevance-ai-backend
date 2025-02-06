# Relevance AI Backend

A FastAPI backend for interacting with Relevance AI agents.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a .env file with your Relevance AI credentials
6. Run the application: `uvicorn app.main:app --reload`

## Environment Variables

- RAI_API_KEY: Your Relevance AI API key
- RAI_REGION: Your Relevance AI region
- RAI_PROJECT: Your Relevance AI project ID