# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

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

# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.
