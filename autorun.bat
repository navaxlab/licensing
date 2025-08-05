@echo off
set /p url=Paste MorphoSource URL: 
set /p nvx=Enter NVX code: 
python generate_all.py %url% %nvx%
pause
