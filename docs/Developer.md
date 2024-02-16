# Contributing

First, thanks for your interest in contributing to this project.
This guide is a good place to start. Please also [join our Discord server](https://discord.gg/EVtNSxS9E2).

## License

* GPLv3.0 or higher - First, because this project is licensed under GPLv3, all contributions must be licensed under the same license.
* DCO - By contributing to this project, you agree to the [Developer Certificate of Origin](https://developercertificate.org/); essentially certifying that the work you are submitting may be legally licensed under this project's license: GPLv3.0 or higher.

## Overview

- Never commit to main.
- Only commit work to personal feature branches.
- Always cut feature branches from the most recent version of main.
- Contribute changes by publishing your feature branch and issuing a
  pull-request to main in the original repository.

There are several ways to contribute. Below I describe two common ways.  The
first assumes you do not have write privileges to the repository, the second
are for those who do have write privileges. Anyone can use the first. Only
those who have been granted write privileges can use the second. If you would
like to apply for write privileges, please open an issue requesting access, and
explain why.

## Contributing with a fork

This procedure does not require any special privileges to contribute changes.

In the example below, I'll be fixing a typo in the README.md of this project.
Below are values that are unique to this example. You could replace them with
values that make sense in your context.

1. From GitHub, fork this project <https://github.com/ourPLCC/>.

```bash
# 2. Clone your fork (first time only; replace the URL with your fork's URL).
git clone https://github.com/StoneyJackson/PROJECT.git

# 3. Change into the root of the project.
cd PROJECT

# 4. Create a remote pointing to the original project (first time only).
git remote add upstream https://github.com/ourPLCC/PROJECT.git

# 5. Make sure you are on main.
git checkout main

# 6. Make sure you have the most recent version of main.
git pull upstream main

# 7. Push the most recent version of main to your fork.
git push origin main

# 8. Create a feature branch (name your branch something meaningful).
git checkout -b sj-fix-typo-in-readme

# 9. Make the change(s) using your favorite tools (replace these commands with whatever makes sense).
vim README.md

# 10. Stage your changes
git add .

# 11. Commit your changes
git commit -v

# 12. Publish your feature branch
git push -u origin sj-fix-typo-in-readme

# 13. Return to main branch
git checkout main
```

14. In your fork on GitHub, create a pull-request from your feature branch
    (in this case, sj-fix-typo-in-readme) to main in the original project.

15. In the pull-request, request a review by placing @ourPLCC/core in a
    comment.

### Updating a pull-request using a fork

We try to keep our git graph linear so that it is more easily understood.  If
someone else's pull-request is merged before yours, you will likely be asked to
update your pull-request. This section describes how you do that.

Let's assume that your pull-request is associated with the feature branch
`sj-fix-typo-in-readme`. Let's also assume that you are working in a fork,
and you have a remote named `upstream` that refers to the original project.
If you followed the "Contributing with a fork" procedure above, then you
should be ready to follow these instructions.

```bash
git checkout main
git pull upstream main
git push origin main
git checkout sj-fix-typo-in-readme
git merge main
```

The last command tries to merge the changes from main into your feature
branch (the currently checked out branch).  Your changes may not be compatible
with the new changes in main. If Git detects a lexical conflict, it will stop
the process and will expect you to resolve the conflicts. Checkout GitHub's
documentation on [Resolving a merge conflict using the command
line](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/resolving-a-merge-conflict-using-the-command-line).

Even if Git does not detect a conflict and finished merging "successfully",
there may be a logical conflict. The only way to detect logical conflicts is
through testing (e.g., manual inspection, running automated tests, manual
testing, etc.). Perform suitable tests and make and commit any necessary fixes.

Once you are satisfied, update your pull-request by pushing your changes to the
associated feature branch in your fork.

```
git push origin sj-fix-typo-in-readme
```

This will automatically update the pull-request. Return to the pull-request on
GitHub and request a review from @ourPLCC/core.

## Contributing without a Fork

You must have write permissions on this repository to use this workflow.

### Clone this project

```bash {.line-numbers}
git clone https://github.com/ourPLCC/plcc.git
cd plcc
```

You only need to clone the repository once. Or if you ever delete your local clone.

### Proposing a Change

In the commands below, replace `feature` with a short descriptive name for your branch.

```bash {.line-numbers}
git switch main
git pull origin main
git switch -c feature
vim ... ; mv ... ; mkdir ... ; rm ...
git add .
git commit -m "short descriptive message"
git push -u origin feature
... # Navigate to URL printed to create a merge-request.
```

- 1-3: Create a new branch based on the most recent copy of `main`.
- 4: Use your favorite tools to make and test changes.
- 5-6: Stage and commit your changes.
- 7-8: Publish your branch and create a pull-request.

### Update a Feature Branch

If you are asked to update a feature branch with new changes in main.

```bash {.line-numbers}
git switch main
git pull origin main
git switch feature
git merge main
vim ... ; mv ... ; mkdir ... ; rm ...
git add .
git merge --continue
git push origin feature
```

- 1-4: Merge the new changes into your feature branch.
- 5-7: Resolve conflicts if any; otherwise move on to 8.
- 8: Push the merged branch. This also updates the merge-request.

### Cleaning up

After your pull-request is merged, you can clean up your local clone as follows.

```bash {.line-numbers}
git switch main
git pull origin main
git branch -d feature
git push origin --delete feature
git pull --prune
```

- 1-2: Update main with the new changes.
- 3: Delete the feature branch locally. If this gives you an error, and you're sure your changes are in main, repeat the command with -D (capital d).
- 4: Delete the feature branch remotely. If the remote branch was already deleted, you'll get an error which you can safely ignore.
- 5: Delete the local reference to the remote branch you just deleted.
- 6: Remove the reference to the remote branch that was just deleted.

## Testing

### Dependencies

* PLCC
* Bash 5+
* [bats 1.2+](https://bats-core.readthedocs.io/en/latest/index.html).

### Test everything

```bash
bin/test/all.bash
```

### Test functionality

```bash
bin/test/functionality.bash
```

### Test other things

See ...

```bash
ls bin/test/
```

### Running the tests inside the official container.

Build and run the PLCC container...

```bash
containers/plcc/build.bash
containers/plcc/run.bash
```

You are now running inside the PLCC container. Now run the tests.

```bash
/plcc/tests/run
```

### Writing Tests

See [Bats documentation](https://bats-core.readthedocs.io/en/latest/index.html).
Place tests in `tests/plcc`. See existing tests for examples.


## Version Numbers

### What version of PLCC am I running?

You can determine what version of PLCC you have by running


```bash
plcc --version
```

### What does PLCC's version number mean?

PLCC uses [Semantic Versioning](https://semver.org/). Each release has a version number containing three numeric components: MAJOR.MINOR.PATCH. These components encode important information about the types of changes that have been made since the last release. This helps you decide if and when to upgrade to newer versions and how much time you should spend reading the CHANGELOG.

### What's with the `-dev.0`?

In between official releases are development releases. The version number for a development release is suffixed with `-dev.0`. For example, `2.3.4-dev.0`. If you are using a development copy and you are not a developer, consider installing an official release instead.

### Should I upgrade?

Here is a quick guide on how to evaluate each release based on its version number.

- Previous release `2.3.4` -> New release `2.3.5`: Only the PATCH component has been incremented. The new release only contains bugfixes --- no new features and no breaking changes. This is a reasonably safe upgrade and you may not even want to read the CHANGELOG.

- `2.3.5` -> `2.4.0`: The MINOR component has been incremented and the PATCH was reset to 0. This means that the new release includes one or more new features as well as zero or more bugfixes --- but no breaking changes. Upgrading to this new version is a bit more risky than the patch release in the previous example. New features may have introduced new bugs that were not caught before releasing. However, it does not contain a change that is expected to interfere with existing functionality. So it's still a reasonably safe upgrade. And you may want to read the CHANGELOG to see what the new features are.

- `2.4.0` -> `3.0.0`: MAJOR has been incremented and the other components reset. This means one or more breaking changes have been introduce. New features and bugfixes may also be included. In this case reading the CHANGELOG is a must. Something in the public interface has changed that may break how you were using the project before. Maybe a feature was renamed or removed. Or maybe the way it behaves is different. Make sure you know what you are getting into before upgrading to a new major release.
