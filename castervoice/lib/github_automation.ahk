#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

check := %1%
title := %2%

MsgBox , , "check=" . ", title=" . title

SetTitleMatchMode, 2
if (check == "exists")
{
	MsgBox ,, check . " Exists"
	if WinExist(title)
	{
		MsgBox , , check . " Exists_2"
		WinActivate, title
		FileAppend,  title . " activated", *
	}
	else
	{
		MsgBox , , check . " Exists_3"
		FileAppend , title . " does not exist", *
	}
}
else if (check = "create")
{
	MsgBox , , check . " creates_4"
	
	WinWait, title
	{
		FileAppend , title . " ready", *
	}
}
