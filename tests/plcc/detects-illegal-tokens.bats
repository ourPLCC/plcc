#!/usr/bin/env bats

load '../relocate_to_temp.bash'

@test "PLCC detects illegal tokens." {
  relocate_to_temp

  # GIVEN a grammar file with a bad token name
  cat << EOF > grammar
token bad_token_name '.'
EOF

  # WHEN plcc is ran on that grammar file
  run plcc grammar

  # print stdout and stderr for debugging
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # THEN plcc exits with an error code
  [ "$status" -ne 0 ]

  # AND plcc reports that there is an "illegal token name"
  [[ "$output" = *"illegal token name"* ]]
}
