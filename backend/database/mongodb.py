import os
import re
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        client_encoding="UTF8"
    )


def extract_score(ai_result):

    match = re.search(
        r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10",
        ai_result,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return None


def save_resume(
    filename,
    resume_text,
    job_description,
    ai_result,
    match_score
):

    connection = get_connection()
    cursor = connection.cursor()

    match_score = extract_score(ai_result)

    cursor.execute(
        """
        INSERT INTO resumes
        (
            filename,
            resume_text,
            job_description,
            ai_result,
            match_score
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            filename,
            resume_text,
            job_description,
            ai_result,
            match_score
        )
    )

    resume_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return resume_id


def get_shortlisted():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            match_score,
            created_at
        FROM resumes
        WHERE match_score >= 7
        ORDER BY match_score DESC, created_at DESC;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    shortlisted = []

    for row in rows:

        shortlisted.append({
            "id": row[0],
            "filename": row[1],
            "match_score": float(row[2]),
            "created_at": row[3].isoformat()
        })

    return shortlisted