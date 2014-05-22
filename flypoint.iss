; Flypoint Setup

[Setup]
AppName=Flypoint
AppVersion=0.1.60
DefaultDirName={drive:C:}\NatLink\NatLink\MacroSystem
DefaultGroupName=Flypoint Installer
DirExistsWarning=no
OutputDir=old\output

[Dirs]
Name: "{app}\exe"
Name: "{app}\languages"

[Files]
; GIT files
Source: "_global.py"; DestDir: "{app}";
Source: "_languagesccr.py"; DestDir: "{app}";
Source: "_serena.py"; DestDir: "{app}";
Source: "chrome.py"; DestDir: "{app}";
Source: "config.py"; DestDir: "{app}";
Source: "eclipse.py"; DestDir: "{app}";
Source: "paths.py"; DestDir: "{app}";
Source: "sh.py"; DestDir: "{app}";
; Note to self: Python remote debugging will have to be set up manually

; Language config files
Source: "languages\*.*"; DestDir: "{app}\languages";Flags: replacesameversion recursesubdirs

; Executables
Source: "exe\*.*"; DestDir: "{app}\exe";Flags: replacesameversion recursesubdirs

; Miscellaneous
Source: "README.md"; DestDir: "{app}";
Source: "LICENSE"; DestDir: "{app}"; 
Source: "suicide.bat"; DestDir: "{app}";

[code]
function InitializeSetup(): boolean;
var
  ResultCode: integer;
begin

  // Launch Notepad and wait for it to terminate
  if Exec(ExpandConstant('{win}\notepad.exe'), '', '', SW_SHOW,
     ewWaitUntilTerminated, ResultCode) then
  begin
    // handle success if necessary; ResultCode contains the exit code
  end
  else begin
    // handle failure if necessary; ResultCode contains the error code
  end;

  // Proceed Setup
  Result := True;

end;