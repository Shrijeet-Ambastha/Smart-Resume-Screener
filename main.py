from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from backend.database.mongodb import save_resume
from backend.services.llm_services import match_resume
import pdfplumber
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

app = FastAPI()


@app.get("/")
def home():
    return FileResponse(
        os.path.join("frontend", "index.html")
    )


@app.get("/style.css")
def style():
    return FileResponse(
        os.path.join("frontend", "style.css")
    )


def extract_text(file_path):

    text = ""

    if file_path.endswith(".pdf"):

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    elif file_path.endswith(".txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

    return text
@app.post("/screen")
async def screen_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(""),
    job_file: UploadFile = File(None)
):

    try:

        os.makedirs("uploads", exist_ok=True)

        resume_path = os.path.join(
            "uploads",
            resume.filename
        )

        with open(resume_path, "wb") as file:
            file.write(await resume.read())

        resume_text = extract_text(resume_path)

        final_job_description = job_description

        if job_file:

            job_file_path = os.path.join(
                "uploads",
                job_file.filename
            )

            with open(job_file_path, "wb") as file:
                file.write(await job_file.read())

            final_job_description = extract_text(
                job_file_path
            )

        if not final_job_description:

            raise HTTPException(
                status_code=400,
                detail="Job description is required"
            )

        ai_result = match_resume(
            resume_text,
            final_job_description
        )

        resume_id = save_resume(
            resume.filename,
            resume_text,
            final_job_description,
            ai_result
        )

        return {
            "id": resume_id,
            "candidate": resume.filename,
            "resume_text": resume_text,
            "job_description": final_job_description,
            "ai_result": ai_result
        }

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )