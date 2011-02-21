@echo off

call setup.bat

echo CLEANING UP

if "%MCPLOGDIR%" == "" goto skip1
del /f /q "%MCPLOGDIR%\*.log" 2>NUL
:skip1
if "%MCPTEMPDIR%" == "" goto skip2
del /f /q "%MCPTEMPDIR%\*.jar" 2>NUL
del /f /q "%MCPTEMPDIR%\*.md5" 2>NUL
:skip2
if "%MCBIN%" == "" goto skip3
rmdir /q /s "%MCBIN%" 2>NUL
:skip3
if "%MCJADOUT%" == "" goto skip4
rmdir /q /s "%MCJADOUT%" 2>NUL
:skip4
if "%MCTEMP%" == "" goto skip5
rmdir /q /s "%MCTEMP%" 2>NUL
:skip5

if "%MCPBINDIR%" == "" goto skip6
del /f /q "%MCPBINDIR%\*.log" 2>NUL
:skip6
if "%MCPBINDIR%" == "" goto skip7
del /f /q "%MCPBINDIR%\*.txt" 2>NUL
:skip7
if "%MCSBIN%" == "" goto skip8
rmdir /q /s "%MCSBIN%" 2>NUL
:skip8
if "%MCPBINDIR%" == "" goto skip9
rmdir /q /s "%MCPBINDIR%\world" 2>NUL
:skip9
if "%MCSJADOUT%" == "" goto skip10
rmdir /q /s "%MCSJADOUT%" 2>NUL
:skip10
if "%MCSTEMP%" == "" goto skip11
rmdir /q /s "%MCSTEMP%" 2>NUL
:skip11

if "%MCREOBSCRIPT%" == "" goto skip12
del /f /q "%MCREOBSCRIPT%" 2>NUL
:skip12
if "%MCSREOBSCRIPT%" == "" goto skip13
del /f /q "%MCSREOBSCRIPT%" 2>NUL
:skip13

if "%MODREOBDIR%" == "" goto skip14
rmdir /q /s "%MODREOBDIR%" 2>NUL
:skip14

if "%MCPOUTDIR%" == "" goto skip15
rmdir /q /s "%MCPOUTDIR%\minecraft" 2>NUL
rmdir /q /s "%MCPOUTDIR%\minecraft_server" 2>NUL
rmdir /q /s "%MCPOUTDIR%\mods" 2>NUL
del /f /q "%MCPOUTDIR%\*.jar" 2>NUL
:skip15

echo DONE

pause
