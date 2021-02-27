#!/usr/bin/env bats

@test "PLCC detects illegal tokens." {
  # GIVEN a grammar file with a bad token name
  cat << EOF > "$BATS_TMPDIR/grammar"
token bad_token_name '.'
EOF

  # WHEN plcc is ran on that grammar file
  run plcc "$BATS_TMPDIR/grammar"

  # print stdout and stderr for debugging
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # THEN plcc exits with an error code
  [ "$status" -ne 0 ]

  # AND plcc reports that there is an "illegal token name"
  [[ "$output" = *"illegal token name"* ]]

  # cleanup
  rm "$BATS_TMPDIR/grammar"
}
