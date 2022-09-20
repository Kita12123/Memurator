@echo off
call %CD%\.win\Scripts\activate.bat
python %CD%\craft_db.py "auto"