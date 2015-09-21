@echo off

set BOOST_SOURCE=C:\build\boost_1_40_0
set BOOST_VERSION=1.40

set GTK_HOME=c:\build\Gtk+
set PKG_CONFIG=%GTK_HOME%\bin\pkg-config.exe

set OPENSSL_HOME=c:\build\openssl-1.0.1e

set QT4DIR=c:\build\qt-4.8.5

set FREETYPE2_HOME=c:\build\freetype-2.4.4
set FREETYPE2_INCLUDE=%FREETYPE2_HOME%\include
set FREETYPE2_INCLUDE=%FREETYPE2_INCLUDE%;%FREETYPE2_HOME%\include\freetype2
set FREETYPE2_LIBPATH=%FREETYPE2_HOME%

set V8_HOME=c:\build\v8
set V8_LIBPATH=%V8_HOME%\build\Release\lib

call "%ProgramFiles%\Microsoft Visual Studio 9.0\vc\bin\vcvars32.bat"
call "%ProgramFiles%\Intel\ComposerXE-2011\bin\iclvars.bat" ia32

REM Windows SDK
set PATH=%PATH%;%ProgramFiles%\Microsoft SDKs\Windows\v6.1\Bin

set PATH=%QT4_DIR%\bin;%PATH%
set PATH=%PATH%;%ProgramFiles%\Subversion\bin
set PATH=%PATH%;C:\Python26;c:\Python26\scripts
set PATH=%PATH%;%ProgramFiles%\gnuwin32\bin
set PATH=%PATH%;%ProgramFiles%\NSIS\

REM set CODE_SIGN_KEY=c:\build\certificate.pfx
REM set CODE_SIGN_KEY_PASS_FILE=c:\build\cert_pass.txt

IF NOT EXIST %SLAVE_NAME% mkdir %SLAVE_NAME%
