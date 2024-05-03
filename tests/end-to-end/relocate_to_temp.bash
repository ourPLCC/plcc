function relocate_to_temp () {
  cd "${BATS_TEST_TMPDIR}"
  cp -R "${BATS_TEST_DIRNAME}/"* .
}
