; Caster Dependencies Installer
; – – – – – – – – – – – – – – – – – – 
; This installs NirCmd and pip python dependencies.

[Setup]
AppName=Caster Dependencies
AppVersion=0.3
DefaultDirName={drive:C:}\NatLink\NatLink\MacroSystem\bin
DefaultGroupName=Caster Dependencies
DirExistsWarning=no
OutputDir=inst

[Files]
Source: "dependencies\*.*"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\pip.bat"