@echo off
echo Installing: dragonfly2, wxPython, pillow

cd c:\python27\scripts
pip install setuptools
pip install dragonfly2
pip install -U wxPython
pip install pillow
pip install toml



echo ------------------------------------------
echo Caster Dependencies Installation Complete
echo ------------------------------------------

pause