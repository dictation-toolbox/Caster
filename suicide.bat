START C:\NatLink\NatLink\MacroSystem\PSTools\pskill.exe natspeak.exe
START C:\NatLink\NatLink\MacroSystem\PSTools\pskill.exe dgnuiasvr_x64.exe
START C:\NatLink\NatLink\MacroSystem\PSTools\pskill.exe dnsspserver.exe
echo.
echo Waiting For One Hour... 
TIMEOUT /T 2 /NOBREAK
START "Dragon death and rebirth" "C:\Program Files (x86)\Nuance\NaturallySpeaking12\Program\natspeak.exe"
