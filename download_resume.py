import os
from urllib.parse import urlparse, parse_qs
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from oauth2client.service_account import ServiceAccountCredentials

# Setup credentials for Google Drive API
scope = ["https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", scope
)
drive_service = build("drive", "v3", credentials=creds)

def extract_file_id(link):
    # Support multiple Google Drive URL formats:
    # - https://drive.google.com/file/d/<FILE_ID>/view
    # - https://drive.google.com/open?id=<FILE_ID>
    # - https://drive.google.com/uc?id=<FILE_ID>&export=download
    if "/d/" in link:
        parts = link.split("/d/")
        if len(parts) > 1 and parts[1]:
            return parts[1].split("/")[0]
    parsed = urlparse(link)
    qs = parse_qs(parsed.query)
    if "id" in qs and qs["id"]:
        return qs["id"][0]
    raise ValueError(f"Could not extract Google Drive file ID from link: {link}")

def download_resume(drive_link, name):
    file_id = extract_file_id(drive_link)
    
    os.makedirs("resumes", exist_ok=True)
    file_path = f"resumes/{name}.pdf"

    try:
        # Use Google Drive API to download
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.close()
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise ValueError(f"Failed to download file {file_id}: {e}")

    # Validate that we received a PDF
    if os.path.getsize(file_path) == 0:
        os.remove(file_path)
        raise ValueError(f"Downloaded file is empty")
    
    with open(file_path, "rb") as f:
        header = f.read(4)
    
    if not header.startswith(b"%PDF"):
        os.remove(file_path)
        raise ValueError(
            f"Downloaded file does not appear to be a valid PDF. "
            f"File header: {header}"
        )

    return file_path