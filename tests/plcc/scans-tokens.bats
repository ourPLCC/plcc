#!/usr/bin/env bats

@test "PLCC scans." {
  cat << EOF > "$BATS_TMPDIR/grammar"
skip WHITESPACE '\s'
token FOO 'foo'
token BAR 'bar'
token ID '[A-Za-z]\w*'
EOF

  IN="foo bar \n foobar"

  TOKENS="$(
    cd "$BATS_TMPDIR" &&
    plccmk "$BATS_TMPDIR/grammar" &&
    OUT="$(echo "$IN" | scan)" &&
    echo "$OUT"
  )"

  [[ "$TOKENS" =~ "FOO 'foo'" ]]
  [[ "$TOKENS" =~ "BAR 'bar'" ]]
  [[ "$TOKENS" =~ "ID 'foobar'" ]]

  rm -rf "$BATS_TMPDIR/grammar"
  rm -rf "$BATS_TMPDIR/Java"
}
