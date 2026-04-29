import os
from pathlib import Path
import pytesseract
import fitz
from docx import Document
import shutil

TESSERACT_AVAILABLE = False
tesseract_path = shutil.which("tesseract")

if not tesseract_path:
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe")
    ]
    for p in common_paths:
        if os.path.exists(p):
            tesseract_path = p
            break

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    TESSERACT_AVAILABLE = True

def text_extraction(full_path):
    suffix = Path(full_path).suffix.lower()
    try:
        if suffix in [".jpeg", ".png", ".jpg"]:
            if not TESSERACT_AVAILABLE:
                print(f"Skipping {full_path} - Tesseract OCR not installed.")
                return ""
            print("processing images with tesseract")
            from PIL import Image
            img = Image.open(full_path)
            text = pytesseract.image_to_string(img)
            text = text.replace("\n", " ").strip()
            print(text)
            return text
        elif suffix == ".pdf":
            doc=fitz.open(full_path)
            text=""
            for page in doc:
                text+=page.get_text()
            return text.strip()
        elif suffix ==".docx":
            doc = Document(full_path)
            text = ""

            for para in doc.paragraphs:
                text += para.text + " "

            return text.strip()
    except Exception as e:
        print(e)
        return ""