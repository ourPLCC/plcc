# Contributing Guide

## Overview

- Never commit to master.
- Only commit work to personal feature branches.
- Always cut feature branches from the most recent version of master.
- Contribute changes by publishing your feature branch and issueing a
  pull-request to master in the original repository.

There are several ways to contribute. Below I describe two common ways.  The
first assumes you do not have write privileges to the repository, the second
are for those who do have write privileges. Anyone can use the first. Only
those who have been granted write privileges can use the second. If you would
like to apply for write privileges, please open an issue requesting access, and
explain why.

## Contributing with a fork

This proceedure does not require any special privileges to contribute changes.

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

# 5. Make sure you are on master.
git checkout master

# 6. Make sure you have the most recent version of master.
git pull upstream master

# 7. Push the most recent version of master to your fork.
git push origin master

# 8. Create a feature branch (name your branch something meaningful).
git checkout -b sj-fix-typo-in-readme

# 9. Make the change(s) using your favorite tools (replace these commands with whatever makes sense).
vim README.md

# 10. Stage your changes
git add .

# 11. Commit your changes (use conventional commit messages; see below)
git commit -v

# 12. Publish your feature branch
git push -u origin sj-fix-typo-in-readme

# 13. Return to master branch
git checkout master
```

14. In your fork on GitHub, create a pull-request from your feature branch
    (in this case, sj-fix-typo-in-readme) to master in the original project.

15. In the pull-request, request a review by placing @ourPLCC/core in a
    comment.

## Contributing with write privileges

If you have write privileges, you can contribute using the fork proceedure
described above, or modify the fork proceedure as follows:

- Don't fork.
- Don't create an upstream remote.
- Update your local master by pulling from origin's master:
    ```
    git checkout master
    git pull origin master
    ```

## Use conventional commit messages

- Short overview <https://seesparkbox.com/foundry/semantic_commit_messages>
- Full specification <https://www.conventionalcommits.org/en/v1.0.0/>

## Updating a pull-request using a fork

We try to keep our git graph linear so that it is more easily understood.  If
someone else's pull-request is merged before yours, you will likely be asked to
update your pull-request. This section describes how you do that.

Let's assume that your pull-request is associated with the feature branch
`sj-fix-typo-in-readme`. Let's also assume that you are working in a fork,
and you have a remote named `upstream` that refers to the original project.
If you followed the "Contributing with a fork" proceedure above, then you
should be ready to follow these instructions. If you followed the "

```bash
git checkout master
git pull upstream master
git checkout sj-fix-typo-in-readme
git merge master
```

The last command tries to merge the changes from master into your feature
branch (the currently checked out branch).  Your changes may not be compatible
with the new changes in master. If Git detects a lexical conflict, it will stop
the process and will expect you to resolve the conflicts. Checkout GitHub's
documentation on [Resolving a merge conflict using the command
line](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/resolving-a-merge-conflict-using-the-command-line).

Even if Git does not detect a conflict and finished rebasing "successfully",
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

## Updating a pull-request with write privileges

Same as "Updating a pull-request using a fork", except pull changes from origin
instead of upstream:

```bash
git checkout master
git pull origin master
```

