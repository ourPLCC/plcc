#!/usr/bin/env bash

set -euo pipefail

PLCC_HOME="${HOME}/.local/lib/plcc"
git clone https://github.com/ourPLCC/plcc.git "${PLCC_HOME}"
echo "# Add the following line to the end of your .bashrc or .zshrc"
"${PLCC_HOME}/installers/plcc/rchook.bash"