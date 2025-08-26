from sqlalchemy import text
from .parsing import get_db_connection

def find_job_matches(resume_id: int, limit: int = 10) -> list:
    """
    Finds top job matches for a given resume vector.
    """
    conn = get_db_connection()

    # 1. Get the resume's embedding from the database
    resume_result = conn.execute(
        text("SELECT embedding FROM resumes WHERE id = :id"), {"id": resume_id}
    ).fetchone()

    if not resume_result:
        conn.close()
        raise ValueError(f"Resume with ID {resume_id} not found.")
        
    resume_embedding = resume_result[0]

    # 2. Perform vector similarity search against the 'jobs' table
    # This query calculates the cosine distance between the resume and all jobs
    sql = text("""
        SELECT id, title, company, description, 1 - (embedding <=> :resume_embedding) AS match_score
        FROM jobs
        ORDER BY embedding <=> :resume_embedding
        LIMIT :limit;
    """)

    matches = conn.execute(
        sql, {"resume_embedding": resume_embedding, "limit": limit}
    ).fetchall()
    
    conn.close()
    
    # Format the results into a list of dictionaries
    return [
        {
            "id": row[0],
            "title": row[1],
            "company": row[2],
            "description": row[3],
            "match_score": row[4],
        }
        for row in matches
    ]