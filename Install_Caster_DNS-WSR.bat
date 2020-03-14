@echo off
set currentpath=%~dp0
echo Installation path: %currentpath%

echo Installing Caster Dependencies for DNS/WSR
python -m pip install -r "%currentpath%requirements.txt"

pause 1