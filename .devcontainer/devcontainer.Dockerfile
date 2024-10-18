FROM mcr.microsoft.com/devcontainers/base:bullseye

RUN apt-get update && apt-get install -y \
  openjdk-17-jdk \
  python3 \
  python3-venv \
&& rm -rf /var/lib/apt/lists/*

USER vscode
RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 -
