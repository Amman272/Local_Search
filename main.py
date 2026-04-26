import os
import sys
import Ocr
import token_gen
import sql

def main():
    sql.init_db()
    
    # allow providing folder path via arguments, else default
    folder_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\amman\Desktop\reader\testing"
    
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        
        # extract text first before creating file DB records
        try:
            text = Ocr.text_extraction(full_path)
        except Exception:
            text = ""
            
        if not text:
            print(f"Skipping {file_name} - no text extractable")
            continue
            
        # generating hash id for all files
        file_id = sql.Files(file_name)
        
        words = token_gen.tokens(text)
        print(words)
        
        for word in words:
            sql.tokensation(file_id, word)
            
        sql.commit()
        print(f"file {file_name} completed")
        
    print("Indexing completed.\n")
    
    while True:
        try:
            search_input = input("enter the words you want to search (or 'exit' to quit): ")
        except EOFError:
            break
            
        if search_input.lower() == 'exit':
            break
            
        search_words = search_input.lower().split()

        if len(search_words) == 0:
            print("please enter at least one word")
            continue

        result = sql.search(search_words)

        if len(result) == 0:
            print("no file found")
        else:
            print("\nfiles found:\n")
            for file in result:
                found_path = os.path.join(folder_path, file[0])
                print(f"{found_path} | score: {file[1]}")
                
        choice = input("\ndo you want to search again? (yes/no): ").lower()
        if choice in ["no", "n"]:
            break

if __name__ == "__main__":
    main()
