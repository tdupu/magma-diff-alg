# Krichever slice-1: substrate gap analysis, prototype, and probes

**Provenance.** These artifacts were produced by two research forks during math-city
Mayor session **QUIMBY 72** (2026-09-19/20) and left in that session's ephemeral
scratchpad. They were rescued on 2026-09-20 into `~/gt/mathcity-mayor/krichever-S72/`
— the Mayor's session-state directory, which is the wrong home for research output —
and relocated here by a fork of **QUIMBY 73** the same day, per Taylor's ruling:

> "All of the magma work for krichever modules should live in magma-diff-alg."

Relocation was copy → sha256-verify → remove-source; all files are byte-identical to
the rescued copies. Nothing was edited.

Directory name follows the live `<repo>/ai/<date>-<topic>/` convention, alongside
`~/repos/krich/ai/2026-09-19-krichever-magma-handbook` — the handbook these artifacts
analyze.

## These are INPUT to a plan, NOT the plan

**Plan 2 / the Krichever migration plan was never written.** Per Taylor, the CITY
writes that plan, not subagents. What is here is measured evidence for it: a gap
analysis, a working prototype, and probe results. Treat the "recommended slice 1"
section inside `krichever-substrate-gap.md` as an input proposal, not an approved plan.

## What each file is

| File | What it is |
|---|---|
| `krichever-substrate-gap.md` | Gap analysis of handbook sections H1–H3 against the existing `magma-diff-alg` substrate: a per-item table (substrate that exists / gap / needed for slice 1?), the `BaseRing` defect (below), the noncommutative-machinery question, and a recommended aggressive cut for slice 1. Ends with an explicit "honest limits" section. |
| `readme-tests-pattern.md` | Survey of hecke's `README` ↔ `README-tests/` mechanics (naming, linkage, boilerplate, runner, the two governing policies) and what will and will not port to `magma-diff-alg`; names 9 structural mismatches (M1–M9) and a 14-item port checklist. Not Krichever-specific, but produced in the same session for this repo's benefit. |
| `slice1proto.mag` | The slice-1 prototype package. Declares exactly two types (`declare type SetKric[ModKric];`) and 13 intrinsics. |
| `slice1spec.spec` | Magma spec attaching `slice1proto.mag`. |
| `slice1run.mag` | Driver that builds the handbook's H2 session and prints the accessors. Its `AttachSpec` still points at QUIMBY 72's scratchpad path — repoint it at `slice1spec.spec` here before re-running. |
| `probe1.mag` | Native-`RngDiffOp` probe: types, order, noncommutative product/powers, `BaseRing`/`ConstantField`, and whether `Evaluate(f::RngUPolElt, L::RngDiffOpElt)` exists (it does not). |
| `probe2.mag` | Probes `hom<A -> R \| L>` (fails: invalid codomain), hand-written Horner evaluation (works), `L(f)` and `Apply(L,f)` (both work), and `ConstantRing(R)`. |
| `probe3.mag` | Probes `map< A -> R \| f :-> ... >` as the working alternative to `hom<>`, and runs the same computation through `WeylAlgebra(K)` for comparison. |
| `probe4.mag` | Type-checks the prototype's accessors — the probe that exposed `BaseRing(M)` returning the wrong ring. |
| `probe5.mag` + `probe5.spec` | Minimal isolation of the `BaseRing`/`CoefficientRing` defect: a bare user type `FooK` declaring **only** `CoefficientRing`. |
| `probe5run.mag` | Runs `probe5`: calls `BaseRing(f)` on a type that never declared it. |
| `probe6.mag` | Probes whether `GCRD`, `LCLM`, `Adjoint`, `SymmetricPower` accept a 2-argument call on `RngDiffOp`. |

## The two load-bearing results

**1. `slice1proto.mag` reproduced the handbook's own session on two declared types.**
Running it gives `Rank(M) = 2` and `Operator(M, T^2-T) = D^4 + D^2` — the latter
matching the handbook's stated output exactly — plus `Apply(M, T, x^3) = x^3 + 6*x`.
This was built and run, not reasoned about. It reduces H1's roughly twenty proposed
types to **two**, `SetKric` and `ModKric` (plus one `recformat` for certificates, which
is a value, not a type). Everything else in the H1 table is either already carried by a
native Magma type, expressible as a `Rec`, or H4+ machinery.

**2. The probes PROVED H3 as written is not implementable.** Magma treats `BaseRing`
and `CoefficientRing` as the **same intrinsic** on a user type: `probe5.mag` declares
only `CoefficientRing(f::FooK)` returning `111`, and calling `BaseRing(f)` also returns
`111`. In the first prototype run this silently made `BaseRing(M)` return the
coefficient ring (`RngUPol`) instead of the differential ring — a real, silent, wrong
answer, caught by `probe4.mag`. H3 specifies `BaseRing(M) -> RngDiff` and
`CoefficientRing(M) -> Rng` as two accessors returning two different objects; that
cannot be done. One must be renamed or the two merged. This is a defect in the
handbook's design, not an implementation gap.

## Caveats carried from the source documents

- `BaseChange` — named in the analysis as the biggest real gap and the only recommended
  slice-1 intrinsic with zero substrate — was **not** prototyped. Its difficulty is
  `[inferred]`, not reproduced.
- Whether native Magma has `Adjoint`/`SymmetricPower` on `RngDiffOp` at all is
  `UNKNOWN`; `probe6.mag` only measured that the 2-argument call fails.
- `readme-tests-pattern.md` executed no Magma; its pass/fail claims about hecke's suite
  are quoted from a ~2-month-stale report and were not re-measured.

## Notes for whoever runs these

- `slice1run.mag` and `probe4.mag` carry `AttachSpec` paths from the original session
  (an absolute scratchpad path and a bare relative `slice1spec.spec`). Both specs are
  present in this directory; fix the paths rather than the specs.
- `probe3.mag` attaches `/Users/tdupuy/repos/magma-diff-alg/diffalg.spec`. Under LP1
  `~/repos` is read-only for `~/gt` agents; the equivalent spec here is
  `~/gt/magma_diff_alg/diffalg.spec`.
- `slice1spec.spec` and `probe5.spec` were rescued from QUIMBY 72's scratchpad by the
  QUIMBY 73 fork in addition to the files it was asked to relocate, because the
  prototypes are not runnable without them and the scratchpad is ephemeral. They are
  two lines each and trivially reconstructible; delete them if unwanted.
