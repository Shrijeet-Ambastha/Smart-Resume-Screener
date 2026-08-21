import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def save_resume(filename, resume_text, job_description, ai_result):

    connection = psycopg2.connect(
        DATABASE_URL,
        client_encoding="UTF8"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO resumes
        (filename, resume_text, job_description, ai_result)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (
            filename,
            resume_text,
            job_description,
            ai_result
        )
    )

    resume_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return resume_id