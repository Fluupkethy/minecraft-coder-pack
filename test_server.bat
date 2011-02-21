@echo off

call setup.bat
call findjdk.bat PATH

java -help >NUL 2>NUL
if errorlevel 1 (
    echo Unable to locate java.exe. Please verify that it is in the PATH.
    pause
    exit /b
)

if exist "%MCSBIN%\net\minecraft\server\MinecraftServer.class" (
    cd "%MCPBINDIR%"
    java -Xms1024M -Xmx1024M -cp "%MCSTESTCP%" net.minecraft.server.MinecraftServer
    cd "%MCPDIR%"
) else (
    echo *** Server not compiled, run recompile.bat
)

pause
