START C:\NatLink\NatLink\MacroSystem\bin\PSTools\pskill.exe natspeak.exe
START C:\NatLink\NatLink\MacroSystem\bin\PSTools\pskill.exe dgnuiasvr_x64.exe
START C:\NatLink\NatLink\MacroSystem\bin\PSTools\pskill.exe dnsspserver.exe
echo.
echo Waiting For Several Seconds... 
TIMEOUT /T 2 /NOBREAK
START "Dragon death and rebirth" "C:\Program Files (x86)\Nuance\NaturallySpeaking12\Program\natspeak.exe"
