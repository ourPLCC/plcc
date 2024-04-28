#!/usr/bin/env bash
PLCC_DIR="$(dirname -- "${BASH_SOURCE[0]}" )/../.."
PLCC_DIR="$(cd -- "${PLCC_DIR}" &> /dev/null && pwd)"

echo "
export PATH=\"${PLCC_DIR}/src/plcc/bin:\$PATH\"
function plcc-con() {
    docker run --rm -it -v \"\$PWD:/workdir\" --user \"\$(id -u):\$(id -g)\" ghcr.io/ourplcc/plcc:latest \"\$@\"
}
"
