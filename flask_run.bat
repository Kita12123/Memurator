@echo off
H:
cd H:\M_Emurator
call %CD%\.venv\Scripts\activate.bat
python %CD%\flask_run.py
pause