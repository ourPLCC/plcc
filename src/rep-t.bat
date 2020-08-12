@ECHO off

IF NOT EXIST Java\Rep.class (
    ECHO Rep: no such file
    EXIT /B 1
)

java -cp .\Java Rep -t %1 %2 %3 %4 %5 %6 %7 %8 %9
