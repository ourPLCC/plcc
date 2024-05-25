#!/usr/bin/env bats

load '../relocate_to_temp.bash'

@test "scan reads files passed on command-line" {
  relocate_to_temp

  cat << EOF > grammar
skip WHITESPACE '\s'
token FOO 'foo'
token BAR 'bar'
token ID '[A-Za-z]\w*'
EOF

  echo "foo bar \n foobar" > in.file

  TOKENS="$(
    plccmk -c grammar &&
    scan in.file
  )"

  [[ "$TOKENS" =~ "FOO 'foo'" ]]
  [[ "$TOKENS" =~ "BAR 'bar'" ]]
  [[ "$TOKENS" =~ "ID 'foobar'" ]]
}
