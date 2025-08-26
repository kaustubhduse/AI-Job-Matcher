import os
from datetime import datetime
import json

# Import the specific pipeline and connector classes from od-parse
from od_parse.advanced.pipeline import (
    PDFPipeline,
    LoadDocumentStage,
    AdvancedParsingStage,
    TableExtractionStage,
    FormExtractionStage,
    DocumentStructureStage,
    OutputFormattingStage
)
from od_parse.advanced.integrations import VectorDBConnector, DatabaseConnector
from od_parse.advanced.unified_parser import UnifiedPDFParser

def process_resume_with_pipeline(file_path: str, file_name: str) -> dict:
    """
    Processes a resume PDF using a full pipeline, stores data and vectors
    in databases, and returns the result.
    """
    # --- Step 1: Configure the full processing pipeline ---
    pipeline = PDFPipeline()
    pipeline.add_stage(LoadDocumentStage())
    pipeline.add_stage(AdvancedParsingStage())
    pipeline.add_stage(TableExtractionStage({"use_neural": True}))
    pipeline.add_stage(FormExtractionStage())
    pipeline.add_stage(DocumentStructureStage())
    pipeline.add_stage(OutputFormattingStage({"format": "json"})) # Ensure output is structured

    # --- Step 2: Process the document ---
    print(f"Processing document: {file_name}")
    result = pipeline.process(file_path)

    # --- Step 3: Store structured data in PostgreSQL ---
    # The connector reads the connection string from environment variables
    db_conn_string = os.getenv("DATABASE_URL")
    if not db_conn_string:
        raise ValueError("DATABASE_URL environment variable is not set.")
        
    db_connector = DatabaseConnector({
        "db_type": "postgres",
        "conn_string": db_conn_string
    })
    # The export method should return the ID of the newly created record
    resume_id = db_connector.export(result, table_name="resumes")
    print(f"Stored structured data for resume ID: {resume_id}")

    # --- Step 4: Store vector embeddings in pgvector for RAG ---
    pgvector_conn_string = os.getenv("PGVECTOR_URL")
    if not pgvector_conn_string:
        raise ValueError("PGVECTOR_URL environment variable is not set.")

    vector_connector = VectorDBConnector({
        "db_type": "pgvector",
        "conn_string": pgvector_conn_string
    })
    # The export method needs the parent record ID to link the vectors
    vector_connector.export(result, foreign_key_id=resume_id, table_name="resume_embeddings")
    print(f"Stored vector embeddings for resume ID: {resume_id}")

    # --- Step 5: Generate human-readable markdown ---
    markdown_content = UnifiedPDFParser().to_markdown(result)

    # --- Step 6: Log the processing (optional, but good practice) ---
    log_data = {
        "file": file_name,
        "resume_id": resume_id,
        "timestamp": datetime.now().isoformat(),
        "duration": result.get("processing_duration_seconds"),
        "stats": result.get("summary", {}).get("extraction_statistics", {})
    }
    print(f"Processing log: {json.dumps(log_data)}")

    return {
        "resume_id": resume_id,
        "file_name": file_name,
        "content": markdown_content
    }