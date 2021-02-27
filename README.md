# PLCC

PLCC is a Programming Language Compiler Compiler.

Please see [our wiki](https://github.com/ourPLCC/plcc/wiki) for documentation.

To contact us, report a problem, or make a suggestion, please open an issue
here: <https://github.com/ourPLCC/plcc/issues>.

For information about how to contribute to this project, please see CONTRIBUTING.md.

## Automated Tests

### Dependencies

* PLCC
* Bash 5+
* [bats 1.2+](https://bats-core.readthedocs.io/en/latest/index.html).

### Running the tests

Run the tests...

```bash
tests/run
```

### Running the tests inside the Docker shell.

Run the shell...

```bash
shell/run
```

Run the tests
```bash
/plcc/tests/run
```

### Writing Tests

See [Bats documentation](https://bats-core.readthedocs.io/en/latest/index.html).
Place tests in `tests/plcc`. See existing tests for examples.
