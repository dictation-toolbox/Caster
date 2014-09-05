; Dragonfly Sorcery Installer
; – – – – – – – – – – – – – – – – – – 
; This installs Dragonfly Sorcery

[Setup]
AppName=Dragonfly Sorcery
AppVersion=0.3
DefaultDirName={drive:C:}\temp\dragonfly_sorcery
DefaultGroupName=Dragonfly Sorcery
DirExistsWarning=no
OutputDir=installer_requirements\output

[Files]
Source: "old\dragonfly_sorcery.bat"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\dragonfly_sorcery.bat"