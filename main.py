import os
import sys
import Ocr
import token_gen
import sql

sql.init_db()


def indexing(folder_path=None, progress_callback=None):
    if folder_path is None:
        folder_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\amman\Desktop\reader\testing"   
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return
        
    files = os.listdir(folder_path)
    total_files = len(files)
    for idx, file_name in enumerate(files):
        full_path = os.path.join(folder_path, file_name)
        try:
            text = Ocr.text_extraction(full_path)
        except Exception:
            text = ""

        if not text:
            print(f"Skipping {file_name} - no text extractable")
            continue

        # generating hash id for all files
        file_id = sql.Files(full_path)

        words = token_gen.tokens(text)
        print(words)

        for word in words:
            sql.tokensation(file_id, word)

        sql.commit()
        print(f"file {file_name} completed")
        if progress_callback:
            progress_callback(idx + 1, total_files, file_name)

    print("Indexing completed.\n")
    return True
def searching():
        try:
            search_input = input("enter the words you want to search (or 'exit' to quit): ")
        except EOFError:
            return
            
        if search_input.lower() == 'exit':
            return
            
        search_words = search_input.lower().split()

        if len(search_words) == 0:
            print("please enter at least one word")
        

        result = sql.search(search_words)

        if len(result) == 0:
            print("no file found")
        else:
            print("\nfiles found:\n")
            for file in result:
                found_path = os.path.join(folder_path, file[0])
                print(f'"{found_path}" | score: {file[1]}')
                
        
