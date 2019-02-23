; Dragonfly Upgrader
; – – – – – – – – – – – – – – – – – – 
; This upgrades Dragonfly from 0.6.5 to the most recent version from Github.

[Setup]
AppName=Dragonfly Github Upgrader
AppVersion=0.2
DefaultDirName={drive:C:}\temp\dragonfly
DefaultGroupName=Dragonfly Github Upgrader
DirExistsWarning=no
OutputDir=inst

[Files]
Source: "dragonfly_upgrade.bat"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\dragonfly_upgrade.bat"