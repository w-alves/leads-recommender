import os

# Script used to generate executable
os.system('cmd /c "python -m pip install -U pip"')
os.system('cmd /c "pip install -r requirements.txt"')
os.system('cmd /k "streamlit run app.py"')