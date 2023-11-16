# Quick Start

For use in Bash, run...

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/install/install.bash)"
```

For use in GitPod, add the following to your project's `.gitpod.yml`

```yaml
tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/install/install.bash)" > ~/.bashrc
        exec bash
```

For use in Docker...

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest
```

For use through Docker...

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest PLCC_COMMANDS_HERE
```
