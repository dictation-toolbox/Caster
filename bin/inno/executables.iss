; DSExecutables
; – – – – – – – – – – – – – – – – – – 
; This installs the executables that I depend on.

[Setup]
AppName=DSExecutables
AppVersion=0.1
DefaultDirName={drive:C:}\NatLink\NatLink\MacroSystem\exe
DefaultGroupName=DSExecutables
DirExistsWarning=no
OutputDir=installer_requirements\output

[Files]
Source: "exe\*.*"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\Switcher.exe"