#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."
cd "$PROJECT_ROOT"

function main() {
    build_test_container_with_maximum_versions_of_python_and_java
    run_tests_in_test_container
    build_test_container_with_minimum_versions_of_python_and_java
    run_tests_in_test_container
}

function build_test_container_with_maximum_versions_of_python_and_java() {
    docker build \
        --tag test \
        --file ./containers/configurable/Dockerfile \
        .
}

function build_test_container_with_minimum_versions_of_python_and_java() {
    docker build \
        --build-arg=PYTHON_VERSION=3.5.10 \
        --build-arg=JAVA_VERSION=11.0.21-tem \
        --tag test \
        --file ./containers/configurable/Dockerfile \
        .
}

function run_tests_in_test_container() {
    docker run -it --rm test bash -c '\
            source /home/tester/.sdkman/bin/sdkman-init.sh ; \
            python3 --version ; \
            python --version ; \
            java --version ; \
            javac --version ; \
            plcc --version ; \
            /home/tester/.plcc/tests/run'
}

main "$@"
