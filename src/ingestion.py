import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def fetch_candidates():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json", scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("Candidate Input (Responses)").sheet1

    data = sheet.get_all_records()
    return pd.DataFrame(data)