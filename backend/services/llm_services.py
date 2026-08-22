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

from backend.services.grok_service import match_resume_with_grok


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


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

IMPORTANT:

The FIRST line MUST be:

Score: X/10

The score must be a number from 1 to 10.

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
Give a short explanation of why the candidate matches the job.

Candidate Resume:
{resume_text}

Job Description:
{job_description}
"""

    # Try Gemini
    try:

        print("================================")
        print("Trying Gemini...")
        print("================================")

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        result = response.text

        print("Gemini succeeded.")

        return result

    except Exception as e:

        error_message = str(e)

        print("================================")
        print("GEMINI ERROR")
        print("================================")
        print(error_message)

        # Check Gemini quota error
        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
            or "Quota exceeded" in error_message
            or "quota" in error_message.lower()
        ):

            print("================================")
            print("GEMINI QUOTA EXCEEDED")
            print("SWITCHING TO GROK...")
            print("================================")

            try:

                result = match_resume_with_grok(
                    resume_text,
                    job_description
                )

                print("GROK FALLBACK SUCCESSFUL")

                return result

            except Exception as grok_error:

                print("================================")
                print("GROK ERROR")
                print("================================")
                print(str(grok_error))

                raise Exception(
                    "Gemini quota exceeded and Grok fallback failed: "
                    + str(grok_error)
                )

        # Gemini temporarily unavailable
        elif (
            "503" in error_message
            or "UNAVAILABLE" in error_message
        ):

            print("Gemini temporarily unavailable.")

            print("Switching to Grok...")

            try:

                return match_resume_with_grok(
                    resume_text,
                    job_description
                )

            except Exception as grok_error:

                raise Exception(
                    "Gemini unavailable and Grok fallback failed: "
                    + str(grok_error)
                )

        # Any other Gemini error
        else:

            print("Gemini failed.")

            print("Switching to Grok...")

            try:

                return match_resume_with_grok(
                    resume_text,
                    job_description
                )

            except Exception as grok_error:

                raise Exception(
                    "Gemini failed and Grok fallback failed: "
                    + str(grok_error)
                )