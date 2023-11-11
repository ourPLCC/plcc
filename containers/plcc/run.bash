#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
set -euxo pipefail
echo "Building and running the PLCC container..."
docker compose -f "$DIR/docker-compose.yml" run --rm plcc
