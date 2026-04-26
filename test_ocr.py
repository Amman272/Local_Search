import sys
sys.path.append(r"c:\Users\amman\Desktop\reader")
import Ocr

try:
    print("starting test")
    img_path = r"c:\Users\amman\Desktop\reader\testing\IMG_20231230_150416.jpg"
    text = Ocr.text_extraction(img_path)
    print("Extracted Length:", len(text) if text else "None")
    print("Excerpt:", text[:100] if text else "None")
except Exception as e:
    import traceback
    traceback.print_exc()
