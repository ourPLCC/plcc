#!/usr/bin/env bats

@test "PLCC parses." {
  cat << EOF > "$BATS_TMPDIR/grammar"
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
EOF

  RESULT="$(cd "$BATS_TMPDIR" && plccmk -c grammar > /dev/null && echo "A asdf A fdsa A B" | parse -n)"

  echo "RESULT: $RESULT"
  [[ "$RESULT" =~ .*OK.* ]]

  rm -rf "$BATS_TMPDIR/grammar"
  rm -rf "$BATS_TMPDIR/Java"
}
