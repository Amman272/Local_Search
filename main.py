import os
import sqlite3
import OcrVerify 
import token_gen
import sql
conn= sqlite3.connect("file_id.db")

cursor =conn.cursor()
#selecting file path and checking if ocr is available or not
#folder=input("enter the folder path")
folder_path = r"C:\Users\amman\Desktop\reader\testing"
for file_name in os.listdir(folder_path):
    #print(file_name)
    full_path = os.path.join(folder_path, file_name)
    result= OcrVerify.Verification(full_path)
   # print (result)
    # generating hash id for all files
    result=sql.Files(file_name)
   
    #sending files for ocr
    text= token_gen.text_extraction(full_path)
    if text ==None:
        continue
    text=token_gen.tokens(text)
    print (text)
    for words in text:
        sql.tokensation(file_name,words)
    conn.commit()
    print(f"file {file_name} completed")
    #indexing completed
while True:
    search = input("enter the words you want to search: ").lower().split()

    if len(search) == 0:
        print("please enter at least one word")
        continue

    result = sql.search(search)

    if len(result) == 0:
        print("no file found")
    else:
        print("\nfiles found:\n")
        for file in result:
            full_path = os.path.join(folder_path, file[0])
            print(f"{full_path} | score: {file[1]}")
    choice = input("\ndo you want to search again? (yes/no): ").lower()
    if choice == "no":
        break
