from pathlib import Path
import easyocr
import fitz
from docx import Document
reader = easyocr.Reader(['en'])
def text_extraction(full_path):
    suffix = Path(full_path).suffix.lower()
    try:
       
        if suffix == ".jpeg" or suffix == ".png " or suffix == ".jpg":
            print("processssing images")
            reader = easyocr.Reader(['en'])
            result = reader.readtext(full_path)
            text = " ".join([item[1] for item in result])   
            text = text.replace("\n", " ").strip()
            print (text)
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