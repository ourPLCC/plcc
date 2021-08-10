@ECHO off

IF NOT EXIST Java\Parse.class (
    ECHO Parse: no such file
    EXIT /B 1
)

java -cp .\Java Parse %*
