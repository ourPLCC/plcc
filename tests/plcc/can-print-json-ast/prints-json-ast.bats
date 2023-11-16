#!/usr/bin/env bats

@test "PLCC can print JSON AST." {
  FILES="expected.json given-grammar.lang given-program.lang"
  for f in $FILES ; do
    cp "${BATS_TEST_DIRNAME}/${f}" "${BATS_TMPDIR}"
  done

  cp "${BATS_TEST_DIRNAME}"/* "$BATS_TMPDIR/"
  cd "${BATS_TMPDIR}"
  plccmk --json given-grammar.lang
  parse --json -n < given-program.lang > result.json
  diff expected.json result.json

  for f in $FILES ; do
    rm "${BATS_TMPDIR}/${f}"
  done
  rm "${BATS_TMPDIR}/result.json"
}
