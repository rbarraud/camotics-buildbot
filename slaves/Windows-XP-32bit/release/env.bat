set SLAVE_NAME=Windows-XP-32bit-release

call ..\env.bat

set PATH=%PATH%;%CD%\%SLAVE_NAME%\testHarness\build
set SCONS_OPTIONS=%CD%\scons-options.py
