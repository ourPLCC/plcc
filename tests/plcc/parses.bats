#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/parse-test
}

teardown() {
  rm -rf ${BATS_TMPDIR}/parse-test
}

@test "PLCC parses." {
  cat << EOF > "${BATS_TMPDIR}/parse-test/grammar"
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
EOF

  RESULT="$(cd "${BATS_TMPDIR}/parse-test" && plccmk -c grammar > /dev/null && echo "A asdf A fdsa A B" | parse -n)"

  echo "RESULT: $RESULT"
  [[ "$RESULT" =~ .*OK.* ]]
}
