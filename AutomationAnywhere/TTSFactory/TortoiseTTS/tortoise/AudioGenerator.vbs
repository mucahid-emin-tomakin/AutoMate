Set WshShell = CreateObject("WScript.Shell")
cmdPath = WScript.ScriptFullName
cmdDir = Left(cmdPath, Len(cmdPath) - Len(WScript.ScriptName))
runCmd = cmdDir & "\" & "AudioGenerator.bat"
WshShell.Run Chr(34) & runCmd & Chr(34), 1, True
