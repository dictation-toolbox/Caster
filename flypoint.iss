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
Name: "{app}\exe\MultiMonitorTool"
Name: "{app}\exe\nircmd"
Name: "{app}\exe\PSTools"
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
Source: "languages\confightml.txt"; DestDir: "{app}\languages";
Source: "languages\configjava.txt"; DestDir: "{app}\languages";
Source: "languages\configpython.txt"; DestDir: "{app}\languages";

; Executables
Source: "exe\Switcher.exe"; DestDir: "{app}\exe";
Source: "exe\MultiMonitorTool\MultiMonitorTool.exe"; DestDir: "{app}\exe\MultiMonitorTool";
Source: "exe\MultiMonitorTool\readme.txt"; DestDir: "{app}\exe\MultiMonitorTool";
Source: "exe\nircmd\nircmd.exe"; DestDir: "{app}\exe\nircmd";
Source: "exe\nircmd\nircmdc.exe"; DestDir: "{app}\exe\nircmd";
Source: "exe\nircmd\NirCmd.chm"; DestDir: "{app}\exe\nircmd";
Source: "exe\PSTools\pskill.exe"; DestDir: "{app}\exe\PSTools";
Source: "exe\PSTools\psshutdown.exe"; DestDir: "{app}\exe\PSTools";
Source: "exe\PSTools\Pstools.chm"; DestDir: "{app}\exe\PSTools";

;Source: "README.md"; DestDir: "{app}";
;Source: "README.md"; DestDir: "{app}";
;Source: "README.md"; DestDir: "{app}";

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