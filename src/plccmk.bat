@ECHO off

IF "%~1"=="-c" (
	DEL Java\*.java Java\*.class 2> NUL
	CALL %0 %2 %3 %4 %5 %6 %7 %8 %9
        EXIT /B
)

IF "%~1"=="" (
	SET FILES=grammar
) ELSE (
	SET FILES=%*
)

IF NOT DEFINED LIBPLCC (
	ECHO LIBPLCC environment variable not defined
	EXIT /B 1
)

IF NOT EXIST "%LIBPLCC%" (
	ECHO %LIBPLCC%: no such directory
	EXIT /B 1
)

SET STD=%LIBPLCC%\Std
IF NOT EXIST "%STD%" (
	ECHO %STD%: no such directory
	EXIT /B 2
)

python "%LIBPLCC%\plcc.py" %FILES%
IF %ERRORLEVEL% NEQ 0 (
	ECHO Cannot compile %FILES%
	EXIT /B 4
)

PUSHD Java
IF %ERRORLEVEL% NEQ 0 (
	ECHO Cannot cd to the Java directory
	EXIT /B 5
)

javac *.java

POPD
