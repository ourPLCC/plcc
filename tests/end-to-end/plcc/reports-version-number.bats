#!/usr/bin/env bats

@test "PLCC reports its version number." {
  run plcc --version

  echo "OUTPUT: $output"
  echo "ERROR: $error"

  regex='^(v?[0-9]+\.[0-9]+\.[0-9]+(-.*)?)$'
  [[ "$output" =~ $regex ]]
  [[ "$status" -eq 0 ]]
}
