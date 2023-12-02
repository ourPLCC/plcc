#!/usr/bin/env bash

set -euo pipefail

echo "
# Add the following to .bashrc or .zshrc
function plcc-con() {
    docker run --rm -it -v \"\$PWD:/workdir\" --user \"\$(id -u):\$(id -g)\" ghcr.io/ourplcc/plcc:latest \"\$@\"
}
"
