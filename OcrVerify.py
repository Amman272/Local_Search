import pymupdf  as pdf
from docx import Document
from pathlib import Path
def Verification(file_path):
    #print("running")
    suffix = Path(file_path).suffix.lower()
    if suffix == ".docx":
        return True
    elif suffix == ".pdf":
        doc=pdf.open(file_path)
        for page in doc:
            text=page.get_text()
           ## print("checking")
            if text:
                return True
        return False
    else:
        return False
    