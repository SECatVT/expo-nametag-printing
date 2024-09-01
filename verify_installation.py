import os
import subprocess
import sys

def check_python_version():
    print("Checking Python version...")
    python_version = sys.version
    if python_version.startswith("3"):
        print(f"Python version is {python_version.split()[0]}: OK")
    else:
        print(f"Python version is {python_version.split()[0]}: FAILED (Python 3.x.x required)")
    print()

def check_git_version():
    print("Checking Git installation...")
    try:
        git_version = subprocess.check_output(["git", "--version"]).decode("utf-8").strip()
        print(f"{git_version}: OK")
    except Exception as e:
        print("Git is not installed or not found in PATH: FAILED")
        print(f"Error: {e}")
    print()

def check_dymo_sdk():
    print("Checking DYMO SDK installation...")
    try:
        import win32com.client
        dymo = win32com.client.Dispatch("Dymo.DymoAddIn")
        print(f"DYMO SDK detected: OK")
    except ImportError as e:
        print("DYMO SDK is not installed or not correctly set up: FAILED")
        print(f"Error: {e}")
    except Exception as e:
        print("An error occurred while checking DYMO SDK: FAILED")
        print(f"Error: {e}")
    print()

def check_dymo_label_software():
    print("Checking DYMO Label Software installation...")
    try:
        if os.name == 'nt':
            software_path = os.path.join(os.getenv('ProgramFiles(x86)'), 'DYMO', 'DYMO Label Software', 'DLS.exe')
            if os.path.exists(software_path):
                print(f"DYMO Label Software found at {software_path}: OK")
            else:
                print("DYMO Label Software not found: FAILED")
        else:
            print("DYMO Label Software check is only supported on Windows: SKIPPED")
    except Exception as e:
        print("An error occurred while checking DYMO Label Software: FAILED")
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("Starting setup verification...\n")
    check_python_version()
    check_git_version()
    check_dymo_sdk()
    check_dymo_label_software()
    print("Setup verification completed.")
