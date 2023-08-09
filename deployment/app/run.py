import subprocess
import os
from multiprocessing import Process


current_dir = os.path.dirname(__file__)

def start_api(path = "."):
    subprocess.run(["uvicorn", "api:app", "--reload", "--port" ," 8000"])

def start_frontend(path = "."):
    subprocess.run(["streamlit", "run", "streamlit.py"], cwd=path)

def run_web():
    path = os.path.realpath(os.path.dirname(__file__))
    api = Process(target=start_api, kwargs={'path': path})
    api.start()
    frontend = Process(target=start_frontend, kwargs={'path': path})
    frontend.start()
    api.join()
    frontend.join()
