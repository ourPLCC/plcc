#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2023 Stoney Jackson <dr.stoney@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

function main () {
    PLCC_HOME="${HOME}/.local/plcc"
    git clone https://github.com/ourPLCC/plcc.git "${PLCC_HOME}"
    >&2 echo
    >&2 echo "Next, complete the installation: append to ${HOME}/.bashrc the following:"
    >&2 echo
    echo "    # PLCC environment
    export LIBPLCC=\"${PLCC_HOME}/src\"
    export PATH=\"\${LIBPLCC}:\$PATH\""

    >&2 echo "
Last, start a new terminal/shell and run the folling:

    python --version
    python3 --version
    java --version
    javac --version
    plcc --version

Check the output and confirm that:

    1. python OR python3 above worked and its version is at least 3.5.10.
    2. java's and javac's version is at least 11 and they match.
"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
