Smart Resume Screener

An AI-powered resume screening system that compares candidate resumes with a given job description and generates an AI-based suitability score. The system stores screening results in a cloud PostgreSQL database and provides shortlisted candidates based on a configurable score threshold.

Features
Upload candidate resume in PDF/TXT format
Upload or enter a job description
Extract resume text automatically
AI-based resume and job-description matching
Match score from 1–10
Identifies:
Matching Skills
Missing Skills
Strengths
Justification
Stores screening results in Supabase PostgreSQL
Shortlists candidates with match score ≥ 7
REST API using FastAPI
Deployable on Render
Gemini API integration with retry handling for temporary failures

System Architecture
                 ┌─────────────────────┐
                 │       User           │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Frontend UI       │
                 │ HTML + CSS + JS      │
                 └──────────┬──────────┘
                            │
                     Upload Resume
                     + Job Description
                            │
                            ▼
                 ┌─────────────────────┐
                 │     FastAPI         │
                 │      main.py        │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        ┌─────────────────┐   ┌─────────────────┐
        │ PDF/TXT Parser  │   │ Job Description │
        │   pdfplumber    │   │     Parser      │
        └────────┬────────┘   └────────┬────────┘
                 │                     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Gemini LLM       │
                 │  Resume Screening   │
                 └──────────┬──────────┘
                            │
                    AI Screening Result
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Supabase PostgreSQL │
                 │      resumes        │
                 └──────────┬──────────┘
                            │
                    match_score >= 7
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Shortlisted         │
                 │ Candidates          │
                 └─────────────────────┘