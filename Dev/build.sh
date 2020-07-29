#!/bin/sh
docker-compose -f Dev/docker-compose.yml build
docker build -t ourplcc/plcc:build .