# Contributing

First, thanks for your interest in contributing to this project.
This guide is a good place to start. Please also [join our Discord server](https://discord.gg/EVtNSxS9E2).

## License

* GPLv3.0 or higher - This project is licensed under GPLv3. All contributions
    must be licensed under the same.
* DCO - By contributing to this project, you are signing off on the
    [Developer Certificate of Origin](https://developercertificate.org/),
    certifying that the work you are submitting may be legally licensed
    under GPLv3.0 or higher.

## Development Environment

Use GitPod and it's VS Code in Browser IDE.
Before you begin, you'll need the following accounts.

* GitHub Account
* GitPod Account

We also recommend that you install a GitPod extension for your browser
(search your browser's extension marketplace for GitPod).

## Overview

- Never commit to main.
- Only commit work to personal feature branches.
- Always cut feature branches from the most recent version of main.
- Contribute changes by publishing your feature branch and issuing a
  pull-request to main in the original repository.
- If the change you have in mind is time consuming, have a conversation
    about it on an issue before doing the work. This will help
    improve the chances of your hard work being merged.
- The longer a PR is open, the less likely it will be merged. This is not
    a policy, just reality. Keep your PRs focused, and help them get merged.

There are several ways to contribute. Below I describe two common ways.  The
first assumes you do not have write privileges to the repository, the second
are for those who do have write privileges. Anyone can use the first. Only
those who have been granted write privileges can use the second. If you would
like to apply for write privileges, please open an issue and explain why.

## Contributing with a fork

This procedure does not require any special privileges to contribute changes.

1. If you have not already done so, fork this project <https://github.com/ourPLCC/plcc>.

1. Open your fork in GitPod. Use VS Code in Browser for your IDE.

1. Synchronize main

    ```bash
    git pull upstream main
    git push upstream main
    ```

1. Create a feature branch.

    ```bash
    git switch -c my-feature-branch
    ```

1. Use the VS Code in Browser IDE to make changes.

1. Stage and commit your changes.

    ```bash
    git stage .
    git commit -m "reasonable commit message here"
    ```

1. Push your branch and create a pull request.

    ```bash
    git push origin my-feature-branch
    ```

    This will print a URL to create a merge request.
    Follow it, fill out the form, and submit it.

1. Stop your GitPod workspace and never use it again.

    ```bash
    gp stop
    ```

1. Draft a final commit message in the first message of the PR. Use
    [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
    for the subject of the commit message. Be sure to list related issues
    and if the PR fully addresses the issue, use "Closes #NN` syntax.
    If multiple people contributed to the PR, use a `Co-authored-by:`
    for each including yourself. When merged, your commits will be
    squashed into a single commit, and the `Co-authored-by:` will give
    you and other contributors credit.

1. When your MR is ready for review, assign one of the maintainers as a
    reviewer. Work with the maintainer to get your code into shape and merged.

### Updating a pull-request using a fork

1. Open your fork or the PR in GitPod.
1. Synchronize main.
    ```bash
    git switch main
    git pull upstream main
    git push upstream main
    ```
1. Merge main into your feature branch.
    ```main
    git switch my-feature-branch
    git merge main
    ```
    Resolve any conflicts, make any additional changes.
    ```main
    git stage .
    git commit -m "reasonable message"
    git push origin my-feature-branch
    ```
1. Stop the GitPod workspace, and never use it again.
    ```bash
    gp stop
    ```

This will automatically update the pull-request. Return to the PR on
GitHub and request a review from @ourPLCC/core.

Checkout GitHub's documentation on
[Resolving a merge conflict using the command line](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/resolving-a-merge-conflict-using-the-command-line).

## Contributing without a Fork

You must have write permissions on this repository to use this workflow.

1. Open this repository in GitPod.
1. Create and switch to a feature branch.
    ```bash
    git branch my-feature-branch
    git switch my-feature-branch
    ```
1. Make, stage, and commit changes to the feature branch.
1. Push the feature branch to origin.
1. Create an PR using the link in the previous step.
1. Stop your GitPod workspace and never use it again.
    ```bash
    gp stop
    ```
1. Draft a final commit message in the first message of the PR. Use
    [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
    for the subject of the commit message. Be sure to list related issues
    and if the PR fully addresses the issue, use "Closes #NN` syntax.
    If multiple people contributed to the PR, use a `Co-authored-by:`
    for each including yourself. When merged, your commits will be
    squashed into a single commit, and the `Co-authored-by:` will give
    you and other contributors credit.
1. When your MR is ready for review, assign one of the maintainers as a
    reviewer. Work with the maintainer to get your code into shape and merged.

### Update a Feature Branch

1. Open the PR in GitPod.
1. Merge main into your feature branch.
    ```main
    git switch my-feature-branch
    git merge main
    ```
    Resolve any conflicts, make any additional changes.
    ```main
    git stage .
    git commit -m "reasonable message"
    git push origin my-feature-branch
    ```
1. Stop the GitPod workspace, and never use it again.
    ```bash
    gp stop
    ```

This will automatically update the pull-request. Return to the PR on
GitHub and request a review from @ourPLCC/core.

Checkout GitHub's documentation on
[Resolving a merge conflict using the command line](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/resolving-a-merge-conflict-using-the-command-line).

## Testing

Open this project in GitPod, and then do one of the following.

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
