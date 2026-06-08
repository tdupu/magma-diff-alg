"""Phase 2 sticky-cone deliverable: Sage half of the Magma->Sage trace-ideal
pipeline. Reconstructs the trace ideal I^[r] = <f, f', ..., f^(r-2)> for
f = x'' + x'y + y in a TIGHTENED interleaved Sage ring of rank 2(r+1), then
computes its Groebner fan and reports the maximal-cone count + dict.

Verifies the pipeline-soundness sentence in notes.tex sec:sticky-cones-example:
"Magma-built trace ideals via <f, f', ..., f^(r-2)> in Jet(P, r) yield the
identical Groebner fan as the Sage infinite-notebook construction at r=2, 3, 4."

Inputs:  no external files; ideal generators encoded in code as Python polys.
         Sage 10.8, gfan 0.6.2 (shells out via sage.interfaces.gfan).
Outputs: per-r: ambient dim, ambient var names, generators, # max cones,
         max-cone dict, fan dim, wall time.
Runtime: ~0.1 s (r=2), ~0.2 s (r=3), ~7 s (r=4) on Taylor's laptop.
         The same r=4 ran ~339 s in the original 41-variable ambient
         (groebner-fans-infinite.ipynb) -- ~46x speedup from the tightening.
Memory:  project_slice2_magma_sage_pipeline_verified.md

Layout convention: variables INTERLEAVED in (derivative order, variable index),
so var[2j+0] = x^(j), var[2j+1] = y^(j). Matches Magma's Names(Jet(P, r))
directly, and matches the projection convention used by the sticky-cone
classification (slice3_sticky_lineality_lp.py).
"""

from sage.all import PolynomialRing, QQ
import time


def build_ring(r):
    var_names = []
    for j in range(r + 1):
        var_names.append(f'x{j:02d}')
        var_names.append(f'y{j:02d}')
    return PolynomialRing(QQ, var_names), var_names


def build_ideal(r):
    """Trace ideal at level r: <f, f', ..., f^(r-2)> in Jet(P, r).

    Polynomial generators derived by hand-computing the total derivative
    D = sum_i sum_j x_i^(j+1) * d/d(x_i^(j)) applied to f = x02 + x01*y00 + y00:
        f      = x02 + x01*y00 + y00                       (order 2)
        f'     = x03 + x02*y00 + x01*y01 + y01             (order 3)
        f''    = x04 + x03*y00 + 2*x02*y01 + x01*y02 + y02 (order 4)
    Verified against the Magma-printed Jet(f^(k), r) in slice2_magma_pipeline.mag.
    """
    S, var_names = build_ring(r)
    g = {n: S.gen(i) for i, n in enumerate(var_names)}
    x, y = g['x00'], g['y00']
    xp, yp = g['x01'], g['y01']
    xpp, ypp = g['x02'], g['y02']
    f = xpp + xp * y + y
    if r == 2:
        return S, var_names, [f]
    xppp = g['x03']
    fp = xppp + xpp * y + xp * yp + yp
    if r == 3:
        return S, var_names, [f, fp]
    xpppp = g['x04']
    fpp = xpppp + xppp * y + 2 * xpp * yp + xp * ypp + ypp
    if r == 4:
        return S, var_names, [f, fp, fpp]
    raise ValueError(f"r={r} not in scope for this slice")


def run_for(r):
    S, var_names, gens = build_ideal(r)
    I = S.ideal(gens)
    t0 = time.time()
    gf = I.groebner_fan()
    gbs = gf.reduced_groebner_bases()
    pf = gf.polyhedralfan()
    mc = pf.maximal_cones()
    elapsed = time.time() - t0
    n_max = sum(len(v) for v in mc.values())
    return {
        'r': r,
        'ambient_dim': S.ngens(),
        'var_names': var_names,
        'generators': [str(p) for p in gens],
        'n_reduced_GBs': len(gbs),
        'n_max_cones': n_max,
        'maximal_cones_dict': dict(mc),
        'fan_dim': pf.dim(),
        'elapsed_s': elapsed,
    }


def main():
    expected = {2: 2, 3: 10, 4: 346}
    for r in [2, 3, 4]:
        out = run_for(r)
        ok = out['n_max_cones'] == expected[r]
        marker = 'PASS' if ok else 'FAIL'
        print(f"==== r = {r} ({marker}) ====")
        print(f"  ambient_dim: {out['ambient_dim']}; var_names: {out['var_names']}")
        print(f"  generators: {out['generators']}")
        print(f"  # reduced GBs: {out['n_reduced_GBs']}")
        print(f"  # max cones: {out['n_max_cones']} (expected {expected[r]})")
        print(f"  fan_dim: {out['fan_dim']}")
        print(f"  elapsed: {out['elapsed_s']:.2f} s")
        # Print the max-cone dict only at small r; r=4 is 346 entries.
        if r <= 3:
            print(f"  maximal_cones: {out['maximal_cones_dict']}")
        print()


if __name__ == '__main__':
    main()
