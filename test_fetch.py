import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("Candidate Input (Responses)").sheet1

data = sheet.get_all_records()

for row in data:
    print(row)

from download_resume import download_resume

for row in data:
    path = download_resume(row['Resume Upload'], row['Name'])
    print("Downloaded:", path)

from src.parser import extract_text_from_pdf

# Test extraction on the last downloaded resume
if 'path' in locals():
    resume_text = extract_text_from_pdf(path)
    print("Extracted text preview:")
    print(resume_text[:1000])


from src.llm_evaluator import evaluate_resume

jd = "Looking for Python backend engineer with ML experience"

result = evaluate_resume(jd, resume_text)
print(result)