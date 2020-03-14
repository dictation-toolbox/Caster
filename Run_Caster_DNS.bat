@echo off
echo Runnig DNS/DPI from Dragonfly CLI with Natlink.

set currentpath=%~dp0

TITLE Caster: Status Window
cmd /c python -m dragonfly load --engine natlink _*.py --no-recobs-messages

pause 1