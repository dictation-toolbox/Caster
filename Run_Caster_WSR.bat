@echo off
echo Running WRS from Dragonfly CLI.

set currentpath=%~dp0

TITLE Caster: Status Window
cmd /c python -m dragonfly load --engine sapi5inproc _*.py --no-recobs-messages

pause 1
