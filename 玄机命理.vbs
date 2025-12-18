Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw """ & Replace(WScript.ScriptFullName, WScript.ScriptName, "") & "a1.py""", 0, False
