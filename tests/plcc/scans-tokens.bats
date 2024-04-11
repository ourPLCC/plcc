#!/usr/bin/env bats

load '../relocate_to_temp.bash'

@test "PLCC scans." {
  relocate_to_temp

  cat << EOF > grammar
skip WHITESPACE '\s'
token FOO 'foo'
token BAR 'bar'
token ID '[A-Za-z]\w*'
EOF

  IN="foo bar \n foobar"

  TOKENS="$(
    plccmk -c grammar &&
    OUT="$(echo "$IN" | scan)" &&
    echo "$OUT"
  )"

  [[ "$TOKENS" =~ "FOO 'foo'" ]]
  [[ "$TOKENS" =~ "BAR 'bar'" ]]
  [[ "$TOKENS" =~ "ID 'foobar'" ]]
}
