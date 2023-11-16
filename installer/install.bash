#!/bin/bash

# SPDX-FileCopyrightText: 2023 Stoney Jackson <dr.stoney@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

PLCC_HOME="${HOME}/.local/plcc"

git clone https://github.com/ourPLCC/plcc.git "${PLCC_HOME}"

# Define LIBPLCC and add it to PATH in ~/.bashrc

echo "
# Add the following to your .bashrc file, and start a new shell.
# PLCC bash environment
export LIBPLCC=\"${PLCC_HOME}/src\"
export PATH=\"\${LIBPLCC}:\$PATH\"
"
