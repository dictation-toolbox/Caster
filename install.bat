@echo off

set currentpath=%~dp0
echo Installation path: %currentpath%

cd C:\Python27

rem echo Installing caster dependencies
rem python -m pip install -r "%currentpath%requirements.txt"

echo Setting natlink user directory
python C:\NatLink\NatLink\confignatlinkvocolaunimacro\natlinkconfigfunctions.py -n "%currentpath:~0,-1%"

echo Caster installed at %currentpath%

pause 1