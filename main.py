from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from backend.database.mongodb import save_resume, get_shortlisted
from backend.services.llm_services import match_resume
import pdfplumber
import os
import re
from openpyxl import Workbook

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


def extract_score(ai_result):

    match = re.search(
        r"Score\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10",
        ai_result,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return 0


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

        match_score = extract_score(ai_result)

        resume_id = save_resume(
            resume.filename,
            resume_text,
            final_job_description,
            ai_result,
            match_score
        )

        return {
            "id": resume_id,
            "candidate": resume.filename,
            "match_score": match_score,
            "shortlisted": match_score > 7,
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


@app.get("/shortlisted")
def shortlisted_students():

    try:

        students = get_shortlisted()

        return {
            "count": len(students),
            "students": students
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/download-excel")
def download_excel():

    try:

        students = get_shortlisted()

        workbook = Workbook()
        sheet = workbook.active

        sheet.title = "Shortlisted Students"

        sheet.append([
            "Candidate",
            "Match Score",
            "Created At"
        ])

        for student in students:

            sheet.append([
                student["filename"],
                student["match_score"],
                student["created_at"]
            ])

        os.makedirs("uploads", exist_ok=True)

        excel_path = os.path.join(
            "uploads",
            "shortlisted_students.xlsx"
        )

        workbook.save(excel_path)

        return FileResponse(
            excel_path,
            filename="shortlisted_students.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )