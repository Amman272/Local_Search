from pathlib import Path
import re

stopwords = {
    "the", "is", "at", "on", "by", "be", "can", "only", "a", "an", "and", 
    "or", "in", "of", "to", "for", "with", "as", "it", "this", "that"
}

def tokens(text):
    text= text.lower()
    words=re.findall(r'\b[a-z]+\b',text)
    filtered=[]
    for word in words:
        if word not in stopwords:
            filtered.append(word)
    return filtered