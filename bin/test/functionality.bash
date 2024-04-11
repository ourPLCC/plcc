#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/../.." &> /dev/null && pwd )"


function run_local_tests() {
    cd "${PROJECT_ROOT}"
    tests/run.bash
}


function run_language_tests() {
    LANGUAGES_VERSION="${LANGUAGES_VERSION:-}"
    cd /tmp

    rm -rf languages
    git clone https://github.com/ourPLCC/languages.git
    if [ -n "${LANGUAGES_VERSION}" ] ; then
        git -C ./languages checkout "${LANGUAGES_VERSION}"
    fi
    languages/bin/test.bash
    rm -rf languages
}


run_local_tests
run_language_tests
