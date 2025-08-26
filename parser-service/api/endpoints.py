import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from . import schemas
from ..core import parsing, rag
from ..core.parsing import process_resume_with_pipeline

router = APIRouter()

@router.post("/parse-resume/", response_model=schemas.ParseResponse)
async def create_upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a resume PDF, parse it, and store it.
    """
    # Save the uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Process the file
        result = process_resume_with_pipeline(tmp_path, file.filename)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path) # Clean up the temp file

    return schemas.ParseResponse(
        resume_id=result["resume_id"],
        file_name=result["file_name"],
        content=result["content"],
        message="Resume parsed and stored successfully."
    )

@router.get("/match-jobs/{resume_id}", response_model=schemas.MatchResponse)
async def get_job_matches(resume_id: int):
    """
    Endpoint to find job matches for a previously parsed resume.
    """
    try:
        matches = rag.find_job_matches(resume_id)
        return schemas.MatchResponse(resume_id=resume_id, matches=matches)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")