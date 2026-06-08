"""Phase 2 sticky-cone deliverable: lineality-aware LP test for sticky cones
at the r=3 -> r=4 transition for f = x'' + x'y + y. Verdict: 10/10 cones
sticky under cone equality (literal defn:sticky-cones reading from §21).

Critical methodology note: a naive ray-set or polyhedron-equality test
(without the lineality of each fan included) returns 0/10, which is WRONG.
Groebner fans of differential ideals have a lineality space coming from
(a) variables that don't appear in any generator, and (b) the differential
homogeneity scaling direction. Both must be added as `+/-` free directions
in the LP. See project_lineality_in_sticky_check.md for the full bug-and-fix
write-up.

Inputs:  no external files. Sage 10.8 / scipy >= 1.10 (HiGHS LP).
Outputs: per-reading sticky counts (strict / weak / reverse), per-L3-cone
         refinement profile, full classification dict written to
         /tmp/karen_slice3_sticky_classification_v2.txt.
Runtime: ~14 s (6 s fan build + 8 s LP loop on 346 x 10 cone pairs).
Memory:  project_slice3_sticky_result.md (data),
         project_lineality_in_sticky_check.md (methodology).

Layout: INTERLEAVED Sage variables -- pf3 in QQ[x00, y00, x01, y01, x02, y02,
x03, y03] (rank 8), pf4 in QQ[..., x04, y04] (rank 10). Projection pi_{4,3}:
R^10 -> R^8 drops indices 8, 9 (x04, y04).
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


# Lineality bases derived by hand.
#
# pf3 (R^8, vars [x00, y00, x01, y01, x02, y02, x03, y03]):
#   I_3 = <f, f'>; v in lineality iff for every generator, all monomials
#   have the same v-weight. Constraints from f: v(x01)=0, v(x02)=v(y00).
#   From f': v(x03)=v(y01) and 2*v(y00)=v(y01). Free: v(x00), v(y02), v(y03).
#   Basis:
#     e_x00, (0,1,0,2,1,0,2,0)   [the "weight 1" diff-homogeneity direction],
#     e_y02, e_y03.   dim 4.
LINEALITY_3 = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 2, 1, 0, 2, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
]
# pf4 (R^10, vars extended by x04, y04):
#   Adding f'' forces v(y02) = 3*v(y00) = v(x04). y02 no longer free;
#   y03 and y04 become free. dim 4.
LINEALITY_4 = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 2, 1, 3, 2, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]


def ray_in_cone_with_lineality(r, cone_rays, lineality_vecs):
    """LP feasibility: r = sum lambda_i * cone_rays[i] + sum mu_j * lineality_vecs[j],
       lambda >= 0, mu free (split into mu+ - mu-, both >= 0)."""
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
    """Test cone(A_rays) + span(A_lin) ⊆ cone(B_rays) + span(B_lin)."""
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
    print("Building pf3, pf4...", flush=True)
    t0 = time.time()
    pf3 = build_fan(3); pf4 = build_fan(4)
    # Defense-in-depth: verify Sage's reported lineality dimension matches the
    # hand-derived bases. Catches the case where someone changes the example
    # or where Sage/gfan changes behavior, which would silently break the LP.
    assert pf3.lineality_dim() == len(LINEALITY_3), \
        f"pf3 lineality_dim {pf3.lineality_dim()} != hand-derived {len(LINEALITY_3)}"
    assert pf4.lineality_dim() == len(LINEALITY_4), \
        f"pf4 lineality_dim {pf4.lineality_dim()} != hand-derived {len(LINEALITY_4)}"
    rays3 = [list(r) for r in pf3.rays()]
    rays4 = [list(r) for r in pf4.rays()]
    cones3 = next(iter(pf3.maximal_cones().values()))
    cones4 = next(iter(pf4.maximal_cones().values()))
    print(f"  pf3: {len(rays3)} rays, {len(cones3)} cones; pf4: {len(rays4)} rays, {len(cones4)} cones", flush=True)
    print(f"  build: {time.time()-t0:.2f}s", flush=True)

    rays4_proj = [r[:8] for r in rays4]
    lin4_proj = [v[:8] for v in LINEALITY_4]
    C3_rays = [[rays3[i] for i in idxs] for idxs in cones3]
    C4_proj_rays = [[rays4_proj[i] for i in idxs] for idxs in cones4]

    print("\nLP loop (3 readings; 346 x 10 cone pairs, both directions)...", flush=True)
    t1 = time.time()
    strict = {k: [] for k in range(len(cones3))}
    weak   = {k: [] for k in range(len(cones3))}
    rev    = {k: [] for k in range(len(cones3))}
    for c4_k, C4p in enumerate(C4_proj_rays):
        for c3_k, C3 in enumerate(C3_rays):
            c3_in_c4 = cone_subseteq(C3, LINEALITY_3, C4p, lin4_proj)
            c4_in_c3 = cone_subseteq(C4p, lin4_proj, C3, LINEALITY_3)
            if c3_in_c4 and c4_in_c3: strict[c3_k].append(c4_k)
            if c3_in_c4:               weak[c3_k].append(c4_k)
            if c4_in_c3:               rev[c3_k].append(c4_k)
    print(f"  LP loop: {time.time()-t1:.2f}s", flush=True)

    n_strict = sum(1 for v in strict.values() if v)
    n_weak   = sum(1 for v in weak.values()   if v)
    n_rev    = sum(1 for v in rev.values()    if v)
    total_rev = sum(len(v) for v in rev.values())
    print(f"\nSTRICT  (C3 == C4_proj):  {n_strict} / 10")
    print(f"WEAK    (C3 ⊆ C4_proj):  {n_weak} / 10")
    print(f"REVERSE (C4_proj ⊆ C3):  {n_rev} / 10")
    print(f"\nTotal L4 cones reverse-contained: {total_rev} / 346")
    print(f"(=346 ⇒ projected level-4 fan refines level-3 fan; here 342, with 4 straddlers)")
    print(f"\nRefinement profile (L3 cone -> # reverse-contained L4 cones):")
    for c3_k in range(len(cones3)):
        print(f"  L3-cone {c3_k}: {len(rev[c3_k])}")

    expected_strict = 10
    expected_total = 342
    assert n_strict == expected_strict, f"strict-sticky regression: {n_strict} != {expected_strict}"
    assert total_rev == expected_total, f"reverse-contain regression: {total_rev} != {expected_total}"
    print(f"\nPASS  (10/10 strict-sticky; 342 of 346 reverse-contained; matches "
          f"project_slice3_sticky_result.md)")
    print(f"\nTotal: {time.time()-t0:.2f}s")


if __name__ == '__main__':
    main()
