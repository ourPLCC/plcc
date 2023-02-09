# Changelog

For release notes after version 3.1.0, please see <https://github.com/ourPLCC/plcc/releases>.

## [3.1.0](https://github.com/ourPLCC/plcc/compare/v3.0.0...v3.1.0) (2021-08-16)

* See issue [#32](https://github.com/ourPLCC/plcc/issues/32)
* and PR [#33](https://github.com/ourPLCC/plcc/pull/33)

### Features

* Add `-v` "verbose" option

    I also want to suggest adding a '-v' (for "verbose") flag on the
    Parse/Rep command line. Setting this flag turns on printing the name
    of the command-line file in which the current expression is being
    parsed/evaluated, using the name "stdin" when reading from
    System.in. Here is an example from the OBJ language:

    Without the '-v' switch:

        java -cp Java Rep Prog/oe
        c
        1
        0
        1
        --> .<c>even?(6)
        1

    With the '-v' switch:

        java -cp Java Rep -v Prog/oe
        [Prog/oe]c
        [Prog/oe]1
        [Prog/oe]0
        [Prog/oe]1
        --> .<c>even?(6)
        [stdin]1

    The '-v' switch is particularly useful when there are several files
    on the command line and you need to find the one where a particular
    error occurs. This is a simple addition and does not break prior
    behaviors.


### Refactors

* Make `Rep` and `Parse` subclasses of `ProcessFiles`

  In VERSION 3.0.0, Parse and Rep both invoke main static method in
  ProcessFiles using a parseOnly parameter that distinguishes between
  just parsing (Parse, with parseOnly=true) and parsing and running
  (Rep, with parseOnly=false). In ProcessFiles, the main method calls a
  run() static method that uses an if statement that invokes either
  $ok() or $run() on the parse tree (an instanceƒ of _Start), depending
  on the value of parseOnly.

  I don't like using if statements if they can be avoided using
  subclassing, so I recommend that we change Rep and Parse so that they
  are subclasses of ProcessFiles, and then they can appropriately call
  the right action -- $ok() or $run() -- without needing to pass a flag.
  This will not have any effects on behavior; it simply makes better
  sense from an OO point of view.

  Oh, and I have taken the two very similar code blocks in ProcessFiles
  and factored them into a single method, processFile, which reduces the
  code size and helps to maintain consistency.


## [3.0.0](https://github.com/ourPLCC/plcc/compare/v2.1.0...v3.0.0) (2021-08-10)

### ⚠ BREAKING CHANGES

* The standalone parser is now called 'Parse' instead of 'Parser'.
  If the parse is successful, it prints 'OK'.

* Both 'Rep' and 'Parse' process command-line arguments and standard
  input in exactly the same way, using a support program called
  'ProcessFiles'. This reduces code duplication and makes for a common
  user interface.

* Printing PLCCExceptions now default to printing a leading "%%% "
  instead of ">>> ". This makes exception output stand out better.

### Features:

* Each PLCC-generated parser class file has a "<Class>:init" hook as
  the first line of its constructor. This can be used to incorporate
  Java code into the Class constructor that can carry out simple
  semantics that would otherwise not be possible using the parser alone.

    For example, the Formals class in Language V4 parses the list of
    formal parameter variables to get a 'varList' of Tokens. In the
    'grammar' file (actually, in the 'code' file that the 'grammar' file
    includes), the lines

    ```
    Formals:init
    %%%
        Env.checkDuplicates(varList, " in proc formals")
    %%%
    ```

    would include this call to 'checkDuplicates' as the first line of
    the Formals constructor. This method will throw an exception if the
    'varList' of Tokens has any duplicate identifiers. Including this
    method in the Formals constructor means that the semantic action of
    checking for duplicate variable names will be done during parsing
    instead of at runtime. This hook is just a comment unless defined
    otherwise in the 'grammar' file.

* Each PLCC-generated parser class file has a "<Class>:top" hook at the
  top of the file. This can be used to incorporate documentation
  regarding the file, such as copyright or whatever. This hook is just
  a comment unless defined otherwise in the 'grammar' file. I haven't
  used this, but someone might find it convenient.

### Refactors

* Instead of printing the 'toString()' value of the root of the parse
  tree to "evaluate" it using the 'Rep' loop, I have the default
  behavior call a '$run()' method on the root of the parse tree.
  Whatever this method does is the 'behavior' of the program. It
  defaults to printing the 'toString()' value as before. The '$run()'
  method is void, so whatever visible behavior a program should have can
  be undertaken in this method.

### Bug Fixes

* **cd:** remove username from test image ([46548c0](https://github.com/ourPLCC/plcc/commit/46548c04cd403c3bfede7986897a541881e54dc5))
* **cd:** use working parts of ci.yaml ([c1c5a03](https://github.com/ourPLCC/plcc/commit/c1c5a030e0f136f060c5782e6fdbbc589fdf9f48))
* **shell:** use bash in shebang ([973da7f](https://github.com/ourPLCC/plcc/commit/973da7fca0bc5e119a861c37ac6e308830c5245b))


## [2.1.0](https://github.com/ourPLCC/plcc/compare/v2.0.1...v2.1.0) (2021-01-22)

### Features

* **feat(Scan.java): fix(plcc.py): refactor(plcc.py):** ([#23](https://github.com/ourPLCC/plcc/issues/23)) ([2013bf2](https://github.com/ourPLCC/plcc/commit/2013bf2c68aa36602dbe9727453b743eaa299dff))


### [2.0.1](https://github.com/ourPLCC/plcc/compare/v2.0.0...v2.0.1) (2020-09-08)

### Bug Fixes

* **plcc.py:** Enforce uppercase token names ([1be4531](https://github.com/ourPLCC/plcc/commit/1be4531b2b75e0f31a3912d1817cb262a94ea07c))


## [2.0.0](https://github.com/ourPLCC/plcc/compare/v1.0.1...v2.0.0) (2020-08-12)

### ⚠ BREAKING CHANGES

* Reorganize files ([ad2f51f](https://github.com/ourPLCC/plcc/commit/ad2f51f64bee866d3c1749005bd3eda701c9a94f))
Moves all source files into a subdirectory named src within the PLCC project.
The path to this src directory is what the LIBPLCC environment variable must
point to, and is also the path that must be added to the PATH environment
variable.  When upgrading, these environment variables must be manually
adjusted to point to the new src directory.

### Features

* Add --version option ([#15](https://github.com/ourPLCC/plcc/issues/15)) ([3a73a85](https://github.com/ourPLCC/plcc/commit/3a73a852ccf40b6241c640d55669402a043b5d1b))

### Bug Fixes

* Renormalize line endings in bat files ([c37f559](https://github.com/ourPLCC/plcc/commit/c37f5598fc77e38f768e78c6236e45a29d787015))
* Restore missing plcc bash script ([#17](https://github.com/ourPLCC/plcc/issues/17)) ([1c0e35c](https://github.com/ourPLCC/plcc/commit/1c0e35c61dad32e1535b791680c493f03d59305c))

### [1.0.1](https://github.com/ourPLCC/plcc/compare/v1.0.0...v1.0.1) (2020-07-12)

### Bug Fixes

* Small fix regarding handling of EOF on input ([7edba11](https://github.com/ourPLCC/plcc/commit/7edba1123d8e8567fdcf24ee7c54ee7acc5c79b5))
