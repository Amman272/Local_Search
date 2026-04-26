from pathlib import Path
import easyocr
import Ocr
import re
text=''
stopwords = {"the", "is", "at", "on", "by", "be", "can", "only"}
def text_extraction(full_path):
    suffix = Path(full_path).suffix.lower()
    text=Ocr.text_extraction(full_path)
   # print(text)
    return text
   
def tokens(text):
    text= text.lower()
    words=re.findall(r'\b[a-z]+\b',text)
    filtered=[]
    for word in words:
        if word not in stopwords:
            filtered.append(word)
    return filtered