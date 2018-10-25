@echo off
echo Uninstall dragonfly2, wxPython, pillow, six, pyperclip, pillow, pywin32
echo ####
echo #### Warning! Only uninstall dependencies that are no longer used for all Python projects.
echo ####

cd c:\python27\scripts
pip uninstall dragonfly2
pip uninstall wxPython
pip uninstall pillow
pip uninstall six
pip uninstall pyperclip
pip uninstall pillow
pip uninstall pywin32
pip uninstall toml

echo ------------------------------------------
echo Caster Dependencies Uninstall Complete
echo ------------------------------------------

pause