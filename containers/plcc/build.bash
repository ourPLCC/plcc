#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
set -euxo pipefail
cd "$DIR/../.."
echo "Building test-environment ..."
docker compose --file "$DIR/docker-compose.yml" build
