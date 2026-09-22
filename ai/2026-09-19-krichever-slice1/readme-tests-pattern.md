# hecke README ↔ README-tests: measured mechanics, and the port to magma-diff-alg

**Measured 2026-09-20** against `/Users/tdupuy/repos/hecke` (read-only) and
`/Users/tdupuy/repos/magma-diff-alg` (read-only). Nothing was modified in either repo.
Every claim below cites a path; where I could not measure something I say so.

---

## 0. Inventory (measured)

`/Users/tdupuy/repos/hecke/magma/test/README-tests/` holds **78 files**:

| Kind | Count |
|---|---|
| `.mag` (executable Magma tests) | 52 |
| `.md` (prose sidecar notes) | 26 |

Of the 26 `.md` files, **19 have no `.mag` sibling** in that directory — they are
prose-only notes about tests that live elsewhere (`magma/test/test-cones-poc-*.mag`,
`test-polyhedra-A-*.mag`, `test-side-pairing-*.mag`, etc.), plus two non-test docs
(`sl2-data-fixture-setup.md`, `mre-sub-issue-A5-irrational-height.md`).
Only 7 `.md` files are true `<name>.mag` + `<name>.md` pairs.

**So `README-tests/` is not a pure test directory.** It is a mixed directory of
executable section-mirror tests, deep-coverage tests, and prose notes.

---

## 1. Naming convention

Two conventions coexist, and hecke's own layout policy only documents the first.

### 1a. Numbered section-mirror tests (the documented convention)

```
test-NN-<kebab-case-topic>.mag
```

`NN` is a **sequential suite index, not an issue number** — it counts README sections
in order, 01…46. `/Users/tdupuy/repos/hecke/POLICY.md:136` states it:

```
| `README-tests/test-NN-<name>.mag` | `test-01-attaching-and-clifford.mag` | Sequential regression suite backing the READMEs |
```

Three real filenames:

- `test-01-attaching-and-clifford.mag`
- `test-19-modular-symbols.mag`
- `test-45-lorentz-cones.mag`

**The numbering is not clean.** Measured gaps and collisions:
- `test-38-…` is listed in the README table but **is not on disk**.
- `test-40-hecke-commute-sentinel.mag` is on disk but **not in the README table**.
- `44` is used **twice**: `test-44-betti-gamma0-gate.mag` and
  `test-44-twelve-squares-smoke.mag`.
- `test-312-mre-segfault.mag` is cited from a table cell but lives in
  `magma/test/`, not in `README-tests/` (the `NNN` = issue-number convention,
  `POLICY.md:135`, which is a *different* naming rule for the parent test dir).

### 1b. Un-numbered deep-coverage tests (undocumented, 8 files)

```
test-<topic>.mag        # no number at all
```

- `test-hyppolt-cone-meet.mag`
- `test-halfspace-to-cone.mag`
- `test-cone-first-refactor-golden.mag`

These are **absent from the README coverage table** (all 7 un-numbered `.mag` files
plus `test-40` are missing from it — measured by diffing table rows against `ls`).
They are reachable only from `magma/README-cones.md:238-241`, a *second*, topic-local
table. `README.md:2516` calls them "Deep coverage … in `magma/test/README-tests/`"
and names five of them in prose.

### 1c. Sidecar notes

```
<same-basename>.md
```
e.g. `test-45-lorentz-cones.mag` + `test-45-lorentz-cones.md`. 7 pairs exist; the
other 19 `.md` files are orphans (§0).

---

## 2. Linkage — how a reader gets README → test → README

**Explicit linkage EXISTS, and it is bidirectional. This is the load-bearing part of
the convention.** Four mechanisms, all measured:

### 2a. README → test: a coverage table (`README.md:3356`)

`/Users/tdupuy/repos/hecke/README.md:3356` opens a section literally titled
**`**README-tests coverage:**`** followed by a two-column table:

```markdown
| File | README section |
|------|----------------|
| `test-01-attaching-and-clifford.mag` | Attaching The Package + Basic Clifford Algebras |
| `test-02-orders.mag` | Orders in Clifford Algebras + Order Equality, Membership, and the Star Involution |
| `test-03-units.mag` | Units |
```

The table runs 46 rows, `test-01` … `test-46`. Cells are free prose, and the later
rows carry issue numbers and bead ids inline, e.g.:

```markdown
| `test-44-betti-gamma0-gate.mag` | Betti numbers of Γ₀(α) (Option B gate) — `betti_numbers(O : Gammaquo)`, b_1 = `relative_h1` rank, rank formula at Γ₀(2+i), positive b_1 = 1 pin at Γ₀(4+7i), `O`psl2` idempotence (#329) |
```

### 2b. test → README: a comment header in every test file

Each `.mag` opens with a header naming the README section it mirrors. **Two header
dialects, both in active use** (measured over all 52 files):

- `Covers README section "<Name>".` — **12 files** (the older `test-01`…`test-12` era):

```magma
// test-02-orders.mag
// Covers README section "Orders in Clifford Algebras".
```

- `— README coverage for: <Name>` + an explicit run line — **34 files** (the newer
  form, and the one the skill template prescribes):

```magma
// test-45-lorentz-cones.mag — README coverage for: Lorentz Cones: meet, subset, and emptiness
// Run from magma/test/README-tests/:  magma test-45-lorentz-cones.mag
```

- **6 files have neither** and name no README section at all:
  `test-40-hecke-commute-sentinel.mag`, `test-46-positive-hrank-pdet6812-experiment.mag`,
  `test-canonical-coset-minimize-perms.mag`, `test-cone-first-refactor-golden.mag`,
  `test-halfspace-to-cone.mag`, `test-hyppol-cone-from-halfspaces.mag`.
  `test-46`'s header points at a **bead** instead (`// Bead: he-t0c9.`).

### 2c. The prose contract (`README.md:3333`)

```markdown
**Running the Code**

Every code example in this README is exercised by a matching Magma test file
under [`magma/test/README-tests/`](magma/test/README-tests/).  When you
change the code, run those tests and update the README so the two stay in sync.
```

and at `README.md:3347`:

```markdown
- `README-tests/` — one file per README section, run from `magma/test/README-tests/`
  using `../../hecke.spec`. Each file ends with `<filename>: OK` on success and
  skips gracefully when required `DATA/` files are absent.
```

### 2d. Sidecar `.md` cross-ref blocks

The 7 paired `.md` files carry an explicit **`**Cross-refs:**`** section pointing back
at the README section and sideways at sibling tests
(`test-45-lorentz-cones.md`):

```markdown
**Cross-refs:**
- `README.md §Lorentz Cones: meet, subset, and emptiness` — the section this file mirrors
- `magma/README-cones.md` §5 — index of cone-architecture worked examples
- `test-hyppol-cone-from-halfspaces.mag` — halfspace-path construction in depth
```

They also carry `**Purpose:**`, `**Runtime:**`, `**What it covers:**` (a bullet list of
pinned values), and `**Gotchas:**`.

### 2e. Where the linkage is BROKEN (measured, not inferred)

Diffing the `README.md:3356` table against `ls magma/test/README-tests/*.mag`:

- **In the table, not on disk:** `test-38-load-gamma0-fp.mag`, `test-312-mre-segfault.mag`.
- **On disk, not in the table (8 files):** `test-40-hecke-commute-sentinel.mag`,
  `test-canonical-coset-minimize-perms.mag`, `test-cone-first-refactor-golden.mag`,
  `test-halfspace-to-cone.mag`, `test-hyppol-cone-from-halfspaces.mag`,
  `test-hyppolt-cone-action.mag`, `test-hyppolt-cone-meet.mag`,
  (`test-41-facets-on-FD.mag` IS in the table).

So the table covers **44 of 52** on-disk `.mag` files and names 2 files that are not
there. **Nothing enforces the table** — it is maintained by hand. This is the single
most important thing to fix when porting: the table is the only README→test index, and
it silently drifts.

---

## 3. Boilerplate — what a test file contains at the top

The measured boilerplate over 52 files:

| Line | Files carrying it |
|---|---|
| `AttachSpec("../../hecke.spec");` | 48 / 52 |
| `SetLMFDBRootFolder("../../");` | 49 / 52 |
| `SetVerbose("Clifford", 0);` | 50 / 52 |
| `Z := Integers(); Q := Rationals();` | ~all (two spellings: one line or two) |
| `SetQuitOnError(...)` | **0 / 52** |
| final `print "<file>: OK"` | 46 / 52 |
| trailing bare `quit;` | 24 / 52 |

Note the relative paths are **two levels up** (`../../`), because the tests sit one
directory deeper than `magma/test/`. Hecke's `CLAUDE.md` working-directory table says
`../hecke.spec` for `magma/test/` scripts; `README-tests/` needs `../../hecke.spec`.

### A short complete example file

`/Users/tdupuy/repos/hecke/magma/test/README-tests/test-04-division.mag` (whole file
is 1131 bytes; here is the shape, with the full header and boilerplate verbatim):

```magma
// test-04-division.mag
// Covers README section "Division Algorithms".

Z := Integers();
Q := Rationals();
AttachSpec("../../hecke.spec");
SetVerbose("Clifford", 0);
SetLMFDBRootFolder("../../");

// ... assertions exercising the README's Division Algorithms examples ...

print "test-04-division.mag: OK";
quit;
```

And the newer dialect, verbatim from `test-45-lorentz-cones.mag:1-20`:

```magma
// test-45-lorentz-cones.mag — README coverage for: Lorentz Cones: meet, subset, and emptiness
// Run from magma/test/README-tests/:  magma test-45-lorentz-cones.mag

Z := Integers(); Q := Rationals();
AttachSpec("../../hecke.spec");
SetLMFDBRootFolder("../../");
SetVerbose("Clifford", 0);

// --- cone(::HypPol): TorCon from halfspace equations, cached on P`cone ---
cl<[I]> := clifford_algebra(Q, [-1]);      // Gaussian order Z[i]
O    := get_maximal_orders(cl)[1];
FD   := fundamental_domain(O);             // 2 HypPol cells, 5 halfspaces each
assert #FD eq 2;
pol1 := FD[1];
pol2 := FD[2];
assert #halfspaces(pol1) eq 5;
```

### Graceful skip

The "skips gracefully when required `DATA/` files are absent" contract is implemented
per-file, by hand, with no shared helper. `test-12-database-query.mag:12-19`:

```magma
// Skip if psycopg2 is not installed.
check := Split(Pipe("python3 -c 'import psycopg2' 2>&1 || echo SKIP", ""), "\n");
check := [s : s in check | #s gt 0];
if #check gt 0 and check[1][1..Minimum(4, #check[1])] eq "SKIP" then
    printf "psycopg2 not available — skipping DB query tests\n";
    print "test-12-database-query.mag: OK (skipped)";
    quit;
end if;
```

Data-dependent skips print a `SKIP` marker mid-file and continue
(`test-02-orders.mag:102`: `printf "[02] SKIP order eq/in/star test (no 3.2_3 order data)\n";`).

### Exit-status caveat

Most files signal success only by **printing** `<file>: OK` — Magma exits 0 either way.
Only `test-hyppolt-cone-meet.mag` uses a real nonzero exit:

```magma
else
    print "test-hyppolt-cone-meet.mag: FAIL";
    quit 1;
end if;
```

So a runner that keys on exit code alone will **under-report failures** on 51 of 52
files; a runner must grep stdout for the `: OK` line. (An `assert` failure does abort
Magma with a nonzero status, so hard-assert failures are caught by exit code; soft
failures and hangs are not.)

---

## 4. Runner — how these are executed

**Measured finding: there is no runner in the repo.** There is no `Makefile`, no CI
workflow, and no shell script that iterates `README-tests/`. `find` over
`/Users/tdupuy/repos/hecke` at depth 3 for `Makefile`/`*.yml`/`*.yaml` returns exactly
one hit, `.beads/config.yaml` — unrelated. `grep` for a loop over `README-tests/*.mag`
across `*.sh`/`Makefile`/`*.yml`/`*.py` returns nothing.

Execution is **by hand, one file at a time, from the test directory** — this is the
documented invocation (`README.md:3338`, and the `Run from …` header line in 34 of the
52 files):

```bash
cd magma/test/README-tests
magma test-45-lorentz-cones.mag
```

The suite *has* been run in bulk — `scratch/readme-tests-report-f55dfc7c.md` is a
full 50-file run report (2026-07-18, Magma V2.29-2, 300 s timeout per test,
49 PASS / 1 FAIL-HANG). Its header records:

```
**Test directory**: magma/test/README-tests/ (CWD per AttachSpec convention)
**Timeout**: 300s per test
```

But **the harness that produced it was not committed** — only the report is in the
repo. The bulk run appears to have been a gascity-dispatched worktree job
(the report's `**Repository**` line points at
`~/gt/hecke/he-vhk56-prepare-item-worktree/worktrees/he-0mlyk`).

**Consequence for the port: there is no runner to copy. One must be written.**

---

## 5. The two policies, one sentence each

**`/Users/tdupuy/repos/agent-skills/docs/policies/improve-readme-merge-gate.md`**
— *(status line 3: **"Draft — awaiting …"**, not yet in force)* — requires that any PR
to a Magma/Sage repo that introduces or substantively changes a mathematical feature
must, before merging to the protected branch, have run the `improve-README` skill and
produced passing `README-tests/` artifacts covering each new/changed README section,
with the invocation recorded on the work bead (§P2's four checks: skill ran, non-trivial
README diff, per-section test artifacts exist, artifacts pass).

**`/Users/tdupuy/repos/agent-skills/docs/brief-bundle/policies/improve-readme-every-iteration.md`**
(hecke bead `he-04y8`, charter, P1 OPEN) — requires that **every** meaningful work
checkpoint (skill FP round, bead close, brief landing, experiment sub-task close)
invoke `improve-README` on *some* appropriate README as a **light 1–3 sentence touch**,
not batched and not a rewrite, with the escape hatch that an iteration where no README
change would add information is satisfied by bead notes instead (§2, §4, §6).

### Two things the merge-gate policy already says about magma-diff-alg

It is **already listed as in-scope**, and its per-repo row is **already written and
already stale**. `improve-readme-merge-gate.md:76`:

```markdown
| `magma-diff-alg` | `README.md` | `magma/test/README-tests/` (proposed) | Authoritative computational lab; results flow into `differential-valuations`. |
```

That proposed path `magma/test/README-tests/` **cannot be right** — magma-diff-alg has
no `magma/` directory (§6). The row must be corrected as part of the port.

And §P5 / the transition list gate the whole policy: it "does not turn on for any repo"
until `improve-README` has passed a coordinate-review fixed point, and turn-on for a
repo additionally requires (`:154`) that "each eligible repo's `CLAUDE.md` records its
per-repo conventions row". magma-diff-alg has **no `CLAUDE.md`** (measured: `ls CLAUDE.md
AGENTS.md POLICY.md .gitignore` → all four absent).

---

## 6. Structural mismatches — what will NOT port cleanly

Measured against `/Users/tdupuy/repos/magma-diff-alg`.

### M1 — No `magma/` subdirectory. Packages sit at the repo root.

hecke: `magma/package-*.mag`, `magma/hecke.spec`, tests two levels down at
`magma/test/README-tests/` → `AttachSpec("../../hecke.spec")`.

magma-diff-alg: `package-*.mag` and `diffalg.spec` are **at the repo root**. A
`test/README-tests/` directory would be two levels down → `AttachSpec("../../diffalg.spec")`
by coincidence of depth, but `README-tests/` directly under the root would be one level
→ `../diffalg.spec`. The depth must be *chosen*, not copied. The policy's proposed
`magma/test/README-tests/` path is simply wrong for this repo.

### M2 — No `SetLMFDBRootFolder` analogue; no `DATA/` tree.

49 of 52 hecke tests call `SetLMFDBRootFolder("../../")`, and the "skip gracefully when
`DATA/` is absent" contract exists entirely because hecke tests read generated data.
magma-diff-alg has **no `DATA/` directory and no root-folder intrinsic** —
`grep SetLMFDBRootFolder` over the repo returns nothing. Two-thirds of hecke's
boilerplate has no counterpart and should be dropped rather than translated.

### M3 — Existing magma-diff-alg tests use ABSOLUTE AttachSpec paths.

`test-valuations/test_initial_ideal_intrinsic.mag:23`:

```magma
SetQuitOnError(true);
AttachSpec("/Users/tdupuy/repos/magma-diff-alg/diffalg.spec");
```

That is machine-specific and unportable, and it is the only `.mag`-file precedent in the
repo. Meanwhile the 20-odd notebooks use `AttachSpec("../diffalg.spec")`. Note the
existing `.mag` file **does** use `SetQuitOnError(true)` — which no hecke README-test
does, and which is strictly better for a runner (it makes exit codes trustworthy, fixing
hecke's §3 exit-status caveat). Keep it.

### M4 — Test-directory naming already diverges.

magma-diff-alg has **four** test directories — `test-homog/`, `test-jacobi/`,
`test-valuations/`, `test-weyl/` — organized by *topic*, not a single `test/` with
subdirs. Three of the four are **notebooks only** (`.ipynb`): `test-homog` 2 files,
`test-jacobi` 13 files, `test-weyl` 6 files. Only `test-valuations/` holds `.mag` files.
There is no `test/` directory to hang `README-tests/` under. Also: existing filenames use
**underscores** (`test_initial_ideal_intrinsic.mag`), the style hecke's `POLICY.md:145`
explicitly deprecates.

### M5 — README examples are STATEFUL and chained across sections.

This is the biggest content obstacle and it has no hecke analogue.
`README.md` §5 "Truncating to Polynomial Rings of Finite Order" (line 189) opens with:

```magma
f:=x^3+t*Diff(x,1)^3+t^2*Diff(x,2)^3;
```

— `x`, `t`, and `P` are never defined in that section; they come from §1 at line 58.
§6 "Leading Monomials…" (line 226) uses `f1`, defined at line 59 in §1.

Measured: 26 `### Example:` sections, but only 20 `PolynomialRingProlSeq(...)` setup
lines and only **6** `AttachSpec` lines in the whole 1172-line README (lines 50, 68, 411,
543, 928, 1059). So roughly 6 sections silently inherit state from a predecessor.
**"One self-contained test file per README section" cannot be applied mechanically** —
each chained section's test must replay its ancestor's setup, or sections must be grouped
into one test file (hecke already does this: `test-01` covers two sections, `test-10`
covers two).

### M6 — One README AttachSpec path is already wrong.

`README.md:928` (inside §23 "Homogeneous Differential Polynomials") reads
`AttachSpec("../diffalg.spec");` while every other example uses
`AttachSpec("diffalg.spec");` (root-relative). One of the two is wrong depending on the
stated CWD, and the README never states a CWD. A port must pick and document a CWD
convention first — hecke does this in its `CLAUDE.md` working-directory table, which
magma-diff-alg has no equivalent of.

### M7 — The Contents anchors are malformed.

`README.md:14-16`: `1. [Example: Instantiating Basic Objects](###example-instantiating-basic-objects)`
— three `#` inside the link target makes these dead anchors (should be
`#example-instantiating-basic-objects`), and entries 3+ drop the `#` entirely
(`(example-weyl-algebras)`). Entry 1 also reads "Instantiating" while the heading at
line 45 reads "Instatiating" (typo in the heading). A coverage table keyed on section
names will inherit these inconsistencies unless they are fixed first.

### M8 — No repo-doc surface to record the convention in.

hecke records the convention in four places: `README.md:3333/3347/3356`, `POLICY.md:136`
and `:153`, `CLAUDE.md` (working-directory table), and `README-data-generation.md:73`.
magma-diff-alg has **none** of these files. There is nowhere to write the convention
down, and `improve-readme-merge-gate.md:154` makes writing it down a precondition for
the gate turning on.

### M9 — Collaborator repo.

`improve-readme-merge-gate.md:110` flags magma-diff-alg specifically: *"Per-repo
conventions row above needs to be confirmed with collaborators (Sreejani, Shilpi, Andrew,
Antoine, DZB) before turning on."* This is a human gate, not an engineering one, and it
is unresolved. **[inferred]** — I read the policy text; I have not checked whether that
confirmation has since happened.

---

## 7. Port checklist for magma-diff-alg

Paths below are all relative to `/Users/tdupuy/repos/magma-diff-alg/`.
**Note LP1: `~/repos/*` is BART's lane — a `~/gt` agent hands this content to BART, it
does not `git add` any of it.**

1. **Decide and document the CWD convention.** Pick `test/README-tests/` (two levels
   down, mirroring hecke, → `AttachSpec("../../diffalg.spec")`) OR `README-tests/`
   (one level, → `AttachSpec("../diffalg.spec")`). Recommend **`test/README-tests/`**:
   it leaves room for the existing four topic dirs to migrate under `test/` later, and
   it keeps the hecke muscle memory. Write the choice into step 2 before any test file
   is authored.

2. **Create `CLAUDE.md`** at the repo root, containing at minimum:
   a Repository Layout block, a **working-directory table** in hecke's shape
   (`~/repos/hecke/CLAUDE.md` "Working directory rules — critical"), and the per-repo
   conventions row required by `improve-readme-merge-gate.md:154`
   (README location = `README.md`; test-artifact location = `test/README-tests/`).
   Without this file the merge gate cannot legally turn on for this repo.

3. **Create the directory `test/README-tests/`.**

4. **Fix `README.md` §Contents first** (M7): repair the 26 anchor targets
   (`(###example-…)` → `(#example-…)`, and add the missing `#` to entries 3–26), and
   fix the "Instatiating" heading typo at line 45. The coverage table in step 6 keys on
   these section names; fixing them after the table exists means editing both.

5. **Normalize `AttachSpec` in the README** (M6): make line 928 consistent with the
   other five, and add one sentence under `# Examples` stating the CWD every example
   assumes (repo root) — mirroring `README.md:3338` in hecke.

6. **Add a coverage table to `README.md`.** Append a section at the end, in hecke's exact
   shape (`README.md:3356`):

   ```markdown
   **README-tests coverage:**

   | File | README section |
   |------|----------------|
   | `test-01-basic-objects.mag` | Example: Instantiating Basic Objects |
   ```

   Seed it with all 26 rows up front, marking unwritten ones — an empty-but-complete
   table makes the drift in §2e visible immediately instead of after 40 files.

7. **Write the test files, `test-NN-<topic>.mag`, NN = 01…26** matching the Contents
   numbering exactly. Use the **newer** hecke header dialect plus `SetQuitOnError`:

   ```magma
   // test-05-truncating-to-jet-rings.mag — README coverage for: Truncating to Polynomial Rings of Finite Order
   // Run from test/README-tests/:  magma test-05-truncating-to-jet-rings.mag

   SetQuitOnError(true);
   AttachSpec("../../diffalg.spec");
   Z := Integers(); Q := RationalField();

   // --- setup replayed from §1 Instantiating Basic Objects (this section chains) ---
   R<t> := PolynomialRing(Q, 1);
   f := map<R->R | f :-> Derivative(f, t)>;
   A := DifferentialRing(R, f, Q);
   F<t> := FieldOfFractions(A);
   P<x,y> := PolynomialRingProlSeq(F, 2 : term_order := <"dblocks", [[1,2]]>);

   // --- <section example, verbatim from README, as hard asserts> ---
   ...
   assert ...;

   print "test-05-truncating-to-jet-rings.mag: OK";
   quit;
   ```

   Drop `SetLMFDBRootFolder` and `SetVerbose` entirely (M2 — no analogue).
   Keep `SetQuitOnError(true)` — it is already the local precedent (M3) and it fixes
   hecke's exit-status weakness (§3).

8. **Handle the ~6 chained sections explicitly** (M5). For each section whose example
   references a variable defined upstream, either (a) replay the §1 setup block with a
   `// --- setup replayed from §N ---` comment, as in step 7, or (b) merge it into the
   upstream section's test file and give that file a two-section table row, as hecke does
   for `test-01` and `test-10`. Do **not** leave a test that silently depends on
   interpreter state.

9. **Write the runner — it does not exist upstream and must be authored** (§4).
   `test/README-tests/run-all.sh`, executable, that: `cd`s to its own directory, loops
   `test-*.mag` in sorted order, runs each under `timeout 300 magma "$f"`, records
   elapsed time and exit code, **and greps stdout for the literal `<file>: OK`** (exit
   code alone is insufficient for any file not using `SetQuitOnError`), then prints a
   PASS/FAIL/HANG summary table and exits nonzero if any test failed. Model the output on
   `~/repos/hecke/scratch/readme-tests-report-f55dfc7c.md` — per-file table, summary
   counts, regression list, verdict line.

10. **Add a table-vs-disk consistency check to the runner** — the drift in §2e
    (2 phantom rows, 8 unlisted files in hecke) is the convention's measured failure mode
    and the only cheap defense is automation. Have `run-all.sh` parse the
    `**README-tests coverage:**` table out of `README.md`, diff it against `ls *.mag`,
    and fail loudly on either direction of mismatch.

11. **No `diffalg.spec` change is required.** Confirmed by reading
    `/Users/tdupuy/repos/magma-diff-alg/diffalg.spec` — it lists exactly the 10
    `package-*.mag` files and nothing else. Test files are *scripts*, not package
    members; hecke's `hecke.spec` likewise lists no test file. **Do not add
    `README-tests` entries to the spec.**

12. **Optionally adopt the sidecar `.md` convention** for tests with non-obvious pinned
    values, following `test-45-lorentz-cones.md`: `**Purpose:**`, `**Runtime:**`,
    `**What it covers:**`, `**Gotchas:**`, `**Cross-refs:**`. Only 7 of 52 hecke tests
    have one — it is a *deep-coverage* convention, not a per-file requirement. Skip it
    for the 26 straightforward section mirrors.

13. **Correct the stale policy row.** `improve-readme-merge-gate.md:76` says
    `magma/test/README-tests/ (proposed)` for magma-diff-alg, which is impossible in a
    repo with no `magma/` directory (M1). Hand the corrected row to BART along with
    everything else. This lives in `~/repos/agent-skills`, also BART's lane.

14. **Do not treat the gate as live.** `improve-readme-merge-gate.md:3` reads
    *"Status: Draft — awaiting …"* and §P5 blocks turn-on until `improve-README` passes a
    coordinate-review fixed point. Items 1–12 stand the convention up; turning the merge
    gate ON is a separate, currently-blocked decision that also needs the collaborator
    confirmation named at `:110` (M9).

---

## 8. Honest limits of this survey

- **I did not execute any Magma.** Every pass/fail claim about hecke's suite is quoted
  from `scratch/readme-tests-report-f55dfc7c.md` (dated 2026-07-18, commit `f55dfc7c`),
  not re-measured. That report is ~2 months stale and predates the `test-hyppolt-cone-action.mag`
  and `test-46-*` files (it lists 50 files; there are now 52).
- **Header-dialect counts (12 / 34 / 6) were measured by `grep -l` over the first 6 lines**
  of each file; a file mentioning the phrase later in the body would be miscounted. Spot
  checks on all 6 "neither" files confirmed they genuinely name no README section.
- **The "~6 chained sections" figure is derived**, not enumerated section by section:
  26 `### Example:` headings vs 20 `PolynomialRingProlSeq` setup lines. The exact list of
  chained sections needs a per-section read before step 8 is executed.
- **M9 (collaborator sign-off) is [inferred]** from the policy text alone; I did not
  check beads or mail for whether that confirmation has since landed.
