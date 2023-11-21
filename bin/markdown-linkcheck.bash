#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/.." &> /dev/null && pwd )"
cd "${PROJECT_ROOT}"

function markdown-linkcheck () {
    docker run -v ${PWD}:/tmp:ro --rm -i ghcr.io/tcort/markdown-link-check:stable "/tmp/$1"
}
export -f markdown-linkcheck

find . -name \*.md -print0 | xargs -0 -n1 bash -c 'markdown-linkcheck "$@"' "{}"