@echo off
echo Running DNS/DPI from Dragonfly CLI with Natlink.

set currentpath=%~dp0

TITLE Caster: Status Window
python -m dragonfly load --engine natlink _*.py --no-recobs-messages

pause 1