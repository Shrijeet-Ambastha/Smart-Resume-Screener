from backend.services.ollama_service import match_resume_with_ollama


resume = """
John Doe
Python Developer

Skills:
Python, Java, SQL, FastAPI, MongoDB

Experience:
Developed web applications using Python and FastAPI.
"""

job = """
We are looking for a Python Developer.

Requirements:
Python
FastAPI
SQL
MongoDB
REST APIs
"""

result = match_resume_with_ollama(
    resume,
    job
)

print("==============================")
print("OLLAMA RESULT")
print("==============================")
print(result)