import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "data/uploads"
SAMPLES_DIR = "data/samples"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    file_path = os.path.join(UPLOAD_DIR, upload_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def get_sample_path(student_id: str) -> str:
    # Look for .png or .jpg in samples
    for ext in [".png", ".jpg", ".jpeg"]:
        path = os.path.join(SAMPLES_DIR, f"{student_id}{ext}")
        if os.path.exists(path):
            return path
    return ""
