@ECHO off

IF NOT EXIST Java\Parser.class (
    ECHO Parse: no such file
    EXIT /B 1
)

pushd Java
java Parser %*
popd
