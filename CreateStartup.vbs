set WshShell = WScript.CreateObject("WScript.Shell")
username = WScript.Arguments(0)
app_dir = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
set oShellLink = WshShell.CreateShortcut("C:\Users\" & username & "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\XSearch.lnk")
oShellLink.TargetPath = app_dir & "\Run.pyw"
'oShellLink.WindowStyle = 1
'oShellLink.Hotkey = "Ctrl+Alt+e"
oShellLink.IconLocation = app_dir & "\Icons\XSearch.ico"
oShellLink.Description = "The most convenient web search application."
oShellLink.WorkingDirectory = app_dir
oShellLink.Save