@echo off
cd %CD%
call %CD%\.venv\Scripts\activate.bat
flask run --host 0.0.0.0
pause