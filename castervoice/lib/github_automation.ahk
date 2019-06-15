#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

check = %1%
title = %2%

SetTitleMatchMode, 2
if (check == "exists")
{
	if WinExist(title)
	{
		WinActivate, %title%
		FileAppend,  %title% activated, *
	}
	else
	{
		FileAppend , %title% does not exist, *
	}
}
else if (check = "create")
{
	WinWait, %title%
	{
		FileAppend , %title% ready, *
	}
}
