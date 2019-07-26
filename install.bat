@echo off
goto check_Permissions

:check_Permissions
    echo Caster: Administrative permissions required to setup Natlink. Detecting permissions...

    net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Success: Administrative permissions confirmed.
    ) else (
        echo Failure: Current permissions inadequate restart install.bat with administrator privileges...
	pause >nul
    )

set currentpath=%~dp0
echo Installation path: %currentpath%

cd C:\Python27

echo Installing caster dependencies
python -m pip install -r "%currentpath%requirements.txt"

IF EXIST "C:\NatLink\" (
echo Setting natlink user directory
python C:\NatLink\NatLink\confignatlinkvocolaunimacro\natlinkconfigfunctions.py -e

echo Setting natlink user directory
python C:\NatLink\NatLink\confignatlinkvocolaunimacro\natlinkconfigfunctions.py -n "%currentpath:~0,-1%"
)

echo Caster installed at %currentpath%

pause 1
