; Element Prerequisites Installer
; – – – – – – – – – – – – – – – – – – 
; This installs prerequisites for Element programming assistant.

[Setup]
AppName=Element Prerequisites Installer
AppVersion=0.1
DefaultDirName={drive:C:}\temp\bottle_and_cherrypy
DefaultGroupName=Element Prerequisites Installer
DirExistsWarning=no
OutputDir=installer_requirements\output

[Files]
Source: "old\installer\*.*"; DestDir: "{app}";Flags: replacesameversion recursesubdirs

[Run]
Filename: "{app}\install_bottle.bat"
Filename: "{app}\CherryPy-3.2.4\install_cherry.bat"