import easyocr

# Create reader (English)
reader = easyocr.Reader(['en'])

# Read text from image
result = reader.readtext(r'C:\Users\amman\Downloads\iNTERNSHIP-POSTER-new-scaled.jpg')

# Print results
for (bbox, text, prob) in result:
    print(f" {text} ")