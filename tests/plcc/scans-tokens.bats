#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/scan-test
}

teardown() {
  rm -rf ${BATS_TMPDIR}/scan-test
}

@test "PLCC scans." {
  cat << EOF > "${BATS_TMPDIR}/scan-test/grammar"
skip WHITESPACE '\s'
token FOO 'foo'
token BAR 'bar'
token ID '[A-Za-z]\w*'
EOF

  IN="foo bar \n foobar"

  TOKENS="$(
    cd "${BATS_TMPDIR}/scan-test" &&
    plccmk -c "grammar" &&
    OUT="$(echo "$IN" | scan)" &&
    echo "$OUT"
  )"

  [[ "$TOKENS" =~ "FOO 'foo'" ]]
  [[ "$TOKENS" =~ "BAR 'bar'" ]]
  [[ "$TOKENS" =~ "ID 'foobar'" ]]
}
