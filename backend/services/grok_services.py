import os
from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)


XAI_API_KEY = os.getenv("XAI_API_KEY")

if not XAI_API_KEY:
    raise ValueError("XAI_API_KEY is missing")


client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


def match_resume_with_grok(resume_text, job_description):

    prompt = f"""
You are an AI resume screening assistant.

Compare the candidate resume with the job description.

Evaluate:

1. Technical skills
2. Relevant experience
3. Education
4. Missing skills
5. Overall suitability

IMPORTANT:

The FIRST line MUST be:

Score: X/10

The score must be a number from 1 to 10.

Return exactly:

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

    print("================================")
    print("CALLING GROK")
    print("================================")

    response = client.chat.completions.create(
        model="grok-4.6",
        messages=[
            {
                "role": "system",
                "content": "You are an AI resume screening assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    if not result:
        raise Exception("Grok returned an empty response")

    print("================================")
    print("GROK RESPONSE RECEIVED")
    print("================================")

    print(result)

    return result