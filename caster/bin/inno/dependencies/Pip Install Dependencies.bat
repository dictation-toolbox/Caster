@echo off
echo Installing: setuptools, future, dragonfly2, wxPython, pillow, toml

cd c:\python27\scripts
pip install -U pip
pip install -U setuptools
pip install -U future
pip install -U dragonfly2
pip install -U wxPython
pip install -U pillow
pip install -U toml



echo ------------------------------------------
echo Caster Dependencies Installation Complete
echo ------------------------------------------

pause