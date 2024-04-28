#!/usr/bin/env bats

load '../../relocate_to_temp.bash'

@test "PLCC parses." {
  relocate_to_temp

  plccmk -c given-grammar.plcc
  # parse -n < given-program.lang
}
