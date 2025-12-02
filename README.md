# Personal_OSINT
This project the based on some movie scenes like prison break, like when the Company want the 'Scylla' back so they have their own software which analyze the face of the person and searches all over the place. So basically I am just trying to make that project and its hard because I don't have that dataset to compare, but we can try to make this thing...


THE STEPS TO RUN THIS PROJECT IS:
man i dont know much things to write in this readme file but still u can find is usefull


This guide provides step-by-step instructions to set up the Kallen Sentinel OSINT project on a new computer.

Prerequisites

Before you begin, you must have the following software installed:

Python: This project was built using Python 3.10. You can download it from python.org.

IMPORTANT: During installation, check the box that says "Add Python to PATH".

Visual Studio C++ Build Tools: This is a critical requirement for the face_recognition library to work on Windows.

Go to the Visual Studio Build Tools download page.

Run the installer.

Select the "Desktop development with C++" workload.

Click "Install".

# Step 1: Set Up the Project

Create Your Project Folder: Create a new folder (e.g., C:\Projects\KallenSentinel).

Copy Project Files: Copy all your Python files (main.py, run_app.py, etc.) and the app folder into this new directory.

Open a Terminal: Open your command prompt or terminal and navigate into your project folder:

cd C:\Projects\KallenSentinel


# Step 2: Create a Virtual Environment (Recommended)

This keeps your project's libraries separate from your main system.

Create the environment:

python -m venv venv


Activate the environment:

.\venv\Scripts\activate


(Your terminal prompt should now show (venv) at the beginning).

# Step 3: Install All Project Libraries

You can install the libraries one-by-one (Method A) or all at once using the requirements.txt file (Method B).

Method A: Install All at Once (Easy Way)

Make sure you have the requirements.txt file (which we created) in your project folder.

Run this single command:

pip install -r requirements.txt


Method B: Install Manually (Step-by-Step)

If you don't have the requirements.txt file, run these commands one after another.

Install Streamlit (The UI):

pip install streamlit


Install Core AI/Scraping Libraries:

pip install requests Pillow numpy


Install PDF Generator:

pip install fpdf2


Install face_recognition (Requires C++ Tools):

First, install CMake and dlib, which are required:

pip install cmake
pip install dlib


Now, install the main library:

pip install face_recognition


Install Playwright (The Web Scraper):

pip install playwright


# Step 4: Install Playwright's Browsers

The playwright library needs its own web browsers to work.

Run this command to download the necessary browser (Chromium):

playwright install


(This might take a minute or two to download).

Step 5: Run the Application

After all steps are complete, you can launch the Kallen Sentinel application.

Make sure you are in your project folder (C:\Projects\KallenSentinel) and your virtual environment is active ((venv)).

Run the following command:

streamlit run main.py


Your web browser should automatically open to http://localhost:8501, showing the app interface.