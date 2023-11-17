## What version of PLCC am I running?

You can determine what version of PLCC you have by running


```bash
plcc --version
```

## What does PLCC's version number mean?

PLCC uses [Semantic Versioning](https://semver.org/). Each release has a version number containing three numeric components: MAJOR.MINOR.PATCH. These components encode important information about the types of changes that have been made since the last release. This helps you decide if and when to upgrade to newer versions and how much time you should spend reading the CHANGELOG.

## What's with the `-dev.0`?

In between official releases are development releases. The version number for a development release is suffixed with `-dev.0`. For example, `2.3.4-dev.0`. If you are using a development copy and you are not a developer, consider installing an official release instead.

## Should I upgrade?

Here is a quick guide on how to evaluate each release based on its version number.

- Previous release `2.3.4` -> New release `2.3.5`: Only the PATCH component has been incremented. The new release only contains bugfixes --- no new features and no breaking changes. This is a reasonably safe upgrade and you may not even want to read the CHANGELOG.

- `2.3.5` -> `2.4.0`: The MINOR component has been incremented and the PATCH was reset to 0. This means that the new release includes one or more new features as well as zero or more bugfixes --- but no breaking changes. Upgrading to this new version is a bit more risky than the patch release in the previous example. New features may have introduced new bugs that were not caught before releasing. However, it does not contain a change that is expected to interfere with existing functionality. So it's still a reasonably safe upgrade. And you may want to read the CHANGELOG to see what the new features are.

- `2.4.0` -> `3.0.0`: MAJOR has been incremented and the other components reset. This means one or more breaking changes have been introduce. New features and bugfixes may also be included. In this case reading the CHANGELOG is a must. Something in the public interface has changed that may break how you were using the project before. Maybe a feature was renamed or removed. Or maybe the way it behaves is different. Make sure you know what you are getting into before upgrading to a new major release.
