# Quick Start

For use in Bash (requires bash, curl, Java, and Python), run...

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)"
```

For use in GitPod, add the following to your project's `.gitpod.yml`

```yaml
tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)" > ~/.bashrc
        # Uncomment to checkout install specific version
        # git -C "$HOME/.local/plcc/" checkout v4.0.1
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
