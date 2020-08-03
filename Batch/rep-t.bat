@ECHO off

IF NOT EXIST Java\Rep.class (
    ECHO Rep: no such file
    EXIT /B 1
)

pushd Java
java Rep -t
popd
