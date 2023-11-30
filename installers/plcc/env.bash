#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2023 Stoney Jackson <dr.stoney@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

echo "
export LIBPLCC=\"${HOME}/.local/lib/plcc/src\"
export PATH=\"\${LIBPLCC}:\$PATH\"
function plcc-con() {
    docker run --rm -it -v \"\$PWD:/workdir\" --user \"\$(id -u):\$(id -g)\" ghcr.io/ourplcc/plcc:latest \"\$@\"
}
"