#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/illegal-tokens-test
}

teardown() {
  rm -rf ${BATS_TMPDIR}/illegal-tokens-test
}

@test "PLCC detects illegal tokens." {
  # GIVEN a grammar file with a bad token name
  cat << EOF > "${BATS_TMPDIR}/illegal-tokens-test/grammar"
token bad_token_name '.'
EOF

  # WHEN plcc is ran on that grammar file
  run plcc "${BATS_TMPDIR}/illegal-tokens-test/grammar"

  # print stdout and stderr for debugging
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # THEN plcc exits with an error code
  [ "$status" -ne 0 ]

  # AND plcc reports that there is an "illegal token name"
  [[ "$output" = *"illegal token name"* ]]
}
