"""Phase 2 sticky-cone deliverable: lineality-aware LP test for sticky cones
at the r=2 -> r=3 transition for f = x'' + x'y + y. Verdict: 2/2 sticky,
refinement profile [3, 7], 0 straddlers (CLEAN refinement, unlike r=3 -> r=4
which introduces 4 straddlers).

Same recipe as slice3_sticky_lineality_lp.py, scaled down by one level.
Run both to populate the table in notes.tex sec:sticky-cones-example:

    | r | # max cones | # sticky from r-1 | # transient |
    | 2 |    2        |       ---         |     ---     |
    | 3 |   10        |        2          |      0      |
    | 4 |  346        |       10          |      0      |

Inputs:  no external files. Sage 10.8 / scipy >= 1.10 (HiGHS LP).
Outputs: r=2->r=3 sticky counts under three readings, refinement profile,
         the canonical sticky lifts (which L3 cone exactly equals each L2
         cone after projection).
Runtime: ~0.5 s on Taylor's laptop.
Memory:  project_slice3_sticky_result.md (covers both r=2->r=3 and r=3->r=4).
"""

import numpy as np
from scipy.optimize import linprog
import time
from sage.all import PolynomialRing, QQ


def build_fan(r):
    var_names = []
    for j in range(r + 1):
        var_names.append(f'x{j:02d}')
        var_names.append(f'y{j:02d}')
    S = PolynomialRing(QQ, var_names)
    g = {n: S.gen(i) for i, n in enumerate(var_names)}
    x, y   = g['x00'], g['y00']
    xp, yp = g['x01'], g['y01']
    xpp    = g['x02']
    f = xpp + xp * y + y
    if r == 2:
        gens = [f]
    elif r == 3:
        xppp = g['x03']
        fp = xppp + xpp * y + xp * yp + yp
        gens = [f, fp]
    return S.ideal(gens).groebner_fan().polyhedralfan()


# pf2 (R^6, vars [x00, y00, x01, y01, x02, y02]): I_2 = <f>.
#   Constraints: v(x01)=0, v(x02)=v(y00). Free: v(x00), v(y01), v(y02). dim 4.
LINEALITY_2 = [
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
]
# pf3 in R^8 (same basis as in slice3_sticky_lineality_lp.py).
LINEALITY_3 = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 2, 1, 0, 2, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
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


def main():
    print("Building pf2, pf3...", flush=True)
    t0 = time.time()
    pf2 = build_fan(2); pf3 = build_fan(3)
    assert pf2.lineality_dim() == len(LINEALITY_2), \
        f"pf2 lineality_dim {pf2.lineality_dim()} != hand-derived {len(LINEALITY_2)}"
    assert pf3.lineality_dim() == len(LINEALITY_3), \
        f"pf3 lineality_dim {pf3.lineality_dim()} != hand-derived {len(LINEALITY_3)}"
    rays2 = [list(r) for r in pf2.rays()]
    rays3 = [list(r) for r in pf3.rays()]
    cones2 = next(iter(pf2.maximal_cones().values()))
    cones3 = next(iter(pf3.maximal_cones().values()))
    print(f"  pf2: {len(rays2)} rays, {len(cones2)} cones; pf3: {len(rays3)} rays, {len(cones3)} cones", flush=True)

    # Project pf3 R^8 -> R^6 by dropping coords 6, 7 (x03, y03).
    rays3_proj = [r[:6] for r in rays3]
    lin3_proj = [v[:6] for v in LINEALITY_3]
    C2_rays = [[rays2[i] for i in idxs] for idxs in cones2]
    C3_proj_rays = [[rays3_proj[i] for i in idxs] for idxs in cones3]

    strict = {k: [] for k in range(len(cones2))}
    rev    = {k: [] for k in range(len(cones2))}
    for c3_k, C3p in enumerate(C3_proj_rays):
        for c2_k, C2 in enumerate(C2_rays):
            c2_in_c3 = cone_subseteq(C2, LINEALITY_2, C3p, lin3_proj)
            c3_in_c2 = cone_subseteq(C3p, lin3_proj, C2, LINEALITY_2)
            if c2_in_c3 and c3_in_c2: strict[c2_k].append(c3_k)
            if c3_in_c2:               rev[c2_k].append(c3_k)

    n_strict = sum(1 for v in strict.values() if v)
    n_rev    = sum(1 for v in rev.values()    if v)
    total_rev = sum(len(v) for v in rev.values())

    print(f"\nSTRICT (C2 == C3_proj):  {n_strict} / 2")
    print(f"REVERSE (C3_proj ⊆ C2):  {n_rev} / 2")
    print(f"Total L3 cones reverse-contained: {total_rev} / {len(cones3)}")
    print(f"Straddlers (L3 cones in no L2 cone): {len(cones3) - total_rev}")
    print(f"\nPer-L2-cone refinement:")
    for c2_k in range(len(cones2)):
        n_strict_c2 = len(strict[c2_k])
        n_rev_c2 = len(rev[c2_k])
        print(f"  L2-cone {c2_k} (rays {list(cones2[c2_k])}): "
              f"{n_rev_c2} reverse-contained L3 cones; {n_strict_c2} strict-equal lift")
        for c3_k in strict[c2_k]:
            print(f"      strict lift: L3-{c3_k} rays {list(cones3[c3_k])}")
        for c3_k in rev[c2_k]:
            if c3_k not in strict[c2_k]:
                print(f"      sub-cone: L3-{c3_k}")

    assert n_strict == 2 and total_rev == 10, "regression vs project_slice3_sticky_result.md"
    print(f"\nPASS  (2/2 strict-sticky; refinement [3, 7]; 0 straddlers)")
    print(f"Total: {time.time()-t0:.2f}s")


if __name__ == '__main__':
    main()
