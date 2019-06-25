taskkill /IM natspeak.exe /f /s localhost
taskkill /IM dgnuiasvr_x64.exe /f /s localhost
taskkill /IM dnsspserver.exe /f /s localhost
taskkill /IM dragonbar.exe /f /s localhost
sleep 1
start "" %1 /user %2


