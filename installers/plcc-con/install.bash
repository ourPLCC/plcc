#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2023 Stoney Jackson <dr.stoney@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

echo "
# Add the following to .bashrc or .zshrc
function plcc-con() {
    docker run --rm -it -v \"\$PWD:/workdir\" --user \"\$(id -u):\$(id -g)\" ghcr.io/ourplcc/plcc:latest \"\$@\"
}
"
