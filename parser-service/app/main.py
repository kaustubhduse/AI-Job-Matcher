from fastapi import FastAPI
from dotenv import load_dotenv
from .api import endpoints

# Load environment variables from a .env file
load_dotenv()

app = FastAPI(
    title="AI Job Matcher - Parser Service",
    description="A microservice for parsing resumes and handling RAG.",
    version="1.0.0"
)

# Include the API routes
app.include_router(endpoints.router, prefix="/api/v1", tags=["Matching"])

@app.get("/")
def read_root():
    return {"status": "Parser service is running"}