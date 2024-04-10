#!/usr/bin/env bats

setup() {
  mkdir ${BATS_TMPDIR}/obj-test
}

teardown() {
  cd ../../../..
  rm -rf ${BATS_TMPDIR}/obj-test
}

@test "PLCC compiles the OBJ language." {
  # Copy the OBJ language to the temporary directory for this test
  cp -R "${BATS_TEST_DIRNAME}/OBJ" "${BATS_TMPDIR}/obj-test"

  # Change into the temporary OBJ directory.
  cd "${BATS_TMPDIR}/obj-test/OBJ"

  # Use plcc to generate the Java files from the OBJ grammar file.
  plcc "grammar"

  # Change into the generated Java file.
  cd Java

  # Compile the Java files.
  run javac *.java

  # Print stdout and stderr for debugging.
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # Assert success.
  [[ "$status" -eq 0 ]]
}
