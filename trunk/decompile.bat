@echo off

call setup.bat
call findjdk.bat PATH

java -help >NUL 2>NUL
if errorlevel 1 (
    echo Unable to locate java.exe. Please verify that it is in the PATH.
    pause
    exit /b
)

if not exist "%MCPTEMPDIR%" mkdir "%MCPTEMPDIR%"
if not exist "%MCPSOURCESDIR%" mkdir "%MCPSOURCESDIR%"

echo === Minecraft Coder Pack %MCPVERSION% === >"%MCPLOG%"

echo MCP %MCPVERSION% running in %MCPDIR%

if exist "%MCJAR%" (
    if exist "%MCJADOUT%\net\minecraft\client\Minecraft.java" (
        echo *** minecraft.jar already decompiled, run cleanup.bat
        echo *** minecraft.jar already decompiled >>"%MCPLOG%"
        goto skip_mc
    )

    echo *** minecraft.jar was found, processing >>"%MCPLOG%"

    echo Deobfuscating minecraft.jar
    echo *** Deobfuscating minecraft.jar >>"%MCPLOG%"
    %MCPRG% "%MCJAR%" "%MCRGJAR%" "%MCRGSCRIPT%" "%MCRGLOG%" %REINDEX_NUMBER% >>"%MCPLOG%"

    echo Unpacking minecraft.jar
    echo *** Unpacking minecraft.jar >>"%MCPLOG%"
    %MCPUNZIP% -o "%MCRGJAR%" * -d "%MCTEMP%" >>"%MCPLOG%"
    del /f /q "%MCTEMP%\META-INF\MOJANG_C.*" 2>NUL
    del /f /q "%MCTEMP%\null" 2>NUL

    echo Fixing minecraft classes
    echo *** Fixing minecraft classes >>"%MCPLOG%"
    %MCPJR% "%MCTEMP%" >>"%MCPLOG%" 2>NUL

    echo Decompiling minecraft classes
    echo *** Decompiling minecraft classes >>"%MCPLOG%"
    %MCPJAD% -b -d "%MCJADOUT%" -dead -o -r -s .java -stat -v "%MCTEMP%\*.class" 2>>"%MCPLOG%"
    %MCPJAD% -b -d "%MCJADOUT%" -dead -o -r -s .java -stat -v "%MCTEMP%\net\minecraft\client\*.class" 2>>"%MCPLOG%"

    echo Repackage minecraft sources
    echo *** Repackage minecraft sources >>"%MCPLOG%"
    %MCPREPACK% "%MCJADOUT%" %MCPACKAGE% >>"%MCPLOG%"

    echo Patching minecraft sources
    echo *** Patching minecraft sources >>"%MCPLOG%"
    %MCPPATCH% -p 1 -u -i "%MCPATCH%" -d "%MCJADOUT%" -s | %MCPTEE% -a "%MCPLOG%"
) else (
    echo *** minecraft.jar was not found, skipping
    echo minecraft.jar was not found >>"%MCPLOG%"
)

:skip_mc

if exist "%MCSJAR%" (
    if exist "%MCSJADOUT%\net\minecraft\server\MinecraftServer.java" (
        echo *** minecraft_server.jar already decompiled, run cleanup.bat
        echo *** minecraft_server.jar already decompiled >>"%MCPLOG%"
        goto skip_mcs
    )

    echo *** minecraft_server.jar was found, processing >>"%MCPLOG%"

    echo Deobfuscating minecraft_server.jar
    echo *** Deobfuscating minecraft_server.jar >>"%MCPLOG%"
    %MCPRG% "%MCSJAR%" "%MCSRGJAR%" "%MCSRGSCRIPT%" "%MCSRGLOG%" %REINDEX_NUMBER% >>"%MCPLOG%"

    echo Unpacking minecraft_server.jar
    echo *** Unpacking minecraft_server.jar >>"%MCPLOG%"
    %MCPUNZIP% -o "%MCSRGJAR%" * -d "%MCSTEMP%" >>"%MCPLOG%"
    del /f /q "%MCSTEMP%\null" 2>NUL

    echo Fixing minecraft server classes
    echo *** Fixing minecraft server classes >>"%MCPLOG%"
    %MCPJR% "%MCSTEMP%" >>"%MCPLOG%" 2>NUL

    echo Decompiling minecraft server classes
    echo *** Decompiling minecraft server classes >>"%MCPLOG%"
    %MCPJAD% -b -d "%MCSJADOUT%" -dead -o -r -s .java -stat -v "%MCSTEMP%\*.class" 2>>"%MCPLOG%"
    %MCPJAD% -b -d "%MCSJADOUT%" -dead -o -r -s .java -stat -v "%MCSTEMP%\net\minecraft\server\*.class" 2>>"%MCPLOG%"

    echo Repackage minecraft server sources
    echo *** Repackage minecraft server sources >>"%MCPLOG%"
    %MCPREPACK% "%MCSJADOUT%" %MCSPACKAGE% >>"%MCPLOG%"

    echo Patching minecraft server sources
    echo *** Patching minecraft server sources >>"%MCPLOG%"
    %MCPPATCH% -p 1 -u -i "%MCSPATCH%" -d "%MCSJADOUT%" -s | %MCPTEE% -a "%MCPLOG%"
) else (
    echo *** minecraft_server.jar was not found, skipping
    echo minecraft_server.jar was not found >>"%MCPLOG%"
)

:skip_mcs

if exist "%MCPSPLASHES%" copy "%MCPSPLASHES%" "%MCSPLASHES%" >NUL

echo Renaming methods and fields
echo *** Renaming methods and fields >>"%MCPLOG%"
%MCPRENAMER% -R -c "%MCPCONFDIR%\renamer.conf" >>"%MCPLOG%"

echo === MCP %MCPVERSION% decompile script finished ===

pause
