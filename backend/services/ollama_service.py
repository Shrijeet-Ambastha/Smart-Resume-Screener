import os
from dotenv import load_dotenv

load_dotenv()


def match_resume_with_ollama(resume_text, job_description):

    import ollama

    prompt = f"""
You are an AI resume screening assistant.

Compare the candidate resume with the job description.

Return:

Score: X/10

Matching Skills:
- skill 1
- skill 2

Missing Skills:
- skill 1
- skill 2

Strengths:
- strength 1
- strength 2

Justification:
Give a short explanation.

Candidate Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]