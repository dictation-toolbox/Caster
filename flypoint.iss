; Flypoint Installer
; – – – – – – –
; Flypoint Installer will do the following:
;
;– install natlink
;– install dragonfly
;– install tenclips
;– install flypoint
;– upgrade dragonfly
;– run switcher
;
;Python 2.7 must be installed beforehand.
;Natlink must be configured afterwards.
;
;(C:\NatLink\NatLink\confignatlinkvocolaunimacro\start_configurenatlink.py)
;

[Setup]
AppName=Flypoint
AppVersion=0.1.60
DefaultDirName={drive:C:}\NatLink\NatLink\MacroSystem
DefaultGroupName=Flypoint Installer
DirExistsWarning=no
OutputDir=installer_requirements\output
InfoBeforeFile=installer_requirements\infobefore.txt

[Dirs]
Name: "{app}\exe"
Name: "{app}\languages"

[Files]
; Source
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
Source: "dragonfly_upgrade.iss"; DestDir: "{app}";
Source: "flypoint.iss"; DestDir: "{app}";
Source: "dragonfly_upgrade.iss"; DestDir: "{app}";
Source: ".gitignore"; DestDir: "{app}";
Source: "config.json"; DestDir: "{app}"; 

Source: "installer_requirements\MSVCR71.DLL"; Flags: dontcopy
Source: "installer_requirements\setup-natlink-4.1golf.exe"; Flags: dontcopy
Source: "installer_requirements\dragonfly-0.6.5.win32.exe"; Flags: dontcopy
Source: "installer_requirements\TenClipsSetup.exe"; Flags: dontcopy
Source: "installer_requirements\dragonfly_0.6.6b1_upgrader.exe"; DestDir: "{tmp}"

[run]
Filename: "{tmp}\dragonfly_0.6.6b1_upgrader.exe"
Filename: "{app}\exe\Switcher.exe"

[code]
function InitializeSetup(): boolean;
var
  ResultCode: integer;
begin
  ExtractTemporaryFile('MSVCR71.DLL');
  Result := True;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode:   Integer;
  natlink_successful: Boolean;
  dragonfly_successful: Boolean;
  ten_clips_successful: Boolean;
begin
  ExtractTemporaryFile('setup-natlink-4.1golf.exe');
  ExtractTemporaryFile('dragonfly-0.6.5.win32.exe');
  ExtractTemporaryFile('TenClipsSetup.exe');
  
  natlink_successful:=Exec(ExpandConstant('{tmp}\setup-natlink-4.1golf.exe'), 'quit', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
  dragonfly_successful:=Exec(ExpandConstant('{tmp}\dragonfly-0.6.5.win32.exe'), 'quit', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
  ten_clips_successful:=Exec(ExpandConstant('{tmp}\TenClipsSetup.exe'), 'quit', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)

end;

