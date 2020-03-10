@echo off
echo Runnig Kaldi from Dragonfly CLI

set currentpath=%~dp0

TITLE Caster: Status Window
cmd /c python -m dragonfly load _*.py --engine kaldi  --no-recobs-messages --engine-options " \
    model_dir=kaldi_model_zamia \
    vad_padding_end_ms=300"

pause 1