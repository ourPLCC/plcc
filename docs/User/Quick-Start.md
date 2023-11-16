# Quick Start

If none of the following work in your context, see [Getting Started](Getting-Started.md).

**For use in Bash** (requires curl, Java SDK >=11, and Python >=3.5), run...

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)"
```

**For use in GitPod**, add or update `.gitpod.yml` in the root of your GitLab/GitHub/Bitbucket repository
with the following, then open your repo in GitPod:

```yaml
image: gitpod/workspace-full:latest

tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)" >> ~/.bashrc
        # Uncomment to checkout install specific version
        # git -C "$HOME/.local/plcc/" checkout v4.0.1
        exec bash
```

**For use in Docker**...

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest
```

**For use through Docker**...

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest PLCC_COMMANDS_HERE
```
