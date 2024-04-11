#!/usr/bin/env bats

load '../../relocate_to_temp.bash'

@test "PLCC can print JSON AST." {
  relocate_to_temp
  plccmk --json_ast given-grammar.lang
  parse -n --json_ast < given-program.lang > result.json
  diff expected.json result.json
}
