# Git Basics for NSQIP Researchers

This guide covers the essential Git commands you need for collaborative research. Don't worry about learning everything - just these basics will get you started.

## What is Git?

Git is like "track changes" for code. It lets you:
- Save versions of your work
- Share code with collaborators
- See what changed and when
- Recover previous versions if needed

## Essential Commands (The Only Ones You Need)

### 1. Getting Started Each Day

Always start by getting the latest changes from your collaborators:

```bash
git pull
```

This downloads any new work from the team.

### 2. Saving Your Work

After you make changes to your analysis, save them with these three commands:

```bash
# Step 1: See what files you changed
git status

# Step 2: Add your changes (usually your whole project folder)
git add projects/yourname-project/

# Step 3: Save with a message describing what you did
git commit -m "Added mortality analysis for diabetic patients"
```

### 3. Sharing Your Work

Send your changes to GitHub so others can see them:

```bash
git push
```

## Complete Daily Workflow Example

Here's what a typical work session looks like:

```bash
# 1. Start your day - get latest updates
git pull

# 2. Open your analysis notebook
uv run marimo edit --sandbox projects/smith-mortality/analysis.py

# ... work on your analysis ...

# 3. When done, save your work
git status                                    # See what changed
git add projects/smith-mortality/             # Add your changes
git commit -m "Completed age stratification"  # Save with message
git push                                      # Share with team
```

## Common Situations

### "I forgot to pull before starting work"

No problem! Git will tell you if there are conflicts. Usually:

```bash
git pull
# Git will merge changes automatically
# If there are conflicts, ask for help
```

### "I accidentally modified someone else's file"

Check what you changed:

```bash
git status
```

Undo changes to files you didn't mean to modify:

```bash
git checkout -- path/to/file
```

### "I want to see what I changed"

Before committing, see your actual changes:

```bash
git diff
```

### "I made a mistake in my commit message"

If you haven't pushed yet:

```bash
git commit --amend -m "New correct message"
```

## Good Commit Messages

Write messages that explain WHAT you did and WHY:

**Good examples:**
- "Added 30-day readmission analysis for cardiac procedures"
- "Fixed age grouping error in mortality table"
- "Updated README with preliminary findings"

**Not helpful:**
- "Updates"
- "Fixed stuff"
- "Analysis"

## What NOT to Do

1. **Never commit data files** - The .gitignore handles this, but always check
2. **Never commit passwords or data paths** - Keep these in your local notebook
3. **Don't modify shared/ folder** - Unless you're contributing utilities for everyone
4. **Don't worry about branches** - We keep it simple with just the main branch

## Getting Help

If you see an error message:

1. **Read it carefully** - Git messages usually tell you what to do
2. **Google the exact message** - Others have had the same problem
3. **Ask for help** - Screenshot the error and ask the team

## Visual Git Tools

If you prefer not to use the command line:

- **GitHub Desktop**: Free, simple interface ([download](https://desktop.github.com/))
- **VS Code**: Has built-in Git support if you use it for editing

But the commands above are all you really need!

## Quick Reference Card

Print this and keep it handy:

```
Daily workflow:
1. git pull                     # Get updates
2. git add projects/myproject/  # Stage changes
3. git commit -m "message"      # Save changes
4. git push                     # Share changes

Check status:
- git status                    # What changed?
- git diff                      # See changes
- git log --oneline -10         # Recent commits
```

Remember: Git is very forgiving. It's hard to permanently lose work, so don't be afraid to try commands. The worst case is usually just asking for help to undo something.