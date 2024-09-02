# Engineering Expo Student Nametag Print Setup

## How To Use It
> I'm sure you'll figure it out.
> - Chen `23

## Pre-Requisites and Verification

Before you begin, make sure your system meets the following requirements and that you've downloaded and installed the necessary software. Each installation step is followed by verification instructions to ensure everything is working correctly.

### 1. Download and Install Visual Studio Code
Visual Studio Code (VS Code) is a powerful code editor that you'll use to write and manage your Python scripts. Download and install it from [here](https://code.visualstudio.com/).

**Installation Steps:**
  1. Visit the [Visual Studio Code download page](https://code.visualstudio.com/).
  2. Select your operating system (Windows, macOS, or Linux).
  3. Follow the installation prompts.

### 2. Download and Install Git
Git is a version control system that allows you to manage and keep track of your code changes. It’s essential for pulling the latest updates of the nametag printing script.

**Installation Steps:**
  1. Visit the [Git download page](https://git-scm.com/downloads).
  2. Select your operating system and download the installer.
  3. Follow the on-screen instructions to install Git.
  4. After installation, open a terminal or command prompt and type `git --version` to verify the installation.

### 3. Download and Install Python
Python is the programming language in which the nametag printing script is written. Ensure you download version 3.x.x, as it includes the necessary libraries and modules.

**Installation Steps:**
  1. Visit the [Python download page](https://www.python.org/downloads/).
  2. Select the latest Python 3.x.x version for your operating system.
  3. During installation, make sure to check the box that says "Add Python to PATH."
  4. Verify the installation by opening a terminal or command prompt and typing `py --version`
  5. Additionally, verify that `pip`, Python’s package installer, is working by running: `pip --version`

### 4. Install the DYMO SDK
The DYMO Software Development Kit (SDK) is required to communicate with the DYMO label printer from your Python script. 

**Installation Steps:**
  1. Download the SDK from [this link](https://www.dymo.com/support?cfid=online-support-sdk).
  2. Follow the installation instructions provided on the website.
  3. Make sure the SDK is properly installed and configured to work with your system.

### 5. Install the DYMO Label Software
The DYMO Label Software allows you to design and print labels. It also contains the drivers required for the DYMO label printer to function properly.

**Installation Steps:**
  1. Download the DYMO Label Software from [this link](https://download.dymo.com/dymo/Software/Win/DLS8Setup8.7.4.exe).
  2. Run the installer and follow the on-screen prompts to complete the installation.
  3. After installation, verify that the software can detect your DYMO label printer.

### 6. Install Python Dependencies
To ensure your Python environment is set up with all necessary dependencies, install the required Python packages.

**Installation Steps:**
  1. Open a terminal or command prompt in the directory containing the `requirements.txt` file.
  2. Run the following command: `pip install -r requirements.txt`

## Verify Setup Using a Python Script

You can use the following Python script to automate the verification of your setup by opening a terminal or command prompt in the root project directory and executing:
   ```bash
   py verify_setup.py
   ```

Alternatively, to just verify the DYMO configuration, complete the following steps: 
  1. Connect your DYMO printer to your computer.
  2. Open a terminal or command prompt.
  3. Run the following Python commands:

  ```python
  py
  >>> import win32com.client
  >>> dymo = win32com.client.Dispatch("Dymo.DymoAddIn")
  >>> print(dymo)
  ```

  - **Expected Output:**  
    If the SDK is installed correctly, you should not receive any import errors, and the `print(dymo)` command should return a COM object reference.





## Feature Demoed
- [x] Scan event registration ID and submit query an event participant on SwapCard API

- [x] Accept VT PID or email and query an event participant on SwapCard API

- [x] Backup input that organizes a customized event participant record

- [x] Manual overwrite grade level setting for an event participant

- [x] Dynamically log an event participant record to machine specfied Google worksheet

- [x] Dynamically merge all records to a master sheet sorted by record timestamp
