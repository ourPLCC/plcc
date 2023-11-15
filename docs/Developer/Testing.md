# Testing

## Dependencies

* PLCC
* Bash 5+
* [bats 1.2+](https://bats-core.readthedocs.io/en/latest/index.html).

## Running the tests

Run the tests...

```bash
tests/run
```

## Running the tests inside the official container.

Build and run the PLCC container...

```bash
containers/plcc/build.bash
containers/plcc/run.bash
```

You are now running inside the PLCC container. Now run the tests.

```bash
/plcc/tests/run
```

## Writing Tests

See [Bats documentation](https://bats-core.readthedocs.io/en/latest/index.html).
Place tests in `tests/plcc`. See existing tests for examples.

