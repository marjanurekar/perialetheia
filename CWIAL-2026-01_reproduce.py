#!/usr/bin/env python3
"""
Perialetheia - CWIAL Report No. 1
Reproducibility script: regenerates the uncertainty budget and the capability
quantities for belief displacement in European GM-food safety discourse.

Method: GUM (JCGM 100:2008) uncertainty budget with Type A and Type B
components combined in quadrature; capability of detection after Currie (1968)
/ ISO 11843-1. Terms follow VIM (JCGM 200:2012) and ISO/IEC 17025:2017.

No external data files are required: every input below is a declared value
drawn from the published Eurobarometer record and the report's Type B
assignments. Run:  python3 CWIAL-2026-01_reproduce.py

Report ID: PERIALETHEIA-CWIAL-2026-01
Status:    Amended 2026-09-03. Three changes from the first release:
           (a) the item base is corrected to the split-ballot base;
           (b) Type B component names follow the programme taxonomy;
           (c) the decision against a zero-prevalence null is withdrawn and
               replaced by capability statements.
           See the amendment notes at the foot of this file.
"""
import math

# ----------------------------------------------------------------------
# 1. Anchor measurement
#    Proposition F (FALSE, Tier-1, VFRB id EU-GMFOOD-SAFETY):
#    "Consuming approved GM food is dangerous to human health."
#    Anchor wave: Eurobarometer 73.1 (2010), health-safety agreement item.
#
#    BASE. The item was administered on a SPLIT BALLOT. The item base is
#    15600, not the wave n. Using the wave n would understate the Type A
#    component by a factor of sqrt(2) and would misstate a property of the
#    instrument, whatever its effect on the combined uncertainty.
# ----------------------------------------------------------------------
D        = 0.59        # measured belief displacement (proportion agreeing with the false claim)
n        = 15600       # item base, split ballot (NOT the wave n)
D_eff    = 1.8         # survey design effect, multi-stage face-to-face;
                       # DECLARED, not derived from the design documentation

# ----------------------------------------------------------------------
# 2. Type A component  (statistical, from observed data)
# ----------------------------------------------------------------------
u_A = math.sqrt(D * (1 - D) / n) * math.sqrt(D_eff)

# ----------------------------------------------------------------------
# 3. Type B components  (evaluated from knowledge; GUM 4.3)
#    Names follow the programme taxonomy used across the CWIMF reports.
#    Each is a half-width or bound converted to a standard uncertainty by
#    the divisor for its assumed distribution.
#
#    u_B4 is not evaluated for this instrument. Eurobarometer 73.1 is a
#    multi-stage probability sample administered face to face, not an opt-in
#    panel, so the panel-skew term carries no value here. It is declared as
#    not applicable rather than assigned a number for symmetry.
#
#    u_B6 is an instrument-specific sixth component. Cross-national
#    translation has no counterpart in a single-country instrument and is
#    therefore not part of the five-term core taxonomy.
# ----------------------------------------------------------------------
u_B1 = 0.010                       # reference classification, Tier-1 bound <= 0.01
u_B2 = 0.050                       # instrument bias: question wording and list
                                   # context changed between waves and the change
                                   # is undocumented in the release
                                   # (Normal, half-width 0.10 at k = 2)
u_B3 = 0.026 / math.sqrt(3)        # temporal mismatch (Rectangular, half-width 0.026)
u_B4 = None                        # panel representativeness: not applicable
u_B5 = 0.012 / math.sqrt(6)        # adversarial adaptation, residual incl.
                                   # coordinated campaign (Triangular, half-width 0.012)
u_B6 = 0.017 / math.sqrt(3)        # translation and cross-country comparability
                                   # (Rectangular, half-width 0.017)

components = {
    "u_A":  u_A,  "u_B1": u_B1, "u_B2": u_B2,
    "u_B3": u_B3, "u_B5": u_B5, "u_B6": u_B6,
}

# ----------------------------------------------------------------------
# 4. Combine (GUM 5.1, independent components -> quadrature)
#    Input quantities are treated as uncorrelated and the covariance terms
#    of GUM eq. 13 are dropped explicitly.
# ----------------------------------------------------------------------
u_c = math.sqrt(sum(u**2 for u in components.values()))
k   = 2
U   = k * u_c

# ----------------------------------------------------------------------
# 5. Capability of the procedure
#    NOT a decision. For a verified-false proposition the null state is a
#    population holding the belief at zero prevalence. No such population
#    has been observed, so u_0 cannot be measured and is approximated by
#    u_c. That approximation is defensible here: displacement-independent
#    Type B terms carry over 99 per cent of the combined variance, which is
#    the condition under which u_0 ~ u_c holds.
# ----------------------------------------------------------------------
critical_value     = 1.645 * u_c
mdd                = 3.29  * u_c
response_threshold = 3.645 * u_c

# ----------------------------------------------------------------------
# 6. Report
# ----------------------------------------------------------------------
print(__doc__.strip().splitlines()[1])
print("-" * 64)
print(f"{'component':8} {'u_i':>10} {'variance share':>16}")
for name, u in components.items():
    print(f"{name:8} {u:10.4f} {100*u*u/(u_c*u_c):15.2f}%")
print(f"{'u_B4':8} {'n/a':>10} {'not applicable':>16}")
print("-" * 64)
print(f"Item base (split ballot)       n   = {n}")
print(f"Combined standard uncertainty  u_c = {u_c:.4f}")
print(f"Coverage factor                k   = {k}")
print(f"Expanded uncertainty           U   = {U:.4f}")
print(f"Belief displacement            D   = {D:+.2f}")
print("-" * 64)
print("CAPABILITY OF THE PROCEDURE (properties of the procedure at the null;")
print("no decision is issued against a zero-prevalence null):")
print(f"  critical value      1.645 u_c  = {critical_value:.4f}")
print(f"  min. detectable displ. 3.29 u_c = {mdd:.4f}   [Currie convention]")
print(f"  response threshold  3.645 u_c  = {response_threshold:.4f}")
print("-" * 64)
print("Dominant term: u_B2 (undocumented change of survey instrument),")
print(f"contributing {100*u_B2*u_B2/(u_c*u_c):.0f}% of the combined variance.")
print(f"Type A carries {100*u_A*u_A/(u_c*u_c):.2f}% of the combined variance.")
print()
print("Where a response decision is required it must be referred to a")
print("difference against a prior measurement of the same instrument on the")
print("same population, where a null of no change is attainable, or to an")
print("externally declared policy threshold.")

# ----------------------------------------------------------------------
# AMENDMENT NOTES (2026-09-03)
#
# (a) BASE. The first release used n = 31238, the wave n. The health-safety
#     item was administered on a split ballot and its base is 15600. The
#     correction raises u_A from 0.0037 to 0.0053 and u_c from 0.0544 to
#     0.0545. No reported conclusion changes.
#
#     That the combined uncertainty is insensitive to halving the base is
#     itself the finding. Type A carries under one per cent of the variance.
#     Survey precision is not what limits this measurement; the undocumented
#     instrument change is.
#
# (b) NAMING. The first release labelled the translation term u_B3 and the
#     temporal term u_B4, which reverses the programme taxonomy used in the
#     other reports and in cwial/simulate.py. No value changed. The
#     translation term is now u_B6 and is declared instrument-specific,
#     u_B3 is the temporal term, and u_B4 is declared not applicable.
#     u_B1 is stated as reference classification, its meaning across the
#     programme, rather than "response classification".
#
# (c) DECISION. The first release computed |D| / U and printed
#     "Distinguishable from zero = YES". Both moves are withdrawn. |D| / U
#     is not the distinguishability criterion, which is the critical value
#     at 1.645 u_c, and no decision may be issued against a null that cannot
#     be prepared. Capability quantities are reported in their place.
# ----------------------------------------------------------------------
