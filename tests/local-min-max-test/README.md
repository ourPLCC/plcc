# Min Max Test

The min-max test was originally designed to run in CI/CD on GitHub.
See `./.github/workflows/test_python-*.yml` files. The files in this
directory allows developers to run an equivalent test locally.

## Overview

Test PLCC using the supported minimum and maximum versions of Python and Java.
The maximum supported versions are the latest, stable releases.
The minimum supported versions are currently:

* Python: 3.5.10 (as identified with pyenv)
* Java: 11.0.21-tem (as identified with sdkman)

## Requirements

* Bash
* Docker

## Run the tests

```bash
./run.bash
```
