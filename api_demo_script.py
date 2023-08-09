from multiprocessing import Process
import subprocess

def run_api(path= "."):
    subprocess.run(["uvicorn", "deployment.app.api:app", "--reload", "--port" ," 8000"])

def run_fronend(path = "."):
    subprocess.run(["streamlit", "run", "streamlit.py"], cwd=path)

if __name__ == "__main__":
    api = Process(target=run_api)
    api.start()
    frontend = Process(target=run_fronend, kwargs={"path": "deployment/app"})
    frontend.start()
    api.join()
    frontend.join()

