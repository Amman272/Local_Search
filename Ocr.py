from pathlib import Path
import easyocr
import fitz
from docx import Document
reader = easyocr.Reader(['en'])
def text_extraction(full_path):
    suffix = Path(full_path).suffix.lower()
    try:
       
        if suffix in [".jpeg", ".png", ".jpg"]:
            print("processing images")
            try:
                from PIL import Image
                import numpy as np
                img = Image.open(full_path)
                img.thumbnail((1200, 1200))
                img_array = np.array(img)
                result = reader.readtext(img_array)
            except Exception as inner_e:
                print(f"PIL resize failed ({inner_e}), falling back to direct load.")
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