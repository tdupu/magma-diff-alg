"""Phase-4 C3 deliverable (bead dv-644), Sage half: re-verify the Phase-3
sticky-cone classification with fans built from StableTrace-exported ideals
instead of the hand-coded raw prolongation chain.

Reads the generator files written by c3_stable_trace_export.mag
(c3_stable_trace_gens_r{2,3,4}.txt). Those generators are the reduced
Groebner-basis presentation coming out of StableTrace's EliminationIdeal
loop — a syntactically different generating set from the raw chain
{f, f', f''} used in slice3_*.py — so this run is a genuine end-to-end
check of the C1 tooling, not a rerun of the old scripts. The Magma half
already verified T_stable = I_raw as ideals, which is what forces the fans
(and hence every index-based comparison below) to agree.

Verifies, with the same lineality-aware LP methodology as
slice3_sticky_lineality_lp.py / slice3_r2_to_r3_sticky.py:
  r=2 -> r=3:  2/2 sticky (strict), refinement profile [3, 7], 0 straddlers,
               canonical lifts L3-0 (for L2-0) and L3-2 (for L2-1);
  r=3 -> r=4:  10/10 sticky (strict), 342/346 L4 cones reverse-contained,
               refinement profile [4, 7, 13, 32, 16, 19, 87, 20, 51, 93],
               strict lifts [0, 2, 22, 20, 42, 16, 102, 38, 89, 195],
               straddlers exactly {L4-43, L4-64, L4-65, L4-223};
and that the level-3 / level-4 maximal-cone dicts match the committed
Phase-3 reference artifacts slice3_r3_max_cones.txt / slice3_r4_max_cones.txt.

Inputs:  c3_stable_trace_gens_r{2,3,4}.txt (from the Magma half),
         slice3_r3_max_cones.txt, slice3_r4_max_cones.txt (Phase-3 reference).
Run:     sage test-valuations/c3_stable_trace_sticky.py   (any CWD; paths are
         resolved relative to this file). Sage 10.8 / scipy >= 1.10 (HiGHS).
Runtime: ~1-4 min, dominated by the 346 x 10 LP loop (machine-dependent).
Memory:  project_rawchain_tstable_same_fan.md (the Phase-3 finding this
         re-verifies), project_slice3_sticky_result.md (expected data),
         project_lineality_in_sticky_check.md (LP methodology).
"""

import ast
import os
import time

import numpy as np
from scipy.optimize import linprog
from sage.all import PolynomialRing, QQ
from sage.misc.sage_eval import sage_eval

HERE = os.path.dirname(os.path.abspath(__file__))


def load_gens(r):
    """Read the StableTrace generator strings exported by the Magma half."""
    path = os.path.join(HERE, f'c3_stable_trace_gens_r{r}.txt')
    gens = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith('#'):
                gens.append(line)
    return gens


def build_fan_from_stable_trace(r):
    """Groebner fan of the StableTrace ideal at level r, in the interleaved
    ring QQ[x00, y00, x01, y01, ..., x0r, y0r] (same layout as slice3_*.py)."""
    var_names = []
    for j in range(r + 1):
        var_names.append(f'x{j:02d}')
        var_names.append(f'y{j:02d}')
    S = PolynomialRing(QQ, var_names)
    g = {n: S.gen(i) for i, n in enumerate(var_names)}
    gens = [sage_eval(s, locals=g) for s in load_gens(r)]
    return S.ideal(gens).groebner_fan().polyhedralfan(), gens


def load_reference_cones(fname):
    """Parse the maximal_cones_dict line of a committed Phase-3 artifact."""
    with open(os.path.join(HERE, fname)) as fh:
        for line in fh:
            if line.startswith('maximal_cones_dict'):
                d = ast.literal_eval(line.split('=', 1)[1].strip())
                (cones,) = d.values()
                return cones
    raise RuntimeError(f'no maximal_cones_dict line in {fname}')


# Hand-derived lineality bases (same as slice3_r2_to_r3_sticky.py and
# slice3_sticky_lineality_lp.py; the ideals are equal so these carry over).
LINEALITY_2 = [
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
]
LINEALITY_3 = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 2, 1, 0, 2, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
]
LINEALITY_4 = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 2, 1, 3, 2, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]


def ray_in_cone_with_lineality(r, cone_rays, lineality_vecs):
    if len(cone_rays) == 0 and len(lineality_vecs) == 0:
        return all(c == 0 for c in r)
    cols = [list(v) for v in cone_rays]
    for v in lineality_vecs:
        cols.append(list(v))
        cols.append([-c for c in v])
    A_eq = np.array(cols, dtype=float).T
    b_eq = np.array(r, dtype=float)
    n_vars = A_eq.shape[1]
    res = linprog(np.zeros(n_vars), A_eq=A_eq, b_eq=b_eq,
                  bounds=[(0, None)] * n_vars, method='highs')
    return res.success and res.status == 0


def cone_subseteq(A_rays, A_lin, B_rays, B_lin):
    for r in A_rays:
        if not ray_in_cone_with_lineality(list(r), B_rays, B_lin):
            return False
    for v in A_lin:
        if not ray_in_cone_with_lineality(list(v), B_rays, B_lin):
            return False
        if not ray_in_cone_with_lineality([-c for c in v], B_rays, B_lin):
            return False
    return True


def classify(cones_lo_rays, lin_lo, cones_hi_proj_rays, lin_hi_proj):
    """For each (hi, lo) cone pair test both containment directions.
    Returns (strict, rev): strict[lo] = hi cones equal to lo after projection;
    rev[lo] = hi cones contained in lo after projection."""
    strict = {k: [] for k in range(len(cones_lo_rays))}
    rev = {k: [] for k in range(len(cones_lo_rays))}
    for hi_k, Chi in enumerate(cones_hi_proj_rays):
        for lo_k, Clo in enumerate(cones_lo_rays):
            lo_in_hi = cone_subseteq(Clo, lin_lo, Chi, lin_hi_proj)
            hi_in_lo = cone_subseteq(Chi, lin_hi_proj, Clo, lin_lo)
            if lo_in_hi and hi_in_lo:
                strict[lo_k].append(hi_k)
            if hi_in_lo:
                rev[lo_k].append(hi_k)
    return strict, rev


def main():
    t0 = time.time()
    print("Building fans from StableTrace generators...", flush=True)
    pf2, gens2 = build_fan_from_stable_trace(2)
    pf3, gens3 = build_fan_from_stable_trace(3)
    pf4, gens4 = build_fan_from_stable_trace(4)
    print(f"  gens per level: r2={len(gens2)}, r3={len(gens3)}, r4={len(gens4)}")
    for r, pf, lin in ((2, pf2, LINEALITY_2), (3, pf3, LINEALITY_3),
                       (4, pf4, LINEALITY_4)):
        assert pf.lineality_dim() == len(lin), \
            f"pf{r} lineality_dim {pf.lineality_dim()} != hand-derived {len(lin)}"
    rays2 = [list(r) for r in pf2.rays()]
    rays3 = [list(r) for r in pf3.rays()]
    rays4 = [list(r) for r in pf4.rays()]
    cones2 = next(iter(pf2.maximal_cones().values()))
    cones3 = next(iter(pf3.maximal_cones().values()))
    cones4 = next(iter(pf4.maximal_cones().values()))
    print(f"  pf2: {len(cones2)} cones; pf3: {len(cones3)} cones; "
          f"pf4: {len(cones4)} cones   (expected 2 / 10 / 346)", flush=True)
    assert (len(cones2), len(cones3), len(cones4)) == (2, 10, 346)

    # The StableTrace-built fans must reproduce the committed Phase-3
    # maximal-cone data exactly (gfan's polyhedralfan output is canonical,
    # and the Magma half proved the ideals are equal). This also pins the
    # cone indexing used by every assertion below.
    ref3 = load_reference_cones('slice3_r3_max_cones.txt')
    ref4 = load_reference_cones('slice3_r4_max_cones.txt')
    mine3 = [list(c) for c in cones3]
    mine4 = [list(c) for c in cones4]
    assert mine3 == ref3, "level-3 maximal cones differ from slice3_r3_max_cones.txt"
    assert mine4 == ref4, "level-4 maximal cones differ from slice3_r4_max_cones.txt"
    print("  level-3 and level-4 maximal-cone dicts match the Phase-3 "
          "reference artifacts  PASS", flush=True)

    # ---- r=2 -> r=3 (expect: 2/2 strict-sticky, profile [3, 7], 0 straddlers)
    print("\nr=2 -> r=3 classification...", flush=True)
    rays3_proj = [r[:6] for r in rays3]
    lin3_proj = [v[:6] for v in LINEALITY_3]
    C2 = [[rays2[i] for i in idxs] for idxs in cones2]
    C3p = [[rays3_proj[i] for i in idxs] for idxs in cones3]
    strict23, rev23 = classify(C2, LINEALITY_2, C3p, lin3_proj)

    n_strict23 = sum(1 for v in strict23.values() if v)
    total_rev23 = sum(len(v) for v in rev23.values())
    contained23 = {c3 for lst in rev23.values() for c3 in lst}
    straddlers23 = sorted(set(range(len(cones3))) - contained23)
    profile23 = [len(rev23[k]) for k in range(len(cones2))]
    lifts23 = [strict23[k] for k in range(len(cones2))]
    print(f"  STRICT (C2 == C3_proj): {n_strict23} / 2")
    print(f"  reverse-contained L3 cones: {total_rev23} / {len(cones3)}")
    print(f"  refinement profile: {profile23}")
    print(f"  strict lifts: {lifts23}")
    print(f"  straddlers: {straddlers23}")
    assert n_strict23 == 2, f"r2->r3 strict-sticky {n_strict23} != 2"
    assert total_rev23 == 10 and not straddlers23, "r2->r3 refinement not clean"
    assert profile23 == [3, 7], f"r2->r3 profile {profile23} != [3, 7]"
    # Canonical lifts per PHASE-4-PLAN A6: L3-0 for L2-0, L3-2 for L2-1.
    assert lifts23 == [[0], [2]], f"r2->r3 strict lifts {lifts23} != [[0], [2]]"
    print("  PASS", flush=True)

    # ---- r=3 -> r=4 (expect: 10/10 strict-sticky, 342/346 reverse-contained,
    #      straddlers {43, 64, 65, 223})
    print("\nr=3 -> r=4 classification (346 x 10 LP pairs)...", flush=True)
    t1 = time.time()
    rays4_proj = [r[:8] for r in rays4]
    lin4_proj = [v[:8] for v in LINEALITY_4]
    C3 = [[rays3[i] for i in idxs] for idxs in cones3]
    C4p = [[rays4_proj[i] for i in idxs] for idxs in cones4]
    strict34, rev34 = classify(C3, LINEALITY_3, C4p, lin4_proj)
    print(f"  LP loop: {time.time()-t1:.2f}s", flush=True)

    n_strict34 = sum(1 for v in strict34.values() if v)
    total_rev34 = sum(len(v) for v in rev34.values())
    contained34 = {c4 for lst in rev34.values() for c4 in lst}
    straddlers34 = sorted(set(range(len(cones4))) - contained34)
    profile34 = [len(rev34[k]) for k in range(len(cones3))]
    lifts34 = [strict34[k] for k in range(len(cones3))]
    print(f"  STRICT (C3 == C4_proj): {n_strict34} / 10")
    print(f"  reverse-contained L4 cones: {total_rev34} / {len(cones4)}")
    print(f"  refinement profile: {profile34}")
    print(f"  strict lifts: {lifts34}")
    print(f"  straddlers: {straddlers34}")
    assert n_strict34 == 10, f"r3->r4 strict-sticky {n_strict34} != 10"
    assert total_rev34 == 342, f"r3->r4 reverse-contained {total_rev34} != 342"
    # Expected data per slice3_sticky_classification.txt.
    expected_profile34 = [4, 7, 13, 32, 16, 19, 87, 20, 51, 93]
    expected_lifts34 = [[0], [2], [22], [20], [42], [16], [102], [38], [89], [195]]
    assert profile34 == expected_profile34, \
        f"r3->r4 profile {profile34} != {expected_profile34}"
    assert lifts34 == expected_lifts34, \
        f"r3->r4 strict lifts {lifts34} != {expected_lifts34}"
    assert straddlers34 == [43, 64, 65, 223], \
        f"straddlers {straddlers34} != [43, 64, 65, 223]"
    print("  PASS", flush=True)

    print(f"\nALL PASS — StableTrace-built ideals reproduce the Phase-3 "
          f"sticky classification:")
    print(f"  2/2 sticky at r=2->r=3 (profile [3, 7], 0 straddlers);")
    print(f"  10/10 sticky at r=3->r=4 (342/346 reverse-contained);")
    print(f"  straddlers = {{L4-43, L4-64, L4-65, L4-223}}.")
    print(f"Total: {time.time()-t0:.2f}s")


if __name__ == '__main__':
    main()
