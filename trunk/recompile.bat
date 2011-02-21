@echo off

call setup.bat
call findjdk.bat PATH

javac -help >NUL 2>NUL
if errorlevel 1 (
    echo Unable to locate javac.exe. Please verify that it is in the PATH.
    echo If you don't know where to get it, please visit http://www.oracle.com/technetwork/java/javase/downloads/index.html and download a JDK.
    pause
    exit /b
)

rmdir /q /s "%MCBIN%" 2>NUL
rmdir /q /s "%MCSBIN%" 2>NUL
mkdir "%MCBIN%"
mkdir "%MCSBIN%"

echo === Minecraft Coder Pack %MCPVERSION% === >"%MCPCOMPLOG%"

echo MCP %MCPVERSION% running in %MCPDIR%

if exist "%MCJADOUT%\net\minecraft\client\Minecraft.java" (
    echo Compiling Minecraft
    echo *** Compiling Minecraft >>"%MCPCOMPLOG%"
    javac -g -verbose -cp "%MCCP%" -sourcepath "%MCJADOUT%" -d "%MCBIN%" %MCSRC1%\*.java %MCSRC2%\*.java "%MCSTART%" "%MCSNDFIX%" 2>&1 | %MCPTEE% -a "%MCPCOMPLOG%" | %MCPGREP% -v "^\[" | %MCPGREP% -v "^Note:"
) else (
    if exist "%MCJAR%" (
        echo *** Client not decompiled, run decompile.bat
    ) else (
        echo *** minecraft.jar was not found, skipping
    )
)

if exist "%MCSJADOUT%\net\minecraft\server\MinecraftServer.java" (
    echo Compiling Minecraft Server
    echo *** Compiling Minecraft Server >>"%MCPCOMPLOG%"
    javac -g -verbose -sourcepath "%MCSJADOUT%" -d "%MCSBIN%" %MCSSRC1%\*.java %MCSSRC2%\*.java 2>&1 | %MCPTEE% -a "%MCPCOMPLOG%" | %MCPGREP% -v "^\[" | %MCPGREP% -v "^Note:"
) else (
    if exist "%MCSJAR%" (
        echo *** Server not decompiled, run decompile.bat
    ) else (
        echo *** minecraft_server.jar was not found, skipping
    )
)

echo === MCP %MCPVERSION% recompile script finished ===

pause
