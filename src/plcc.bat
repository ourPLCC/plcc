@ECHO off

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
