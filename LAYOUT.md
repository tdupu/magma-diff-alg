# LAYOUT.md — repository layout contract

| Field | Value |
| --- | --- |
| Repo | `magma-diff-alg` |
| Status | Draft |
| Date | 2026-09-20 |
| Approved by | `<human name — required before Status: Adopted>` |
| Checked by | `check-layout` |
| Amended by | `new-repo-layout-policy` |

What goes where, what is canonical, what is kept-but-ignored. The tree is the
TARGET state; deviations live in the Brownfield register.

## Tree

```
magma-diff-alg/
├── package-*.mag        ← the Magma package sources; 10 files, repo root
├── diffalg.spec         ← THE spec. Root-level. Every test attaches this one.
├── test-valuations/     ← .mag tests + .out expected-output fixtures + .py/.txt data
├── test-homog/          ← notebook-form tests (.ipynb)
├── ai/                  ← durable agent-generated investigations; dated dirs
├── scratch/             ← genuinely transient output (LY3); disposable
├── LAYOUT.md            ← this file: layout + the TS testing rules
├── AGENTS.md  CLAUDE.md ← agent entry points; both point here for tests
├── CONTEXT.md           ← domain glossary; designated-migrator declaration
├── README.md            ← the handbook/progress bar for package convergence
└── ── gitignored but KEEP on disk ──
    .agents/  crew/  mayor/  polecats/  refinery/  plugins/  settings/
    witness/  mda-*/      ← gc rig scaffolding, never repo content (LY1)
```

## Testing infrastructure (TS rules)

**TS1 — One spec, attached relatively [C].** `diffalg.spec` lives at the repo
root and is the only spec a test attaches. A test in a directory one level down
uses `AttachSpec("../diffalg.spec")`. **No absolute path, ever** — an absolute
path silently binds the test to one checkout. Measured 2026-09-20: six tracked
tests carried `AttachSpec("/Users/tdupuy/repos/magma-diff-alg/diffalg.spec")`,
so `~/gt`'s tests were loading a *different checkout's* spec. Fixed in this
commit; `test-valuations/` is now uniform at 7/7.
- Pass: `git ls-files -z '*.mag' | xargs -0 grep -l 'AttachSpec("/'` returns
  nothing.
- Fail: any match.
- **Scope the check to `*.mag`.** An unscoped grep also matches the prose in
  this file and in `CLAUDE.md`, which quote the forbidden pattern in order to
  forbid it — so the rule's own statement would fail the rule. Documentation
  that names a bad pattern is not an instance of it.

**TS2 — A test must PROVE its spec attached [C].** This is the rule that
matters and it is not obvious. `SetQuitOnError(true)` does **not** make a failed
`AttachSpec` non-zero. Measured, with both controls, 2026-09-20:

| case | guard | exit |
| --- | --- | --- |
| clean script | on | 0 |
| runtime error after the guard | on | 1 |
| **failed `AttachSpec`** | on, set before the attach | **0** |

So a test whose spec did not load runs every intrinsic against nothing, fails,
and **reports success**. Guard presence is not protection: all 6 tracked tests
already call `SetQuitOnError(true)` and all 6 were exposed.
- Pass: every `.mag` test calls a known intrinsic from the spec immediately
  after attaching, so a non-loaded spec raises a runtime error — which the guard
  *does* convert to exit 1.
- Fail: a test that attaches and proceeds straight to work.

**TS3 — Exit code alone is not a verdict [C].** Because of TS2, a runner must
check BOTH the exit code AND stdout. A test ends with an explicit success
sentinel on its last line; the runner greps for it.
- Pass: runner asserts exit 0 **and** the sentinel present.
- Fail: a runner branching on `$?` alone.
- Note: `magma … | head` reports the exit status of `head`. Use
  `${PIPESTATUS[0]}` or no pipe.

**TS4 — Expected-output fixtures are tracked [C].** `test-valuations/*.out` are
committed Magma outputs used as comparison fixtures (7 files) — repository
content, not build output. **Never add `*.out` to `.gitignore`.** Generic
repo-doc templates ban `*.out` as a LaTeX byproduct; that rule does not apply
here and adopting it would untrack the fixtures.
- Pass: `git ls-files 'test-valuations/*.out'` returns 7.
- Fail: fewer, or an `*.out` entry in `.gitignore`.

**TS5 — Tests are run from their own directory [C].** TS1's relative path is
resolved against the process working directory, not the script location.

**TS6 — Magma `.sig` files are byproducts [C].** `package-*.sig` are compiled
signatures, regenerated on attach. Never tracked.
- Pass: `git ls-files '*.sig'` returns nothing.

## .gitignore stanza

**This is not a LaTeX repository** — zero `.tex` files and zero LaTeX
byproducts, measured 2026-09-20. The template's LaTeX byproduct list is
deliberately absent. (`package-latex.mag` *emits* LaTeX; that does not make
this a LaTeX tree.) The `*.pdf` ban is kept on its own footing: the standing
ruling is that PDFs are never tracked, anywhere, whatever produced them.

```gitignore
*.pdf     ← standing ruling; the rule is on what a file IS, not where it sits
*.sig     ← Magma compiled signatures (TS6)
# *.out is deliberately NOT here — see TS4; those are tracked fixtures.
.agents/  crew/  mayor/  polecats/  refinery/  plugins/  settings/  witness/
mda-*/    ← gc rig scaffolding; keep on disk, never tracked
.repo.git/  .beads/  .gc/  config.json   ← git/beads/gc internals
scratch/
```

## Brownfield register (pending cleanup — NOT part of the contract)

| Current state | Target disposition |
| --- | --- |
| `.agents/` (124 files), `crew/`, `mayor/`, `polecats/`, `refinery/`, `plugins/`, `settings/`, `witness/`, 9 × `mda-*/` — untracked gc scaffolding at root | keep-untracked (gitignore + tree row) — **awaiting human confirmation** |
| `README.md` carries BOTH `AttachSpec("diffalg.spec")` and `AttachSpec("../diffalg.spec")`; one is wrong depending on the reader's cwd | **work, not a decision** — correct form is derivable from TS1. Filed and dispatched 2026-09-22 |
| `test-homog/` holds only `.ipynb`; no `.mag` tests and no runner | TBD (human) — is notebook-form a supported test type? |
| No runner exists for `test-valuations/` | **work, not a decision** — TS3 states the contract in full. Filed `mda-fn4` (P1) and dispatched 2026-09-22 |
| ~~`CLAUDE.md` + `CONTEXT.md` untracked at root~~ | **RESOLVED 2026-09-22** — both tracked as of `748c885`; verified with `git ls-files --error-unmatch` |

## Rules

**Scope.** This repo carries `LAYOUT.md` and nothing else from the repo-doc
template family. `LATEX.md`, `STYLE.md`, `ADR.md` and `AI-POLICY.md` were
instantiated 2026-09-20 and **removed the same day**: no `.tex` here, and four
generic contracts nobody wrote for this repo are noise, not governance. **A
check reporting their absence is applying the wrong template**; the LY5 "six
repo docs" predicate does not bind here.

- **LY1 — clean tree.** Packages, spec, tests, README, this file. No
  scaffolding tracked.
- **LY2 — tree + register are total.** Every top-level dir and tracked root
  file has a row above or below.
- **LY3 — transient output to `scratch/`.**
- **LY7 — naming:** lowercase, hyphen-separated. Existing underscore names are
  register rows, not silent violations — not renamed in the same pass that
  changed their contents.
- **LY8 — few folders.** A new top-level dir needs an amendment.
- **LY9 — PDFs never tracked**, per the standing ruling. The LaTeX-byproduct
  half is not carried; see the stanza above.

`scratch/` and `ai/` are **non-canonical**: not the published artifact, and
every audit scoping by non-canonical content excludes both.
