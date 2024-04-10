#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/generate-python-test
}

teardown() {
  rm -rf ${BATS_TMPDIR}/generate-python-test
}

@test "Creates Python directory when 4th section detected." {
  cat << EOF > "$BATS_TMPDIR/generate-python-test/grammar"
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
%
%
EOF

  RESULT="$(cd "$BATS_TMPDIR/generate-python-test" && plccmk --json_ast grammar)"

  echo "RESULT: $RESULT"
  [[ -d $BATS_TMPDIR/generate-python-test/Python ]]
}
