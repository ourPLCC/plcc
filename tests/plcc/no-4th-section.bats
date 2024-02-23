#!/usr/bin/env bats

@test "Functions correctly when no 4th section exists." {
  cat << EOF > "$BATS_TMPDIR/grammar"
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
%
EOF

  RESULT="$(cd "$BATS_TMPDIR" && plccmk -c grammar)"

  echo "RESULT: $RESULT"
  [[ ! -d $BATS_TMPDIR/Python ]]

  rm -rf "$BATS_TMPDIR/grammar"
  rm -rf "$BATS_TMPDIR/Java"
}