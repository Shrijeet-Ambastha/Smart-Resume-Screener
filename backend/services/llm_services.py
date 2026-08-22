# import os
# import time
# from dotenv import load_dotenv
# from google import genai

# BASE_DIR = os.path.dirname(
#     os.path.dirname(
#         os.path.dirname(
#             os.path.abspath(__file__)
#         )
#     )
# )

# load_dotenv(os.path.join(BASE_DIR, ".env"))

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY is missing")

# client = genai.Client(api_key=api_key)


# def match_resume(resume_text, job_description):

#     prompt = f"""
# You are an AI resume screening assistant.

# Compare the candidate resume with the job description.

# Evaluate:

# 1. Technical skills
# 2. Relevant experience
# 3. Education
# 4. Missing skills
# 5. Overall suitability

# IMPORTANT INSTRUCTIONS:

# - Give a match score from 1 to 10.
# - The FIRST line of your response MUST be exactly in this format:
# Score: X/10
# - Replace X with the actual score.
# - Do not put any text before the Score line.
# - Do not use markdown formatting on the Score line.

# Then use exactly these sections:

# Score: X/10

# Matching Skills:
# - skill 1
# - skill 2

# Missing Skills:
# - skill 1
# - skill 2

# Strengths:
# - strength 1
# - strength 2

# Justification:
# Give a short explanation of why the candidate matches the job.

# Candidate Resume:
# {resume_text}

# Job Description:
# {job_description}
# """

#     for attempt in range(4):

#         try:

#             response = client.models.generate_content(
#                 model="gemini-3.6-flash",
#                 contents=prompt
#             )

#             result = response.text.strip()

#             print("AI RESULT:")
#             print(result)

#             return result

#         except Exception as e:

#             error_message = str(e)

#             if "503" in error_message or "UNAVAILABLE" in error_message:

#                 if attempt < 3:

#                     wait_time = 2 ** attempt

#                     print(
#                         f"Gemini temporarily unavailable. "
#                         f"Retrying in {wait_time} seconds..."
#                     )

#                     time.sleep(wait_time)

#                 else:

#                     return (
#                         "Gemini is currently busy. "
#                         "Please try screening again in a few minutes."
#                     )

#             else:

#                 raise e


import os
import time
from dotenv import load_dotenv
from google import genai

#from backend.services.ollama_service import match_resume_with_ollama


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
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(
    api_key=api_key
)


def match_resume(resume_text, job_description):

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

    try:

        print("================================")
        print("CALLING GEMINI")
        print("================================")

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print("Gemini successful")

        return response.text

    except Exception as gemini_error:

        error_message = str(gemini_error)

        print("Gemini failed:")
        print(error_message)

        print("================================")
        print("SWITCHING TO OLLAMA")
        print("================================")

        try:

            result = match_resume_with_ollama(
                resume_text,
                job_description
            )

            print("Ollama successful")

            return result

        except Exception as ollama_error:

            print("Ollama also failed:")
            print(str(ollama_error))

            raise Exception(
                "Both Gemini and Ollama failed. "
                f"Gemini: {gemini_error} | "
                f"Ollama: {ollama_error}"
            )