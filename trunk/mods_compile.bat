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

rmdir /q /s "%MODREOBDIR%" 2>NUL
mkdir "%MODREOBDIR%"

echo === Minecraft Coder Pack %MCPVERSION% === >"%MODCOMPLOG%"

echo MCP %MCPVERSION% running in %MCPDIR%

if exist "%MCBIN%\net\minecraft\client\Minecraft.class" (
    echo Compiling MCP Mod Launcher
    echo *** Compiling MCP Mod Launcher >>"%MODCOMPLOG%"
    for /D %%a in (%MODSOURCEBASE%\*) do (
        javac -g -verbose -cp "%MODCP%" -sourcepath "%MCPMODDIR%" -d "%MODTEMP%" %%a\*.java 2>&1 | %MCPTEE% -a "%MODCOMPLOG%" | %MCPGREP% -v "^\[" | %MCPGREP% -v "^Note:"
    )

    cd "%MODTEMP%"
    jar xf "%MCPMODDIR%\mcp_v1.jar"
    rmdir /q /s META-INF 2>NUL
    cd "%MCPDIR%"

    if exist "%MODTEMP%\MCP\Mod.class" (
        echo + Obfuscating mods.
        echo + Obfuscating mods. >>"%MODCOMPLOG%"
        %MCPOBFUSC% -c "%MCPCONFDIR%\reob.conf" -d "%MCREOBSCRIPT%" -i "%MODTEMP%" -o "%MODREOBDIR%" >>"%MODCOMPLOG%"
    ) else (
        echo *** Mods not compiled, skipping
    )

    xcopy /s /y /q "%MCPMODDIR%\MCP\mod_jumpblock\lang" "%MODREOBDIR%\MCP\mod_jumpblock\lang\" >NUL
    xcopy /s /y /q "%MCPMODDIR%\MCP\mod_mcp\lang" "%MODREOBDIR%\MCP\mod_mcp\lang\" >NUL
    xcopy /s /y /q "%MCPMODDIR%\MCP\mod_mcp\gfx" "%MODREOBDIR%\MCP\mod_mcp\gfx\" >NUL
    
    jar cfe "%MODJAR%" MCP.Start -C "%MODREOBDIR%" .
) else (
    if not exist "%MCJADOUT%\net\minecraft\client\Minecraft.java" (
        echo *** Client not recompiled, run recompile.bat
    ) else (
        if exist "%MCJAR%" (
            echo *** Client not decompiled, run decompile.bat
        ) else (
            echo *** minecraft.jar was not found, skipping
        )
    )
)

echo === MCP %MCPVERSION% compile mods script finished ===

pause
