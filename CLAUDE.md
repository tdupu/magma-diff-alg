# Project Instructions for AI Agents

This file provides instructions and context for AI coding agents working on this project.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:6cd5cc61 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files, validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close beads, run quality gates, commit, and push as part of session close. A current "do not commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:
   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status

   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   git push
   git status
   ```
5. **Hand off** - Summarize changes, validation, issue status, and any blocked sync/commit/push step

**Critical rules:**
- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current user request.
- If a required sync or push is blocked, stop and report the exact command and error.
<!-- END BEADS INTEGRATION -->


## Build & Test

Governed by **LAYOUT.md § Testing infrastructure (TS1–TS5)**. Read it before
touching a test; two of the rules are not guessable.

```bash
# Run a test — FROM ITS OWN DIRECTORY. The AttachSpec is relative (TS1, TS5).
cd test-valuations
/Applications/Magma/magma -b test_initial_ideal_intrinsic.mag
echo $?          # 0 = pass, 1 = fail
```

**Three things that will bite you, all measured 2026-09-20:**

1. **Never use an absolute `AttachSpec` path.** Six tracked tests used
   `AttachSpec("/Users/tdupuy/repos/magma-diff-alg/diffalg.spec")`, so this
   checkout's tests were silently loading *another checkout's* spec. The
   convention is `AttachSpec("../diffalg.spec")` from a test directory.

2. **`SetQuitOnError(true)` does NOT catch a failed `AttachSpec`.** It converts
   a later runtime error to exit 1, but a spec that never loaded exits **0** —
   the test runs against nothing and reports success. All 7 tracked tests now
   carry an attach-proof immediately after the attach:

   ```magma
   assert IsIntrinsic("differentialPolynomialRing"); // TS2: prove the spec attached
   ```

   Keep it. Without it, the most common failure mode in this repo is invisible.

3. **`magma … | head` reports the exit status of `head`, not Magma.** Use
   `${PIPESTATUS[0]}`, or do not pipe.

There is no test runner yet — LAYOUT.md TS3 specifies what one must do
(check exit code **and** grep stdout for a success sentinel). Writing it is
open work, registered in LAYOUT.md's Brownfield register.

## Architecture Overview

_Add a brief overview of your project architecture_

## Conventions & Patterns

_Add your project-specific conventions here_
