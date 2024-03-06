#!/usr/bin/env bats

teardown() {
  rm -rf "$BATS_TMPDIR/OBJ"
}

@test "PLCC compiles with 4 sections." {
  # Copy the OBJ language to the temp directory for this test
  cp -R "${BATS_TEST_DIRNAME}/OBJ" "${BATS_TMPDIR}"

  # Change into the temporary OBJ directory.
  cd "${BATS_TMPDIR}/OBJ"

  # Use plcc to generate the Java files from the OBJ grammar file.
  plcc "grammar"

  # Change into the generated Java file.
  cd Java

  # Compile the Java files.
  run javac -cp "/${BATS_TEST_DIRNAME}/../../../lib/jackson/*" *.java

  # Print stdout and stderr for debugging.
  echo "OUTPUT: $output"
  echo "ERROR: $error"

  # Assert success.
  [ "$status" -eq 0 ]
}
