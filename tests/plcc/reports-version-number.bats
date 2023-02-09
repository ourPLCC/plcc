#!/usr/bin/env bats

@test "PLCC reports its version number." {
  run plcc --version

  echo "OUTPUT: $output"
  echo "ERROR: $error"

  regex='^(v?\d+\.\d+\.\d+(-.*)?)|(Unknown)$'
  [[ "$output" =~ $regex ]]
  [[ "$status" -eq 0 ]]
}
