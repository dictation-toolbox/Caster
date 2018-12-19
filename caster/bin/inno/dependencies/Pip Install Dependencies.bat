@echo off
echo Installing: setuptools, future, dragonfly2, wxPython, pillow, toml

cd c:\python27\scripts
pip install setuptools
pip install future
pip install dragonfly2
pip install -U wxPython
pip install pillow
pip install toml



echo ------------------------------------------
echo Caster Dependencies Installation Complete
echo ------------------------------------------

pause