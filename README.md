# PLCC

PLCC is a Programming Language Compiler Compiler designed for use in
a Programming Languages course.

- License: [GPLv3.0 or higher](LICENSE)
- Need help? [Chat with us](https://discord.gg/EVtNSxS9E2)
- Report a problem or request a feature? [Open an issue](https://github.com/ourPLCC/plcc/issues).
- [Documentation](docs/README.md)

## Quick Start

### Install

If the following don't work for you or your context,
please see [Documentation](docs/README.md).

**Bash (Linux, macOS, Windows via WSL)**

Requires bash, curl, and git.

```bash
/bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)"
```

**Docker**

Start a shell in the PLCC container.

```bash
docker run --rm -it -v "${PWD}:/workdir" ghcr.io/ourplcc/plcc:latest
```

**GitPod**

Add the following to `.gitpod.yml` in the root of your GitLab/GitHub/Bitbucket
repository:

```yaml
image: gitpod/workspace-full:latest

tasks:
  - name: Install PLCC
    command: |
        /bin/bash -c "$(curl -fsSL https://github.com/ourPLCC/plcc/raw/main/installer/install.bash)" >> ~/.bashrc
        exec bash
```

### Use

```bash
$ $EDITOR grammar        # Write a grammar file defining your language.
$ $EDITOR samples        # Write sample programs in your language.
$ plccmk -c grammar      # Compile grammar into a scanner, parser, and interpreter.
$ scan < samples         # Run the scanner on your samples.
$ parse -n -t < samples  # Run the parser on your samples.
$ rep -n -t < samples    # Run the interpreter on your samples.
```

See [Documentation](docs/README.md) for more details.

