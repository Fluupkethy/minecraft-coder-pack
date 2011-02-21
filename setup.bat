set MCPVERSION=2.8

echo *** Minecraft Coder Pack Version %MCPVERSION% ***

set MCPDIR=%CD%
set MCPTOOLSDIR=%MCPDIR%\tools
set MCPPYTHONTOOLSDIR=%MCPDIR%\tools-python
set MCPLOGDIR=%MCPDIR%\logs
set MCPJARSDIR=%MCPDIR%\jars
set MCPCONFDIR=%MCPDIR%\conf
set MCPTEMPDIR=%MCPDIR%\temp
set MCPSOURCESDIR=%MCPDIR%\sources
set MCPSOURCEBASE=sources
set MCPPATCHDIR=%MCPDIR%\patches
set MCPBINDIR=%MCPDIR%\bin
set MCPMODDIR=%MCPDIR%\mods
set MCPOUTDIR=%MCPDIR%\final_out

set MCPLOG=%MCPLOGDIR%\minecraft.log
set MCPCOMPLOG=%MCPLOGDIR%\minecraft_compile.log

set MCPRG=java -cp "%MCPTOOLSDIR%\retroguard.jar" RetroGuard
set MCPUNZIP="%MCPTOOLSDIR%\unzip.exe"
set MCPJR="%MCPTOOLSDIR%\jadretro.exe"
set MCPJAD="%MCPTOOLSDIR%\jad.exe"
set MCPPATCH="%MCPTOOLSDIR%\applydiff.exe"
set MCPGETCSV="%MCPTOOLSDIR%\get_csv.exe"
rem set MCPGETCSV=python "%MCPPYTHONTOOLSDIR%\get_csv.py"
set MCPRENAMER="%MCPTOOLSDIR%\renamer.exe"
rem set MCPRENAMER=python "%MCPPYTHONTOOLSDIR%\renamer_v3.py"
set MCPREPACK="%MCPTOOLSDIR%\repackage.exe"
set MCPOBFUSC="%MCPTOOLSDIR%\obfuscathon.exe"
rem set MCPOBFUSC=python "%MCPPYTHONTOOLSDIR%\obfuscathon.py"
set MCPTEE="%MCPTOOLSDIR%\tee.exe"
set MCPGREP="%MCPTOOLSDIR%\grep.exe"
set MCPWHEREIS="%MCPTOOLSDIR%\whereis.exe"
rem set MCPWHEREIS=python "%MCPPYTHONTOOLSDIR%\whereis.py"

set MCJAR=%MCPJARSDIR%\bin\minecraft.jar
set MCSJAR=%MCPJARSDIR%\minecraft_server.jar
set MCJI=%MCPJARSDIR%\bin\jinput.jar
set MCJGL=%MCPJARSDIR%\bin\lwjgl.jar
set MCJGLU=%MCPJARSDIR%\bin\lwjgl_util.jar
set MCCP=%MCJAR%;%MCJI%;%MCJGL%;%MCJGLU%

set MCRGJAR=%MCPTEMPDIR%\minecraft_rg.jar
set MCRGSCRIPT=%MCPCONFDIR%\minecraft.rgs
set MCRGLOG=%MCPLOGDIR%\minecraft_rg.log

set MCSRGJAR=%MCPTEMPDIR%\minecraft_server_rg.jar
set MCSRGSCRIPT=%MCPCONFDIR%\minecraft_server.rgs
set MCSRGLOG=%MCPLOGDIR%\minecraft_server_rg.log

set MCTEMP=%MCPTEMPDIR%\minecraft
set MCSTEMP=%MCPTEMPDIR%\minecraft_server

set MCJADOUT=%MCPSOURCESDIR%\minecraft
set MCSJADOUT=%MCPSOURCESDIR%\minecraft_server

set MCPACKAGE=net.minecraft.src
set MCSPACKAGE=net.minecraft.src

set MCPATCH=%MCPPATCHDIR%\minecraft.patch
set MCSPATCH=%MCPPATCHDIR%\minecraft_server.patch
set MCPSPLASHES=%MCPPATCHDIR%\splashes.txt

set REINDEX_NUMBER=21000

set MCSTART=%MCPPATCHDIR%\Start.java
set MCSNDFIX=%MCPPATCHDIR%\gd.java

set MCSRC1=%MCPSOURCEBASE%\minecraft\net\minecraft\client
set MCSRC2=%MCPSOURCEBASE%\minecraft\net\minecraft\src
set MCBIN=%MCPBINDIR%\minecraft
set MCSSRC1=%MCPSOURCEBASE%\minecraft_server\net\minecraft\server
set MCSSRC2=%MCPSOURCEBASE%\minecraft_server\net\minecraft\src
set MCSBIN=%MCPBINDIR%\minecraft_server

set MCSPLASHES=%MCTEMP%\title\splashes.txt

set MCTESTCP=%MCBIN%;%MCTEMP%;%MCJI%;%MCJGL%;%MCJGLU%
set MCNAT=%MCPJARSDIR%\bin\natives
set MCSTESTCP=%MCSBIN%;%MCSTEMP%

set MCREOBSCRIPT=%MCPDIR%\conf\minecraft_rev.saffx
set MCSREOBSCRIPT=%MCPDIR%\conf\minecraft_server_rev.saffx
set MCREOBDIR=%MCPOUTDIR%\minecraft
set MCSREOBDIR=%MCPOUTDIR%\minecraft_server

set MCPREOBLOG=%MCPDIR%\logs\reobf.log
set MCREOBLOG=%MCPDIR%\logs\reobf_minecraft_rg.log
set MCSREOBLOG=%MCPDIR%\logs\reobf_minecraft_server_rg.log

set MODCOMPLOG=%MCPLOGDIR%\mcpmod_compile.log
set MODTEMP=%MCBIN%
set MODREOBDIR=%MCPTEMPDIR%\mods
set MODSOURCEBASE=mods\MCP
set MODCP=%MCPMODDIR%\mcp_v1.jar;%MCTESTCP%
set MODJAR=%MCPOUTDIR%\mcp_12_02.jar
