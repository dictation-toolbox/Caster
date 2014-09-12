; DSExecutables
; – – – – – – – – – – – – – – – – – – 
; This installs the executables that I depend on.

[Setup]
AppName=DSExecutables
AppVersion=0.2
DefaultDirName={drive:C:}\NatLink\NatLink\MacroSystem\bin
DefaultGroupName=DSExecutables
DirExistsWarning=no
OutputDir=installer_requirements\output

[Files]
Source: "bin\*.*"; Excludes: "\data, \inno, \media, \misc, \py2exe, monitors.txt"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\Switcher.exe"