import subprocess
import time
import socket
import sys
import webbrowser

try:
    import webview
    HAVE_WEBVIEW = True
except ImportError:
    HAVE_WEBVIEW = False

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_streamlit():
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

if __name__ == '__main__':
    port = 8501
    
    # Start Streamlit server quietly in the background
    server_process = run_streamlit()
    
    # Wait for the server to spin up
    retries = 0
    while not check_port(port) and retries < 20:
        time.sleep(0.5)
        retries += 1

    if HAVE_WEBVIEW:
        # Create native desktop window
        window = webview.create_window('Local File Search', f'http://localhost:{port}', width=1000, height=800)
        webview.start()
        # Clean up the Streamlit server when the window is closed
        server_process.kill()
    else:
        # Fallback to normal web browser
        print("Native window unavailable. Opening in default browser...")
        webbrowser.open(f'http://localhost:{port}')
        print("Press Ctrl+C in this console to stop the server.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server_process.kill()
