If (!(Test-Path A:))
{
New-PSDrive -Name "A" -PSProvider "FileSystem" -Root "\\192.168.0.31\Public"https://github.com/LeonLoong/Maya-callback/blob/main/install.ps1
}
else { Write-Host "The A: drive is already in use." }

$HOMEPATH = $env:USERPROFILE
$DEMOSERVERPATH = "A:\Demo_Tech\Global\Script\DEMO_Main\DEMO\"
$DEMOLOCALPATH = join-path -path $HOMEPATH -childpath "DEMO_Main\Program\DEMO"
$DEMOSHORCUTFULLPATH = join-path -path $HOMEPATH -childpath "Desktop\DEMO.lnk"
$DEMOLOCALFULLPATH = join-path -path $DEMOLOCALPATH -childpath "DEMO.exe"

If ((Test-Path $DEMOLOCALPATH))
{
Remove-Item –path $DEMOLOCALPATH –Recurse
}
else { Write-Host "DEMO is not existed, creating DEMO..." }

If (!(Test-Path $DEMOLOCALPATH))
{
Copy-Item $DEMOSERVERPATH -Destination $DEMOLOCALPATH -Recurse
}
else { Write-Host "DEMO is already existed." }

$s=(New-Object -COM WScript.Shell).CreateShortcut($DEMOSHORCUTFULLPATH);$s.TargetPath = $DEMOLOCALFULLPATH;$s.Save()
Write-Host "DEMO shorcut is created."

pause
