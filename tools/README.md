# tools

## import-repo.sh

Copies another Git repository into a folder of this repo **with its full commit
history**. Every commit keeps its author, date and message; only the file paths
move into the target folder.

```bash
tools/import-repo.sh <repo-url> "<target/folder>"
```

### Starting a course project (instead of forking)

When a course hands out a starter repo, import it straight into the week folder:

```bash
tools/import-repo.sh https://github.com/codepath/<starter-repo> "AI201/20270115 W03/Project/<project-name>"
```

Then work in that folder as usual: edit, commit, push. Nothing needs to be
migrated when the course ends.

If a course requires submitting a standalone repo link, fork as usual during the
course, then bring the fork in at the end:

```bash
tools/import-repo.sh https://github.com/thxsyyd/<project-name> "AI201/20270115 W03/Project/<project-name>"
```

### Notes

- Run it with a clean working tree. It refuses to write into a folder that already has tracked files.
- It creates one merge commit and does **not** push. Check the result with
  `git log --oneline -- "<target/folder>"`, then push.
- Commit IDs of the imported history change, because the file paths change.
- Untracked files such as `.env` are never imported.
