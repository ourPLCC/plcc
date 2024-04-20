#!/usr/bin/env bats

load '../relocate_to_temp.bash'

@test "PLCC parses." {
  relocate_to_temp

  cat << EOF > grammar
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
EOF

  RESULT="$(plccmk -c grammar > /dev/null && echo "A asdf A fdsa A B" | parse -n)"

  echo "RESULT: $RESULT"
  [[ "$RESULT" =~ .*OK.* ]]
}
