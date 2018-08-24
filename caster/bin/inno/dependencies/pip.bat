@echo off
echo Installing: pywin32, dragonfly, pillow, psutil, wmi

cd c:\python27\scripts
pip install pywin32
pip install wxpython
pip install dragonfly
pip install pillow
pip install psutil
pip install wmi

echo ------------------------------------------
echo Caster Dependencies Installation Complete
echo ------------------------------------------

pause