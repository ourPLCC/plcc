You must have write permissions on this repository to use this workflow.

## Clone this project

```bash {.line-numbers}
git clone https://github.com/ourPLCC/plcc.git
cd plcc
```

You only need to clone the repository once. Or if you ever delete your local clone.


## Proposing a Change

In the commands below, replace `feature` with a short descriptive name for your branch.

```bash {.line-numbers}
git switch master
git pull origin master
git switch -c feature
vim ... ; mv ... ; mkdir ... ; rm ...
git add .
git commit -m "short descriptive message"
git push -u origin feature
... # Navigate to URL printed to create a merge-request.
```

- 1-3: Create a new branch based on the most recent copy of `master`.
- 4: Use your favorite tools to make and test changes.
- 5-6: Stage and commit your changes.
- 7-8: Publish your branch and create a pull-request.


## Update a Feature Branch

If you are asked to update a feature branch with new changes in master.

```bash {.line-numbers}
git switch master
git pull origin master
git switch feature
git merge master
vim ... ; mv ... ; mkdir ... ; rm ...
git add .
git merge --continue
git push origin feature
```

- 1-4: Merge the new changes into your feature branch.
- 5-7: Resolve conflicts if any; otherwise move on to 8.
- 8: Push the merged branch. This also updates the merge-request.

## Cleaning up

After your pull-request is merged, you can clean up your local clone as follows.

```bash {.line-numbers}
git switch master
git pull origin master
git branch -d feature
git push origin --delete feature
git pull --prune
```

- 1-2: Update master with the new changes.
- 3: Delete the feature branch locally. If this gives you an error, and you're sure your changes are in master, repeat the command with -D (capital d).
- 4: Delete the feature branch remotely. If the remote branch was already deleted, you'll get an error which you can safely ignore.
- 5: Delete the local reference to the remote branch you just deleted.
- 6: Remove the reference to the remote branch that was just deleted.