from pathlib import Path
import pytesseract
import fitz
from docx import Document

# IMPORTANT: If Tesseract isn't in your system PATH, uncomment and set this line to your install location:
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\amman\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def text_extraction(full_path):
    suffix = Path(full_path).suffix.lower()
    try:
        if suffix in [".jpeg", ".png", ".jpg"]:
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