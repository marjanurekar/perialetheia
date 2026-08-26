"""
PERIALETHEIA-CWIAL-2026-02 -- reproducibility annex
Belief Displacement in the Brexit GBP 350m Claim (Report No. 2)

Regenerates every figure in Report No. 2 from its declared inputs.
Pure Python 3.8+ standard library. No data files required.

    python CWIAL-2026-02_reproduce.py

Conventions follow JCGM 100:2008 (GUM) for the uncertainty budget and
Currie (1968) / ISO 11843-1 for capability of detection. Capability
figures are reported as properties of the procedure, not as a decision
against a zero-prevalence null: no population has ever held a verified-
false belief at zero prevalence, so that null cannot be prepared.
"""
import math

# ---------------------------------------------------------------- inputs
# Anchor wave: Policy Institute at King's College London / Ipsos MORI /
# UK in a Changing Europe, "Brexit Misperceptions", October 2018.
# Online, GB adults 18-75, n > 2,200. 67% report having heard the claim;
# 42% OF THOSE AWARE believe it true. Target population P is therefore
# the claim-aware subpopulation.
P_BELIEVE_2018 = 0.42
AWARE_2018 = 0.67
N_TOTAL_2018 = 2200
N_AWARE_2018 = round(N_TOTAL_2018 * AWARE_2018)   # derived, not published
D_EFF = 1.8            # DECLARED assumption for a quota-controlled online
                       # panel; not derived from the source study's design
                       # documentation and not a measured value.

# Comparison wave: Ipsos MORI Political Monitor, telephone, 11-14 June
# 2016, n = 1,257 GB adults 18+. Q19 screens awareness, Q20 asks belief.
# Published toplines are reported on ALL adults: 47% true, 39% false,
# 78% having heard the claim.
P_BELIEVE_2016_ALL = 0.47
AWARE_2016 = 0.78

# Type B components (Paper 3B Sec. 5). Each is a zero-expectation
# correction term in an additive model, so every sensitivity coefficient
# is unity. Input quantities are treated as uncorrelated and the
# covariance terms of GUM eq. 13 are dropped explicitly.
TYPE_B = {
    "u_B1_reference_classification":
        (0.030, "normal", "Tier-2 truth-classification risk; not the numeric range"),
    "u_B2_instrument_bias":
        (0.050, "normal", "Assumed framing shift, half-width 0.10 at k = 2"),
    "u_B3_temporal_mismatch":
        (0.026, "rectangular", "28 months campaign to measurement; +/-0.045 / sqrt(3)"),
    "u_B4_panel_representativeness":
        (0.035, "rectangular", "Opt-in panel skew; +/-0.061 / sqrt(3)"),
    "u_B5_adversarial_adaptation":
        (0.015, "triangular", "Residual claim reuse; +/-0.037 / sqrt(6)"),
}


# ------------------------------------------------------------- the budget
def type_a(p, n, d_eff):
    """Type A standard uncertainty on a survey proportion, D_eff corrected."""
    return math.sqrt(p * (1 - p) / n) * math.sqrt(d_eff)


def combine(u_a, type_b):
    """Combined standard uncertainty, quadrature sum over uncorrelated inputs."""
    return math.sqrt(u_a ** 2 + sum(v[0] ** 2 for v in type_b.values()))


# --------------------------------------------------- base harmonisation
def rebase_aware_to_all(p_aware, aware):
    """
    An 'among those aware' reading, expressed on an all-adult base.
    Respondents who had not heard the claim were not asked, so the
    fraction of them that would have endorsed it on presentation is
    unmeasured. Bounding it at 0 and at 1 gives the attainable interval.
    """
    lo = p_aware * aware
    return lo, lo + (1 - aware)


def rebase_all_to_aware(p_all, aware):
    """
    An all-adult reading, expressed on a claim-aware base. The split of
    believers between the aware and unaware groups is not published, so
    it is bounded.
    """
    lo = max(0.0, p_all - (1 - aware)) / aware
    hi = min(p_all, aware) / aware
    return lo, hi


def main():
    u_a = type_a(P_BELIEVE_2018, N_AWARE_2018, D_EFF)
    u_b_combined = math.sqrt(sum(v[0] ** 2 for v in TYPE_B.values()))
    u_c = combine(u_a, TYPE_B)
    bdi = P_BELIEVE_2018 - 0.0          # aligned prevalence p0 = 0, V(F) = FALSE

    print("=" * 66)
    print("PERIALETHEIA-CWIAL-2026-02  |  ANCHOR MEASUREMENT")
    print("=" * 66)
    print(f"  population        : GB adults 18-75 reporting awareness of F")
    print(f"  derived base n    : {N_AWARE_2018} (= {N_TOTAL_2018} x {AWARE_2018:.2f}, derived)")
    print(f"  belief prevalence : {P_BELIEVE_2018:.2f}")
    print(f"  BDI = p - p0      : {bdi:+.3f}")
    print()
    print(f"  Type A (D_eff = {D_EFF}) : {u_a:.4f}")
    for name, (val, dist, note) in TYPE_B.items():
        print(f"  {name:32s} : {val:.4f}  [{dist}] {note}")
    print(f"  {'Type B combined':32s} : {u_b_combined:.4f}")
    print(f"  {'Combined u_c':32s} : {u_c:.4f}")
    print(f"  {'Expanded U (k = 2)':32s} : {2 * u_c:.4f}")
    print()
    print("  CAPABILITY OF THE PROCEDURE (not a decision against a null)")
    print(f"  {'critical value 1.645 u_c':32s} : {1.645 * u_c:.4f}")
    print(f"  {'min. detectable displ. 3.29 u_c':32s} : {3.29 * u_c:.4f}")
    print(f"  {'response threshold 3.645 u_c':32s} : {3.645 * u_c:.4f}")
    print(f"  |BDI| / response threshold       : {abs(bdi) / (3.645 * u_c):.2f}")
    print()
    print("  No decision is issued against a zero-prevalence null. The null")
    print("  state is not physically realisable and u_0 cannot be measured.")

    print()
    print("=" * 66)
    print("PRINCIPAL FINDING  |  THE 2016-2018 COMPARISON DOES NOT CLOSE")
    print("=" * 66)
    a_lo, a_hi = rebase_aware_to_all(P_BELIEVE_2018, AWARE_2018)
    b_lo, b_hi = rebase_all_to_aware(P_BELIEVE_2016_ALL, AWARE_2016)
    print(f"  2016 reading (all adults, n = 1257, phone) : {P_BELIEVE_2016_ALL:.2f}")
    print(f"  2018 reading (claim-aware, online)         : {P_BELIEVE_2018:.2f}")
    print(f"  awareness moved {AWARE_2016:.2f} -> {AWARE_2018:.2f} "
          f"({100 * (AWARE_2018 - AWARE_2016):+.0f} pp)")
    print()
    print(f"  2018 rebased onto the all-adult base : "
          f"[{a_lo:.3f}, {a_hi:.3f}]  width {a_hi - a_lo:.3f}")
    print(f"    contains the 2016 reading {P_BELIEVE_2016_ALL:.2f} : "
          f"{a_lo <= P_BELIEVE_2016_ALL <= a_hi}")
    print(f"  2016 rebased onto the claim-aware base : "
          f"[{b_lo:.3f}, {b_hi:.3f}]  width {b_hi - b_lo:.3f}")
    print(f"    contains the 2018 reading {P_BELIEVE_2018:.2f} : "
          f"{b_lo <= P_BELIEVE_2018 <= b_hi}")
    print()
    print("  Each interval contains the other wave's reading. Neither")
    print("  stability nor change is established by the published record.")
    print("  The harmonisation term -- the endorsement rate among those")
    print("  not previously aware -- is the missing quantity. It was")
    print("  measurable in 2016, when belief was asked of all respondents,")
    print("  and is not reported in the 2018 release.")


if __name__ == "__main__":
    main()
