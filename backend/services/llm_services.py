from google import genai
from dotenv import load_dotenv
import os

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

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)


import time
from google import genai
from dotenv import load_dotenv
import os

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

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)


def match_resume(resume_text, job_description):

    prompt = f"""
You are an AI resume screening assistant.

Compare the candidate resume with the job description.

Evaluate:

1. Technical skills
2. Relevant experience
3. Education
4. Missing skills
5. Overall suitability

Give a match score from 1 to 10.

Return the result in this format:

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

    for attempt in range(4):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < 3:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    return "Gemini is currently busy. Please try screening again in a few minutes."

            else:

                raise e