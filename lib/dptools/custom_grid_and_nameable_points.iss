; Custom Grid and Nameable Points
; – – – – – – – – – – – – – – – – – – 
; This installs some tools made by Doug Parent

[Setup]
AppName=Custom Grid and Nameable Points
AppVersion=0.1
DefaultDirName={drive:C:}\NatLink\NatLink\MacroSystem
DefaultGroupName=dp
DirExistsWarning=no
OutputDir=installer_requirements\output

[Files]
; Source
; discussion of these tools can be found here: 
; http://www.speechcomputing.com/node/3933
; http://www.speechcomputing.com/node/3932
Source: "argparse.py"; DestDir: "{app}";
Source: "CustomGrid.py"; DestDir: "{app}";
Source: "_keyCodes.py"; DestDir: "{app}";
Source: "_mycommon.py"; DestDir: "{app}";
Source: "_myclickLocations.py"; DestDir: "{app}";