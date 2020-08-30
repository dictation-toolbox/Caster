@echo off
echo Running Kaldi from Dragonfly CLI

set currentpath=%~dp0

TITLE Caster: Status Window
python -m dragonfly load _*.py --engine kaldi  --no-recobs-messages

pause 1
