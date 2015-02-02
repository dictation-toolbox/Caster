; Caster Installer
; – – – – – – – – – – – – – – – – – – 
; This installs Caster

[Setup]
AppName=Caster
AppVersion=0.3
DefaultDirName={drive:C:}\temp\caster
DefaultGroupName=Caster
DirExistsWarning=no
OutputDir=inst

[Files]
Source: "caster.bat"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\caster.bat"