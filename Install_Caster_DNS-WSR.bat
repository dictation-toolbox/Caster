@echo off
set currentpath=%~dp0
echo Installation path: %currentpath%
echo Using this python/pip:
py -m pip -V

echo Installing Caster Dependencies for DNS/WSR
py -m pip install -r "%currentpath%requirements.txt"

pause 1