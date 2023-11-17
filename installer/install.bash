#!/bin/bash

# SPDX-FileCopyrightText: 2023 Stoney Jackson <dr.stoney@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

set -euo pipefail

PLCC_HOME="${HOME}/.local/plcc"

git clone https://github.com/ourPLCC/plcc.git "${PLCC_HOME}"

echo "

# PLCC has been installed to ${PLCC_HOME}.
# To complete the installation, add the following to ${HOME}/.bashrc

export LIBPLCC=\"${PLCC_HOME}/src\"
export PATH=\"\${LIBPLCC}:\$PATH\"

"
