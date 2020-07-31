#!/bin/sh
docker run -it -v "${PWD}:/home/my/work" --rm ourplcc/plcc:build
