rem Finding java
java -help > NUL 2> NUL
if not errorlevel 1 (
    goto :findjavac
)
echo Finding java.exe... if you want to speed this up, add it to your PATH
FOR /F "TOKENS=*" %%A IN ('%MCPWHEREIS% -d "%PROGRAMFILES%" java.exe') DO SET JAVAPATH=%%A
set PATH=%PATH%;%JAVAPATH%

:findjavac
rem Finding javac
javac -help > NUL 2> NUL
if not errorlevel 1 (
    goto :eof
)
echo Finding javac.exe... if you want to speed this up, add it to your PATH
FOR /F "TOKENS=*" %%A IN ('%MCPWHEREIS% -d "%PROGRAMFILES%" javac.exe') DO SET JAVACPATH=%%A
set PATH=%PATH%;%JAVACPATH%

echo Path set.
set "%~1=%PATH%"
