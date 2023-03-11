
@echo off

SetLocal EnableDelayedExpansion
set python_version=3.10-32
set currentpath=%~dp0
echo Installation path: %currentpath%

@REM execute python launcher for python directory
FOR /F "tokens=1 USEBACKQ delims=" %%i IN (`py -%python_version% -c "import sys; print(sys.exec_prefix)"`) DO ( set python_path=%%i )

@REM  whack a funny trailing character (newline?) from end
set python_path=!python_path:~0,-1!

set PATH=%python_path%;%python_path%/Scripts;%PATH%
echo %PATH%

echo Next line should clearly state python version:
python --version

echo Using this python/pip:

py -%python_version% -m pip install --upgrade pip

echo Installing Caster Dependencies for DNS/WSR
py -%python_version% -m pip install -r "%currentpath%requirements.txt"

pause 1
