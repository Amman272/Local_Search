import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog
import sql
import main
import Ocr

st.set_page_config(page_title="Local File Search", layout="wide")

# Inject Material Symbols
st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />', unsafe_allow_html=True)

# CSS Styling
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Search Bar Fix */
    [data-testid="stTextInput"] > div {
        background-color: transparent !important;
    }
    [data-baseweb="input"] {
        border-radius: 30px !important;
        border: 2px solid #333 !important;
        background-color: #1e1e1e !important;
        overflow: hidden !important;
    }
    [data-baseweb="input"] > div {
        background-color: transparent !important;
    }
    [data-testid="stTextInput"] input {
        padding: 12px 20px !important;
        font-size: 18px !important;
        color: #fff !important;
        background-color: transparent !important;
    }

    /* Result Box Container */
    .result-box {
        border: 2px solid #333;
        border-radius: 15px;
        padding: 20px; /* Added padding */
        margin-bottom: 15px;
        background-color: #1e1e1e; /* Darker box */
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out;
    }
    
    .result-box:hover {
        transform: translateY(-5px);
        box-shadow: 5px 5px 0px #000;
        border-color: #555;
    }

    /* Icons */
    .material-symbols-outlined {
        font-size: 28px;
        vertical-align: middle;
        margin-right: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 20px !important;
        border: 2px solid #333 !important;
        background-color: #1e1e1e !important;
        color: #fff !important;
        transition: all 0.2s !important;
        padding: 10px 20px !important;
    }
    
    .stButton > button:hover {
        background-color: #fff !important;
        color: #000 !important;
        transform: scale(1.05) !important;
        border-color: #fff !important;
    }

    /* Hide Streamlit Defaults */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory(master=root)
    root.destroy()
    return folder_path

def open_file(path):
    try:
        os.startfile(path)
    except Exception as e:
        st.error(f"Error opening file: {e}")

has_files = sql.check_has_files()

if not has_files:
    if not getattr(Ocr, 'TESSERACT_AVAILABLE', True):
        st.warning("⚠️ Tesseract OCR is not installed on this system. Image files will be skipped during indexing.")
        
    st.markdown("<h1 style='text-align: center; margin-top: 10%;'>File Search Indexer</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #aaa; margin-bottom: 30px;'>No files indexed yet. Please select a folder to begin.</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Select Folder to Index", use_container_width=True):
            folder_path = select_folder()
            if folder_path:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total, filename):
                    progress_bar.progress(current / total)
                    status_text.markdown(f"<p style='text-align: center; color: #888;'>Indexing {current}/{total}: <strong>{filename}</strong></p>", unsafe_allow_html=True)

                with st.spinner("Indexing files..."):
                    main.indexing(folder_path, update_progress)
                st.success("Indexing completed!")
                st.rerun()
else:
    # Header area with Title and New Folder Button
    col_empty, col_title, col_btn = st.columns([1, 4, 1])
    with col_title:
        st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>Search Your Files</h1>", unsafe_allow_html=True)
        current_dir = sql.get_current_directory()
        if current_dir:
            st.markdown(f"<p style='text-align: center; color: #888; font-size: 14px;'>Current Index: {current_dir}</p>", unsafe_allow_html=True)
            
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("New Folder", use_container_width=True):
            sql.clear_db()
            st.rerun()
    
    # Big Search Bar
    search_query = st.text_input("Type to search...", key="search_query")
    
    # View Toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        view_mode = st.radio("View Mode", ["List", "Grid"], horizontal=True, label_visibility="collapsed")

    if search_query:
        words = search_query.lower().split()
        if len(words) > 0:
            results = sql.search(words)
            if not results:
                st.warning("No files found matching your search.")
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                if view_mode == "List":
                    for file_path, score in results:
                        ext = os.path.splitext(file_path)[1].lower()
                        icon = "draft"
                        if ext == ".pdf":
                            icon = "picture_as_pdf"
                        elif ext == ".docx" or ext == ".doc":
                            icon = "description"
                        elif ext == ".txt":
                            icon = "article"

                        filename = os.path.basename(file_path)
                        
                        col_box, col_btn = st.columns([5, 1])
                        with col_box:
                            st.markdown(f"""
                            <div class="result-box">
                                <div><span class="material-symbols-outlined">{icon}</span><strong style="font-size: 18px; vertical-align: middle;">{filename}</strong></div>
                                <div style='color: #888; margin-top: 8px; font-size: 13px;'>Word Frequency: {score} | {file_path}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_btn:
                            st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True) # Spacer to align
                            if st.button("Open", key=f"btn_{file_path}", use_container_width=True):
                                open_file(file_path)
                else:
                    # Grid View
                    cols = st.columns(3)
                    for i, (file_path, score) in enumerate(results):
                        ext = os.path.splitext(file_path)[1].lower()
                        icon = "draft"
                        if ext == ".pdf":
                            icon = "picture_as_pdf"
                        elif ext == ".docx" or ext == ".doc":
                            icon = "description"
                        elif ext == ".txt":
                            icon = "article"

                        filename = os.path.basename(file_path)
                        
                        with cols[i % 3]:
                            st.markdown(f"""
                            <div class="result-box" style="text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 180px;">
                                <span class="material-symbols-outlined" style="font-size: 50px; margin: 0 0 10px 0;">{icon}</span>
                                <div style="font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; width: 100%;" title="{filename}">{filename}</div>
                                <div style="font-size: 12px; color: #888; margin-top: 5px;">Word Frequency: {score}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("Open", key=f"grid_btn_{file_path}", use_container_width=True):
                                open_file(file_path)
                            st.markdown("<br>", unsafe_allow_html=True)