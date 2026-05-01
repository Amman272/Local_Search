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

import ctypes
import os

class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('PerProcessUserTimeLimit', ctypes.c_int64),
        ('PerJobUserTimeLimit', ctypes.c_int64),
        ('LimitFlags', ctypes.c_uint32),
        ('MinimumWorkingSetSize', ctypes.c_size_t),
        ('MaximumWorkingSetSize', ctypes.c_size_t),
        ('ActiveProcessLimit', ctypes.c_uint32),
        ('Affinity', ctypes.c_size_t),
        ('PriorityClass', ctypes.c_uint32),
        ('SchedulingClass', ctypes.c_uint32),
    ]

class IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ('ReadOperationCount', ctypes.c_uint64),
        ('WriteOperationCount', ctypes.c_uint64),
        ('OtherOperationCount', ctypes.c_uint64),
        ('ReadTransferCount', ctypes.c_uint64),
        ('WriteTransferCount', ctypes.c_uint64),
        ('OtherTransferCount', ctypes.c_uint64),
    ]

class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('BasicLimitInformation', JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ('IoInfo', IO_COUNTERS),
        ('ProcessMemoryLimit', ctypes.c_size_t),
        ('JobMemoryLimit', ctypes.c_size_t),
        ('PeakProcessMemoryUsed', ctypes.c_size_t),
        ('PeakJobMemoryUsed', ctypes.c_size_t),
    ]

_job_handle = None

def assign_process_to_job(process):
    if os.name == 'nt':
        try:
            job = ctypes.windll.kernel32.CreateJobObjectW(None, None)
            if job:
                info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
                info.BasicLimitInformation.LimitFlags = 0x2000 # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                ctypes.windll.kernel32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))
                ctypes.windll.kernel32.AssignProcessToJobObject(job, int(process._handle))
                global _job_handle
                _job_handle = job
        except Exception:
            pass

def run_streamlit():
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    assign_process_to_job(process)
    return process

if __name__ == '__main__':
    port = 8501
    
    # Start Streamlit server quietly in the background
    server_process = run_streamlit()
    
    # Wait for the server to spin up
    retries = 0
    while not check_port(port) and retries < 20:
        time.sleep(0.5)
        retries += 1

    launched_native = False
    if HAVE_WEBVIEW:
        try:
            # Create native desktop window
            window = webview.create_window('Local File Search', f'http://localhost:{port}', width=1000, height=800)
            webview.start()
            # Clean up the Streamlit server when the window is closed
            server_process.kill()
            launched_native = True
        except Exception as e:
            print(f"Failed to launch native window due to missing dependencies: {e}")
            
    if not launched_native:
        # Fallback to normal web browser
        print("Native window unavailable. Opening in default browser...")
        webbrowser.open(f'http://localhost:{port}')
        print("Press Ctrl+C in this console to stop the server.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server_process.kill()
