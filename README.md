# AI Grader

This repository contains Python scripts to generate automated grading reports and draft feedback for student case study assignments. The grader relies on Google's **Gemini** API and a custom rubric provided in plain text.

## Contents

- `grader.py` – grades final submissions and outputs a DOCX report summarising rubric scores and reasoning.
- `draft_grader.py` – generates formative feedback for draft submissions without assigning a grade.
- `master_prompt.txt` – prompt template and rubric for the main grader.
- `draft_feedback_prompt.txt` – prompt for draft feedback.
- `feedback_review_prompt.txt` – prompt used to check the AI feedback against the student's submission.
- `grade_review_prompt.txt` – prompt used to double-check the fairness of the final grade.
- `grading_process.log` and `draft_grading_process.log` – example log files created by the scripts.
- `venv/` – Python virtual environment containing all dependencies (committed for portability).

## Requirements

The scripts expect Python 3.12 and the following packages:

```
dotenv
google-generativeai
python-docx
PyPDF2
PyYAML
```

A local virtual environment is included, but you can recreate one with `python -m venv venv` and install the packages manually.

## Configuration

1. Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY="YOUR_API_KEY"
```

2. Ensure the directories `input_assessments/` and `output_feedback/` exist in the repository root (they will be created automatically if missing). Place student files (`.docx` or `.pdf`) inside `input_assessments/`.

3. Adjust the prompt templates if required. Both contain a `{{STUDENT_SUBMISSION_TEXT_HERE}}` placeholder where the extracted student text is inserted.

## Usage

Run the main grader:

```bash
python grader.py
```
This script now performs an additional moderation pass to check that the assigned grade is fair. Any concerns are saved as a `_grade_review.txt` file next to the final DOCX report. If the review suggests a different overall grade (e.g. "grade should be B"), the report and summary CSV automatically use that revised grade.

For draft feedback instead of a final grade:

```bash
python draft_grader.py
```

`draft_grader.py` now also runs a second pass that compares the AI's feedback
with the student's original text. The result is saved as a `_feedback_review.txt`
file next to each DOCX report.

Each script processes all files in `input_assessments/` and writes DOCX reports to the appropriate output folder. Logs describing progress and any errors are written to `grading_process.log` or `draft_grading_process.log`.

## Grade Calculation

The overall grade in each report is derived from the rubric points returned by the AI. All points from `assistant_grade.breakdown` are summed (out of 30). Scores of **27–30** receive an **A**, **24–26** a **B**, **21–23** a **C**, and **18–20** a **D**. Anything below 18 is graded **E**.

Each DOCX report lists the grade suggested by the AI (`assistant_grade.overall_grade`) alongside the grade calculated from the rubric totals. If the two differ, the final grade shown is the one based on the rubric points and a short note explains that the grade was adjusted accordingly.

## Notes

- PDF text extraction uses `PyPDF2`; encrypted or malformed PDFs may fail.
- DOCX extraction now captures text inside tables.
- The repository currently includes a Windows-based `venv` directory which can be removed if you prefer to create your own environment.
- Automated tests are provided under the `tests/` directory. Run them with:

```bash
python -m pytest
```
- Each run of `draft_grader.py` also outputs a `_feedback_review.txt` file summarising any inaccuracies in the AI feedback or areas already addressed in the submission.
- Running `grader.py` performs a second pass to verify the grading. The result is saved as a `_grade_review.txt` file alongside each report, and a `grading_summary.csv` file summarises total points and grades.
