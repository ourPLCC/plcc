#!/usr/bin/env bats

@test "PLCC compiles the OBJ language." {
  # Copy the OBJ language to the temp directory for this test
  cp -R "${BATS_TEST_DIRNAME}/OBJ" "${BATS_TMPDIR}"

  # Change into the temporary OBJ directory.
  cd "${BATS_TMPDIR}/OBJ"

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
  [ "$status" -eq 0 ]
}
