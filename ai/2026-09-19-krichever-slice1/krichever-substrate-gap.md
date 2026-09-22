# Krichever handbook H1–H3 vs. existing substrate — gap analysis

Date: 2026-09-20. Sources read-only; nothing in any repo was modified.

- Handbook: `/Users/tdupuy/repos/krich/ai/2026-09-19-krichever-magma-handbook/report.md`
  (H1 = L57, H2 = L98, H3 = L138, H4 = L163 — all `[measured]` via `grep -n '^### H'`).
- Code: `/Users/tdupuy/repos/magma-diff-alg/` — intrinsic counts re-derived with
  `grep -c '^intrinsic'`: `package-rngdiffpol.mag` 169, `package-prolongations.mag` 106,
  `package-weyl-algebra.mag` 52, `package-noncommutative.mag` 1. All four match the brief. `[measured]`
- Magma binary present at `/Applications/Magma/magma`, so every claim below about *native*
  Magma behaviour is `[measured]` by running a probe, not read off documentation.

## 0. The headline measurement: the slice-1 session runs on TWO declared types

I did not reason about the minimal type set — I built it and ran it.
Prototype: `slice1proto.mag` + `slice1run.mag` in this scratchpad directory.
It declares exactly `declare type SetKric[ModKric];` and nothing else, and reproduces the
H2 hypothetical session verbatim:

```
Krichever module of rank 2 over ...Rational Field... , delta(x) = 1
  Coefficient algebra: Univariate Polynomial Ring in T over Rational Field,
  infinity pole degree of T = 1
  Action: T |-> D^2 + 1
  Source fixed: ...; isomorphisms are scalar gauges over ...
Type(M) = ModKric
Parent(M) = Krichever modules for Univariate Polynomial Ring in T over Rational Field
            in Differential operator ring over ...
Rank(M) = 2
Operator(M, T^2-T) = D^4 + D^2        <-- matches handbook L131 exactly
Apply(M, T, x^3) = x^3 + 6*x
ActionMap type = Map
```

`[measured]` **Answer to question 3: 2 declared types.** `SetKric` and `ModKric`.
Everything else in the H1 table is either (a) carried by a native Magma type already,
(b) expressible as a `Rec`, or (c) H4+ machinery.

## 1. The table

`slice-1` = the thinnest thing that works, per the brief: construct a rank-2 module over
Q(x) with `T |-> D^2+1`, print it, query its action, change base.

| item | H-section | substrate that exists | gap | slice-1 necessary? |
|---|---|---|---|---|
| `KricCoeff` | H1/H2 | native `RngUPol` (`PolynomialRing(C)`); `ConstantRing(R)` returns `Rational Field` `[measured]`; pole degree of `T` in `Q[T]` is `Degree` | pointed smooth completion, certified pole filtration, curve presentation | **NO** — prototype passed `A::RngUPol` straight into `SetKric` and printed the handbook's "pole degree of T = 1" line `[measured]` |
| `SetKric` | H1/H2 | NONE. No parent-category type in magma-diff-alg pairs a coefficient algebra with an operator ring. Nearest *pattern*: `AlgWeyl` decl `package-weyl-algebra.mag:36` + `UnderlyingRing` `:223` | whole type, 3 attributes (`cring`, `opring`, `iota`) | **YES** |
| `KricIdeal` | H1/H2 | NONE (`grep -i ideal` on the H2 surface: no `KricheverIdeal` analogue) | whole type + native-ideal adapter | **NO** — ideals are the H6 isogeny/quotient surface |
| `ModKric` | H1 | NONE | whole type, 3 attributes | **YES** |
| `PreModKric` | H1/H2 | NONE | candidate type + `Certify` | **NO** — handbook L135 itself: "The polynomial case is immediate from the positive order of its image". Prototype's whole certification is `require Order(L) gt 0` `[measured]` |
| `MapKric` | H1 | NONE | — | **NO** (H5) |
| `MapKricFrac` | H1 | NONE | — | **NO** (H5) |
| `SetKricHom` | H1 | NONE | — | **NO** (H5) |
| `AlgKricEnd` | H1 | NONE; `Centralizer`/`Commutator` grep = **0 hits** in all 10 `.mag` files `[measured]` | centralizer computation | **NO** (H7) |
| `AlgKricSpectral` | H1 | NONE; `Spectral` grep = **0 hits** `[measured]` | — | **NO** (H8) |
| `KricDatum`, `KricSheaf` | H1 | NONE; no `Curve`/`Place`/`FunctionField`/`Genus` intrinsic anywhere in the repo `[measured]` | — | **NO** (H11) |
| `KricTors`, `KricSol`, `KricLevel` | H1 | NONE | — | **NO** (H9) |
| `KricPV`, `KricRep`, `KricTateSystem` | H1 | NONE | — | **NO** (H10) |
| `KricFormal`, `KricWave`, `KricTau` | H1 | NONE | — | **NO** (H12) |
| `KricLocalModel`, `KricModuliSpec` | H1 | NONE | — | **NO** (H13) |
| `CrtKric`, `ResKric` | H1 | NONE as types; Magma `recformat`/`Rec` is native and the handbook (L55) already says "named `recformat` records" | certificate *content* is the real work, not the type | **NO as a declared type.** `BaseChange` returns one as its 3rd value, so slice 1 needs a *value* — a `Rec` with `{ok, checks_run, constants_enlarged}` suffices |
| `ModDiff` | H1 | NONE | left-module convention adapter | **NO** (H15 layering) |
| `DBKric` | H1 | NONE | — | **NO** (H14) |
| `GrpSch`, `Plc`, `Pt`, `PtJac` | H1 | NONE (adapter names, handbook L74 disclaims them) | — | **NO** (H8+) |
| `KricheverCoefficientRing(A::RngUPol)` | H2 | native `PolynomialRing` | wrapper only | **NO** — cut; pass `A` directly `[measured]` |
| `KricheverCoefficientRing(X, P)` curve | H2 | NONE in repo; native Magma `Crv`/`PlcCrvElt`/`FunctionField` exist outside it | pole filtration certificate | **NO** |
| `KricheverCoefficientRing(A, F)` record | H2 | NONE | filtration certificates | **NO** |
| `KricheverIdeal(S, gens)` | H2 | NONE | — | **NO** |
| `KricheverModules(S, R)` | H2 | NONE | ~8 lines | **YES** `[measured]` |
| `KricheverModule(H, images)` | H2 | NONE | ~15 lines incl. order-law check | **YES** `[measured]` |
| `KricheverModule(S,R,images)` | H2 | — | sugar over the above | **NO** |
| `KricheverModule(H, phi::Map)` | H2 | — | needs a map-domain check | **NO** |
| `KricheverModuleCandidate` / `Certify` | H2 | NONE | — | **NO** (see `PreModKric`) |
| `ValidationCertificate` / `Verify` | H2 | `Order(L::RngDiffOpElt)` native `[measured: Order(D^2+1)=2]`; `Order(L::AlgWeylElt)` `package-weyl-algebra.mag:920` | the *certificate object*; the *check* already exists | **NO as a type**; the check is 1 line and is slice-1 |
| `Parent(M)` | H3 | pattern: `Parent(x::AlgWeylElt)` `package-weyl-algebra.mag:748`; `Parent(x::RngMPolProlSeqElt)` `package-prolongations.mag:681` | trivial | **YES** |
| `BaseRing(M)` | H3 | **COLLISION — see §2.** | H3 as written is not implementable | **YES but must be renamed** |
| `CoefficientRing(M)` | H3 | `BaseRing(P::RngMPolProlSeq)` `package-prolongations.mag:596`; `BaseRing(Mats1::ModMatRng0)` `package-magma-fixes.mag:337` | trivial | **YES** |
| `CoefficientDatum(M)` | H3 | NONE | needs `KricCoeff` | **NO** (falls with `KricCoeff`) |
| `OperatorRing(M)` | H3 | `UnderlyingRing(WR::AlgWeyl)` `package-weyl-algebra.mag:223` is the exact analogue | trivial | **YES** |
| `ConstantEmbedding(M)` | H3 | native `Coercion(ConstantRing(R), BaseRing(R))` — `[measured]` returns `Mapping from: FldRat: C to RngDiff: K` | the *declared-vs-proved-exact* distinction in its certificate | **YES** (trivially; the certificate distinction is not) |
| `Rank(M)` | H3 | native `Order(RngDiffOpElt)` `[measured]`; `Order(L::AlgWeylElt)` `package-weyl-algebra.mag:920` | for `Q[T]` rank = `Order(image)`; general case needs pole degrees | **YES** |
| `DefiningOperators(M)` | H3 | stored attribute | trivial | **YES** |
| `ActionMap(M)` | H3 | native `map< A -> R \| f :-> ... >` `[measured: Type = Map]`. **NOT** `hom<>` — `hom< A -> R \| L >` fails with "Homomorphism has an invalid codomain" `[measured]` | none, once you know to use `map` not `hom` | **YES** |
| `Operator(M, a)` | H3 | **`Evaluate(f::RngUPolElt, L::RngDiffOpElt)` DOES NOT EXIST** — `[measured]` "Runtime error in 'Evaluate': Bad argument types / RngUPolElt[FldRat], RngDiffOpElt". Nearest existing thing: `Evaluate(f::AlgFrElt, seq::SeqEnum[AlgWeylElt])` `package-noncommutative.mag:2` — wrong source type (free algebra) and wrong target (`AlgWeyl`, not `RngDiffOp`) | ~8-line Horner loop | **YES** — and this is the one true missing primitive in H3 |
| `Apply(M, a, y)` | H3 | native `Apply(L, x^3)` and `L(x^3)` both return `x^3 + 6*x` `[measured]`; `'@'(L::AlgWeylElt, f::RngElt)` `package-weyl-algebra.mag:660` | none — pure composition of `Operator` + native `Apply` | **YES**, ~1 line |
| `BaseChange(M, iota)` | H3 | **NONE.** `BaseChange`/`ChangeDerivation` grep = **0 hits** across all 10 `.mag` files `[measured]` | verifying `iota*delta = delta'*iota` on an arbitrary map, + constants-enlargement detection | **YES** (the brief's slice-1 includes "change base") — **the biggest real gap** |
| `TransportCoefficientRing(M, alpha)` | H3 | NONE | needs pole-filtration compatibility, i.e. `KricCoeff` | **NO** — cut with `KricCoeff` |
| `ChangeDerivation(M, f)` | H3 | NONE | changes the ambient Ore ring; `D \|-> f^{-1}D'` with noncommutative re-expansion | **NO** — genuinely new machinery, defer to H4+ |

## 2. Defect found in H3 as written: `BaseRing` and `CoefficientRing` are the SAME intrinsic

`[measured]`, `probe5.mag` in this directory. Declaring only

```
intrinsic CoefficientRing(f::FooK) -> RngIntElt {} return 111; end intrinsic;
```

and then calling `BaseRing(f)` returns `111`. Magma treats the two names as synonyms on a
user type. In my first prototype run this silently made `BaseRing(M)` return the coefficient
ring (`Type = RngUPol`) instead of the differential ring, even though
`BaseRing(OperatorRing(M))` correctly returned `RngDiff` — a real, silent, wrong answer.

H3 (report.md L140–141) specifies `BaseRing(M) : ModKric -> RngDiff` **and**
`CoefficientRing(M) : ModKric -> Rng` as two accessors returning two different objects.
**That is not implementable in Magma.** One of them must be renamed
(`DifferentialBaseRing(M)` or `AmbientDifferentialRing(M)` for the `RngDiff`), or the two
must be merged. This is a design defect in the handbook, not an implementation gap.

## 3. Question 1 — does H1–H3 need noncommutative machinery beyond `package-weyl-algebra.mag`?

**No. Noncommutative machinery does not block slice 1.** `[measured]`

Slice 1 needs exactly four noncommutative operations, and all four are native to Magma's
`RngDiffOp`, with no package at all attached:

| need | native result `[measured]` |
|---|---|
| noncommutative product | `L*x = x*D^2 + 2*D + x`, `x*L = x*D^2 + x`, `L*x eq x*L` is `false` |
| powers | `(D^2+1)^2 = D^4 + 2*D^2 + 1` |
| order | `Order(D^2+1) = 2` |
| action on functions | `Apply(D^2+1, x^3) = x^3 + 6*x` |

`package-weyl-algebra.mag` reimplements all four on its own `AlgWeyl` type (`'*'` at :577 with
the explicit Leibniz `Binomial(n1,n1-k)*Diff(a2,n1-k)` twist, `'^'` at :702, `Order` at :920,
`'@'` at :660). I ran the same computation through `AlgWeyl` over the same `RngDiff` and got
identical answers (`1+ 2*d^2+ d^4`, `x^3 + 6*x`) `[measured]`. So `AlgWeyl` and `RngDiffOp`
are **two implementations of one thing** — that is a choice slice 1 must make consciously
(xkcd-927 risk), not a gap.

What `package-noncommutative.mag`'s single intrinsic actually does:
`Evaluate(f::AlgFrElt, seq::SeqEnum[AlgWeylElt])` evaluates a **free associative algebra**
element at a sequence of Weyl elements. That is the machinery for a source algebra with
**≥2 non-commuting generators**. Slice 1's source is `Q[T]` — one generator, commutative — so
it is not reached. It becomes relevant at H2's "generator images must … commute, satisfy all
source relations" only when `A` is a curve coordinate ring with ≥2 generators.

What is genuinely missing for **later** sections (named, so the plan can sequence it):
- `Centralizer` and `Commutator` on operators: **0 hits** in the repo `[measured]`. Blocks
  `AlgKricEnd` (H7) and `AlgKricSpectral` (H8).
- Ore division toward GCRD: the repo has `DivideStep` `:946` and `Divide` `:977` on `AlgWeyl`
  (the seed) but **no** `GCRD`/`LCLM` (**0 hits** `[measured]`). Native Magma `RngDiffOp`
  **does** have `GCRD` and `LCLM` `[measured]` — a further argument for building on `RngDiffOp`.
- No `Adjoint`, no `SymmetricPower` on `RngDiffOp` in the 2-argument form I probed
  (`no/2-arg-fail`; this is `UNKNOWN` as a claim about existence — the probe only shows the
  2-argument call failed. Settle it with `magma -b` running bare `Adjoint;` to print signatures).

## 4. Question 2 — do `RngDiff`/`RngDiffOp`/`WeylAlgebra` make some proposed types redundant?

- **`RngDiffOp` fully covers the operator ring.** `[measured]` The handbook is right to use it
  (H2 L119–121). No new operator type is needed, and `AlgWeyl` is a redundant second one.
- **`KricCoeff` is redundant for slice 1 — YES, cut it.** Native `RngUPol` carries `A` and its
  presentation; `ConstantRing(R)` gives the constant field (`Rational Field`) `[measured]`;
  "infinity pole degree of `T` = 1" is `Degree`. `KricCoeff` earns its existence only when `A`
  is a curve coordinate ring needing a pointed smooth completion + certified pole filtration,
  i.e. from H8/H11 down. Introducing it in slice 1 buys nothing and costs a type.
- **`SetKric` is NOT redundant.** Nothing native or in-repo pairs a coefficient algebra with
  an operator ring plus a constants embedding. `Parent(M)` in the handbook session prints
  exactly that pair, and there is no existing object to print. `[measured]` — the prototype
  had to declare it.
- **`ModKric` is NOT redundant.** A module here is an action, not an element set; no native
  Magma module type stores "a ring map into a noncommutative Ore ring".

## 5. Recommended slice 1 (aggressive cut)

Types: **2** — `SetKric`, `ModKric`. Plus one `recformat` for certificates (not a type).

Intrinsics (13, all measured working in the prototype):
`KricheverModules`, `KricheverModule`, `Print(SetKric)`, `Print(ModKric)`, `Parent`,
`Rank`, `ActionMap`, `Operator`, `Apply`, `CoefficientRing`, `OperatorRing`,
`ConstantEmbedding`, `DefiningOperators` — and `BaseChange`, which is the only one I did
**not** prototype and the only one with zero substrate.

Cut from slice 1: `KricCoeff`, `KricIdeal`, `PreModKric`, `Certify`, the curve and
record `KricheverCoefficientRing` overloads, `CoefficientDatum`,
`TransportCoefficientRing`, `ChangeDerivation`, and all 16 H4+ types.

Must be resolved before writing code: the `BaseRing`/`CoefficientRing` name collision (§2),
and whether the operator ring is `RngDiffOp` (recommended — native, has `GCRD`/`LCLM`) or the
repo's `AlgWeyl`.

## Honest limits of this analysis

- `BaseChange` was **not** prototyped. Its difficulty ("verifies `iota` commutes with
  derivations") is `[inferred]` from H3 L158 plus the measured absence of any substrate,
  not reproduced. Probe that would settle it: build two `RngDiff`s and a candidate map and
  try to check `sigma*delta = delta'*sigma` elementwise on generators.
- Whether native Magma has `Adjoint`/`SymmetricPower` on `RngDiffOp` at all is `UNKNOWN`
  (see §3); only the 2-argument call was measured to fail.
- I did not read H4–H15 beyond their headers, so "needed only for H4+" placements are
  `[inferred]` from the H1 table's own one-line meanings.
