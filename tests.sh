#!/usr/bin/env bats

@test "PLCC reports its version number." {
  run plcc --version

  echo "OUTPUT: $output"
  echo "ERROR: $error"

  regex='^PLCC \d+\.\d+\.\d+(-dev.0)?$'
  [[ "$output" =~ $regex ]]
  [[ "$status" -eq 0 ]]
}

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

@test "PLCC parses." {
  cat << EOF > "$BATS_TMPDIR/grammar"
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
EOF

  RESULT="$(cd "$BATS_TMPDIR" && plccmk grammar > /dev/null && echo "A asdf A fdsa A B" | parse)"

  echo "RESULT: $RESULT"
  [[ "$RESULT" =~ P@[0-9a-f]+ ]]

  rm -rf "$BATS_TMPDIR/grammar"
  rm -rf "$BATS_TMPDIR/Java"
}

@test "PLCC detects illegal tokens." {
  # GIVEN a grammar file with a bad token name
  cat << EOF > "$BATS_TMPDIR/grammar"
token bad_token_name '.'
EOF

  # WHEN plcc is ran on that grammar file
  run plcc "$BATS_TMPDIR/grammar"

  # print stdout and stderr for debugging
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # THEN plcc exits with an error code
  [ "$status" -ne 0 ]

  # AND plcc reports that there is an "illegal token name"
  [[ "$output" = *"illegal token name"* ]]

  # cleanup
  rm "$BATS_TMPDIR/grammar"
}
