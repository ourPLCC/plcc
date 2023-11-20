# Maintainer's Guide

## Merging

When a PR is merged, a release is automatically cut. So, ensure all tests are passing, and then perform a squash merge writing a good commit message. This commit message:

1. Must follow Conventional Commits since it will be used to determine the next version number.
2. Will become the release notes for the new release. So identify bugs fixed, new features, and BREAKING CHANGES made in the pull request. If you don't know what they are, ask the author. If you still don't know, don't merge.

## Release

Release are cut automatically when a PR is merged. The new release number is determined by Conventional Commit 1.0.0 messages and follow SemVer 2.0.0.
