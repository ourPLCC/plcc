#!/usr/bin/env bats

load '../relocate_to_temp.bash'

@test "Creates Python directory when 4th section detected." {
  relocate_to_temp
  cat << EOF > grammar
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
%
%
EOF

  RESULT="$(plccmk --json_ast grammar)"

  echo "RESULT: $RESULT"
  [[ -d Python ]]
}
