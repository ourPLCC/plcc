#!/usr/bin/env bash

echo "
export LIBPLCC=\"${HOME}/.local/lib/plcc/src\"
export PATH=\"\${LIBPLCC}:\$PATH\"
function plcc-con() {
    docker run --rm -it -v \"\$PWD:/workdir\" --user \"\$(id -u):\$(id -g)\" ghcr.io/ourplcc/plcc:latest \"\$@\"
}
"