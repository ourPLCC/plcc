#!/usr/bin/env bats

@test "PLCC reports its version number." {
  run plcc --version

  echo "OUTPUT: $output"
  echo "ERROR: $error"

  regex='^PLCC \d+\.\d+\.\d+(-.*)?$'
  [[ "$output" =~ $regex ]]
  [[ "$status" -eq 0 ]]
}
