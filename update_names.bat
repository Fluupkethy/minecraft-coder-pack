@echo off

call setup.bat

echo MCP %MCPVERSION% running in %MCPDIR%

%MCPGETCSV% -d "%MCPCONFDIR%"
%MCPRENAMER% -R -c "%MCPCONFDIR%\renamer.conf"

echo === MCP %MCPVERSION% update names script finished ===

pause
