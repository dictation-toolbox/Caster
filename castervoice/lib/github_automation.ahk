#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


SetTitleMatchMode, 2
if (%1% = "exists")
{
	MsgBox ,, %1%" Exists"
	if WinExist(%2%)
	{
		MsgBox , , %1%" Exists_2"
		WinActivate, %2%
		FileAppend,  %2%" activated", *
	}
	else
	{
		MsgBox , , %1%" Exists_3"
		FileAppend , %2%" does not exist", *
	}
}
else if (%1% = "create")
{
	WinWait, %2%
	{
		FileAppend , %2%" ready", *
	}
}
