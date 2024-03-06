#!/usr/bin/env bats

teardown() {
  rm -rf ${BATS_TMPDIR}/expected.json
  rm -rf ${BATS_TMPDIR}/given-grammar.lang
  rm -rf ${BATS_TMPDIR}/given-program.lang
  rm -rf ${BATS_TMPDIR}/result.json
  rm -rf ${BATS_TMPDIR}/Java
}

@test "PLCC can print JSON AST." {
  FILES="expected.json given-grammar.lang given-program.lang"
  for f in $FILES ; do
    cp "${BATS_TEST_DIRNAME}/${f}" "${BATS_TMPDIR}"
  done

  cd "${BATS_TMPDIR}"
  plccmk --json_ast given-grammar.lang
  parse -n --json_ast < given-program.lang > result.json
  diff expected.json result.json
}
