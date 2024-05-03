#!/usr/bin/env bats

load '../relocate_to_temp.bash'

@test "Functions correctly when no 4th section exists." {
  relocate_to_temp
  cat << EOF > grammar
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
%
EOF

  RESULT="$(plccmk -c grammar)"

  echo "RESULT: $RESULT"
  [[ ! -d $BATS_TMPDIR/no-4th-test/Python ]]
}
