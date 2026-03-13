______________________________________________________________________

## description: Sync working directory with remote repository - rebase, intelligently commit changes, and push to same branch name: sync agent: agent tools: \[todo, execute\]

## Sync Working Directory with Remote

This command synchronizes the local working directory with the remote repository using git with intelligent commit grouping.

### Step 0: Create Todo List for Sync Workflow

Initialize a todo list to track the remaining steps:

```
- [ ] Step 1: Get current branch
- [ ] Step 2: Rebase from upstream
- [ ] Step 3: Check .gitignore changes
- [ ] Step 4: Identify all changes
- [ ] Step 5: Analyze and group changes
- [ ] Step 6: Commit each group
- [ ] Step 7: Verify all changes committed
- [ ] Step 8: Push to remote
```

This todo list will be updated as you progress through the workflow.

### Step 1: Get Current Branch

Execute the following git command to determine the current branch:

```
git branch --show-current
```

Update todo list - mark Step 1 as completed.

### Step 2: Rebase from Upstream

Fetch the latest changes from all remotes:

```
git fetch --all
```

Rebase the current branch onto its upstream/remote branch:

```
git rebase
```

If there are merge conflicts, stop and ask the user how to resolve them before proceeding.

Update todo list - mark Step 2 as completed.

### Step 3: Check for .gitignore Changes

Check if there are any changes to .gitignore:

```
git status --porcelain .gitignore
```

**If .gitignore has changes:**

1. Stage the .gitignore changes: `git add .gitignore`
1. Use the **git-commit-workflow** skill to commit these changes with an appropriate message
1. After committing .gitignore changes, re-check the overall git status to identify all remaining files

Update todo list - mark Step 3 as completed.

### Step 4: Identify All Changes (Tracked and Untracked)

Check the overall git status to see all modified, staged, and untracked files:

```
git status --short
```

Update todo list - mark Step 4 as completed.

### Step 5: Analyze and Group Changes Intelligently

Based on the output from Step 4, analyze the changes to group them logically by:

- File type (e.g., all documentation files together, all code files together)
- Feature/component (e.g., all files related to a specific feature)
- Change type (e.g., all new features, all bug fixes, all documentation updates)

Create a list of logical file groups that would make sense as separate commits.

**Update the todo list with the identified file groups:**

- Create a new sub-todo list item for each logical group (e.g., "Commit: documentation updates", "Commit: feature X changes", etc.)
- Mark each sub-item as not-started so they can be tracked during Step 6

Update todo list - mark Step 5 as completed and add commit group sub-items.

### Step 6: Commit Each Group Using git-commit-workflow

For each logical group of changes:

1. Stage the files in that group: `git add <files>`
1. Use the **git-commit-workflow** skill to create an appropriate commit message following conventional commits format
1. The skill will commit the staged files with the generated message

**Important:** Repeat this process for each logical group until all tracked and untracked files have been committed.

Update todo list - mark each commit group sub-item as completed as you finish them. Mark Step 6 as completed when all groups are committed.

### Step 7: Verify All Changes Are Committed

Check that no more changes remain:

```
git status
```

Ensure the working tree is clean with no untracked or modified files.

Update todo list - mark Step 7 as completed.

### Step 8: Push to Remote

Push all commits to the remote repository with the same branch name:

```
git push origin <BRANCH_NAME>
```

Replace `<BRANCH_NAME>` with the branch name obtained in Step 1.

If the push fails (e.g., due to remote changes), inform the user and ask how to proceed (force push, rebase again, etc.).

Update todo list - mark Step 8 as completed.
