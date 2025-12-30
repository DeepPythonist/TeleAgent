import os
import sys
import subprocess
import venv

def create_venv():
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        venv.create("venv", with_pip=True)

def install_requirements():
    pip_executable = os.path.join("venv", "bin", "pip")
    if sys.platform == "win32":
        pip_executable = os.path.join("venv", "Scripts", "pip")
        
    print("Installing requirements...")
    subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])

def run_bot():
    python_executable = os.path.join("venv", "bin", "python")
    if sys.platform == "win32":
        python_executable = os.path.join("venv", "Scripts", "python")
        
    print("Starting bot...")
    subprocess.call([python_executable, "main.py"])

def main():
    create_venv()
    install_requirements()
    run_bot()

if __name__ == "__main__":
    main()
