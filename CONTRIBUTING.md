# Contributing Guide

## Overview

- Never commit to master.
- Only commit work to personal feature branches.
- Always cut feature branches from the most recent version of master.
- Contribute changes by publishing your feature branch and issueing a
  pull-request to master in the original repository.

## Contributing with a fork

The proceedure does not require any special privileges to contribute changes.

In the example below, I'll be fixing a typo in the README.md of this project.
Below are values that are unique to this example. You could replace them with
values that make sense in your context.

1. From GitHub, fork this project <https://github.com/ourPLCC/>.

```bash
# 2. Clone your fork (first time only; replace the URL with your fork's URL).
git clone https://github.com/StoneyJackson/course.git

# 3. Change into the root of the project.
cd course

# 4. Create a remote pointing to the original project (first time only).
git remote add upstream https://github.com/ourPLCC/course.git

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

