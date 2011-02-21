@echo off

call setup.bat
call findjdk.bat PATH

java -help >NUL 2>NUL
if errorlevel 1 (
    echo Unable to locate java.exe. Please verify that it is in the PATH.
    pause
    exit /b
)

if exist "%MODJAR%" (
    java -Xmx1024m -Xms1024m -classpath "%MODJAR%;%APPDATA%\.minecraft\bin\*" "-Djava.library.path=%APPDATA%\.minecraft\bin\natives" MCP.Start -searge MCPlayer
) else (
    echo *** Mods not compiled, run mods_compile.bat
)

pause
