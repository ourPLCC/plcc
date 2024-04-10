#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/4-section-test
}

teardown() {
  cd ../../../..
  rm -rf ${BATS_TMPDIR}/4-section-test
}

@test "PLCC compiles with 4 sections." {
  # Copy the OBJ language to the temp directory for this test
  cp -R "${BATS_TEST_DIRNAME}/OBJ" "${BATS_TMPDIR}/4-section-test"

  # Change into the temporary OBJ directory.
  cd "${BATS_TMPDIR}/4-section-test/OBJ"

  # Use plcc to generate the Java files from the OBJ grammar file.
  plccmk grammar

  # Print stdout and stderr for debugging.
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # Assert success.
  [[ "$status" -eq 0 ]]
}
