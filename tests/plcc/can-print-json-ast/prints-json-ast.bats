#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/json-test
}

teardown() {
  cd ../..
  rm -rf ${BATS_TMPDIR}/json-test
}

@test "PLCC can print JSON AST." {
  FILES="expected.json given-grammar.lang given-program.lang"
  for f in $FILES ; do
    cp -R "${BATS_TEST_DIRNAME}/${f}" "${BATS_TMPDIR}/json-test"
  done

  cd "${BATS_TMPDIR}/json-test"
  plccmk --json_ast given-grammar.lang
  parse -n --json_ast < given-program.lang > result.json
  diff expected.json result.json
}
