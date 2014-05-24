; Dragonfly Upgrade
; – – – – – – – – – – – – – – – – – – 
; This upgrades Dragonfly from 0.6.5 to 0.6.6b1.

[Setup]
AppName=Dragonfly 0.6.6b1 Upgrader
AppVersion=0.1
DefaultDirName={drive:C:}\Python27\Lib\site-packages\dragonfly
DefaultGroupName=Dragonfly 0.6.6b1 Upgrader Installer
DirExistsWarning=no
OutputDir=output

[Files]
; the dragonfly directory contains all of the 0.6.6b1 files from here: 
; https://code.google.com/p/dragonfly/source/browse/trunk#trunk%2Fdragonfly
Source: "dragonfly\*.*"; DestDir: "{app}";Flags: replacesameversion recursesubdirs