@echo off
echo Running Test Engine from Dragonfly CLI.
echo(

set currentpath=%~dp0

TITLE Caster: Test Engine Window
echo --------------------------Instructions -------------------------
echo Type commands to emulate as if they are being dictated by voice. 
echo lowercase mimics `commands`, UPPERCASE mimics `free dictation`
echo Upper and lowercase words can be mixed e.g `say THIS IS A TEST` 
echo(
echo Edit the `--delay 3` in bat file to change command delay in seconds.
echo The delay allows user to switch to the relevant application to test commands
echo ----------------------------------------------------------------
echo(
echo(

python -m dragonfly test _caster.py --delay 3

pause 1
