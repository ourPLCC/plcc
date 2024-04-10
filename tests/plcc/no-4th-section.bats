#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/no-4th-test
}

teardown() {
  cd ../../../..
  rm -rf ${BATS_TMPDIR}/no-4th-test
}

@test "Functions correctly when no 4th section exists." {
  cat << EOF > "$BATS_TMPDIR/no-4th-test/grammar"
A 'A'
B 'B'
skip OTHER '.'
%
<p> ::= <aaa> B
<aaa> **= A
%
EOF

  RESULT="$(cd "$BATS_TMPDIR/no-4th-test" && plccmk -c grammar)"

  echo "RESULT: $RESULT"
  [[ ! -d $BATS_TMPDIR/no-4th-test/Python ]]
}
