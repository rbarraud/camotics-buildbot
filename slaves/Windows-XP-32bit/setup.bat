set BPATH=HKLM\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced
reg add "%BPATH%" /t REG_DWORD /v EnableBalloonTips /f /d 0

set PATH=%PATH%;C:\Program Files\Microsoft SDKs\Windows\v6.1\Bin
set PATH=%PATH%;C:\Program Files\Subversion\bin
set PATH=%PATH%;C:\Python26;c:\Python26\scripts
set PATH=%PATH%;C:\Program Files\gnuwin32\bin
set PATH=%PATH%;C:\Program Files\Console2
set PATH=%PATH%;%ProgramFiles%\NSIS\

set ENVPATH=HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment

reg add "%ENVPATH%" /t REG_EXPAND_SZ /v Path /f /d "%PATH%"
