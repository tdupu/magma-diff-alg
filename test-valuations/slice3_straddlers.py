"""Phase 2 sticky-cone deliverable: identify the 4 level-4 cones that do NOT
reverse-contain into any single level-3 cone after projection (the "straddler"
cones in notes.tex sec:sticky-cones-example). Their projections cross
boundaries between adjacent level-3 cones.

Result on f = x'' + x'y + y at the r=3 -> r=4 transition:
    L4-43:  ray-indices [0, 2, 5, 10, 17, 18, 37]
    L4-64:  ray-indices [0, 2, 5, 10, 17, 30, 37]
    L4-65:  ray-indices [0, 2, 5, 10, 18, 30, 37]
    L4-223: ray-indices [2, 10, 18, 32, 38, 40, 44]
(L4-43/64/65 share a 5-ray core {0, 2, 5, 10, 37}; L4-223 is structurally
separate, sharing only {2, 10, 18} with the family.)

Inputs:  no external files. Sage 10.8 / scipy >= 1.10 (HiGHS LP).
Outputs: 4 straddler ray-index lists.
Runtime: ~7 s on Taylor's laptop (full pass through 346 L4 cones with the
         lineality-aware containment LP; early-exit per L4 cone).
Memory:  project_slice3_sticky_result.md (records the 4 indices as data).
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
    x, y = g['x00'], g['y00']
    xp, yp = g['x01'], g['y01']
    xpp, ypp = g['x02'], g['y02']
    f = xpp + xp * y + y
    if r == 3:
        xppp = g['x03']
        fp = xppp + xpp * y + xp * yp + yp
        gens = [f, fp]
    elif r == 4:
        xppp = g['x03']
        xpppp = g['x04']
        fp = xppp + xpp * y + xp * yp + yp
        fpp = xpppp + xppp * y + 2 * xpp * yp + xp * ypp + ypp
        gens = [f, fp, fpp]
    return S.ideal(gens).groebner_fan().polyhedralfan()


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
        cols.append(list(v)); cols.append([-c for c in v])
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
    print("Building pf3 and pf4...", flush=True)
    pf3 = build_fan(3); pf4 = build_fan(4)
    assert pf3.lineality_dim() == len(LINEALITY_3), \
        f"pf3 lineality_dim {pf3.lineality_dim()} != hand-derived {len(LINEALITY_3)}"
    assert pf4.lineality_dim() == len(LINEALITY_4), \
        f"pf4 lineality_dim {pf4.lineality_dim()} != hand-derived {len(LINEALITY_4)}"
    rays3 = [list(r) for r in pf3.rays()]
    rays4 = [list(r) for r in pf4.rays()]
    cones3 = next(iter(pf3.maximal_cones().values()))
    cones4 = next(iter(pf4.maximal_cones().values()))

    rays4_proj = [r[:8] for r in rays4]
    lin4_proj = [v[:8] for v in LINEALITY_4]
    C3_rays = [[rays3[i] for i in idxs] for idxs in cones3]
    C4_proj_rays = [[rays4_proj[i] for i in idxs] for idxs in cones4]

    print("Scanning 346 L4 cones for straddlers (no single L3 cone contains "
          "their projection)...", flush=True)
    t0 = time.time()
    straddlers = []
    for c4_k, C4p in enumerate(C4_proj_rays):
        if not any(cone_subseteq(C4p, lin4_proj, C3, LINEALITY_3)
                   for C3 in C3_rays):
            straddlers.append((c4_k, list(cones4[c4_k])))
    print(f"  scan: {time.time()-t0:.2f}s", flush=True)
    print(f"\n{len(straddlers)} straddler L4 cones found:")
    for c4_k, idxs in straddlers:
        print(f"  L4-{c4_k}: ray-indices = {idxs}")

    expected = {43, 64, 65, 223}
    found = {c[0] for c in straddlers}
    assert found == expected, f"regression vs project_slice3_sticky_result.md: {found} != {expected}"
    print(f"\nPASS  (straddler set = {{43, 64, 65, 223}})")


if __name__ == '__main__':
    main()
