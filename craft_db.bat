@echo off
call %CD%\.win\Scripts\activate.bat
python %CD%\craft_db_all.py "auto"
pause