import ollama


def match_resume_with_ollama(resume_text, job_description):

    prompt = f"""
You are an AI resume screening assistant.

Compare the candidate resume with the job description.

IMPORTANT:
You MUST return a complete screening result.

The FIRST line MUST contain the match score exactly in this format:

Score: 8/10

The score must be a number from 1 to 10.

Then return exactly these sections:

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
Give a short explanation of why the candidate matches the job.

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