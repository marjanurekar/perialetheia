#!/usr/bin/env python3
"""
Perialetheia - CWIAL Report No. 1
Reproducibility script: regenerates the uncertainty budget and the headline
decision figure for belief displacement in European GM-food safety discourse.

Method: GUM (JCGM 100:2008) uncertainty budget with Type A and Type B
components combined in quadrature; detection decision after Currie (1968) /
ISO 11843-1. Terms follow VIM (JCGM 200:2012) and ISO/IEC 17025:2017.

No external data files are required: every input below is a declared value
drawn from the published Eurobarometer record and the report's Type B
assignments. Run:  python3 CWIAL-2026-01_reproduce.py

Report ID: PERIALETHEIA-CWIAL-2026-01
Status:    WORKING ANNEX - provisional Type B evaluation, under review.
           The published Report No. 1 states the anchor reading with Type A
           only; this script reproduces the working Type B budget.
"""
import math

# ----------------------------------------------------------------------
# 1. Anchor measurement
#    Proposition F (FALSE, Tier-1 verified by WHO / EFSA / NASEM):
#    "Consuming approved GM food is dangerous to human health."
#    Anchor wave: Eurobarometer 73.1 (2010), health-safety agreement item.
# ----------------------------------------------------------------------
D        = 0.59        # measured belief displacement (proportion agreeing with the false claim)
n        = 31238       # reported sample size
D_eff    = 1.8         # survey design effect (multi-stage face-to-face)

# ----------------------------------------------------------------------
# 2. Type A component  (statistical, from observed data)
# ----------------------------------------------------------------------
u_A = math.sqrt(D * (1 - D) / n) * math.sqrt(D_eff)

# ----------------------------------------------------------------------
# 3. Type B components  (evaluated from knowledge; GUM 4.3)
#    Each is a half-width or bound converted to a standard uncertainty by
#    the divisor for its assumed distribution.
# ----------------------------------------------------------------------
u_B1 = 0.010                       # response classification, bounded <= 0.01
u_B2 = 0.050                       # question-wording / instrument change (Normal, half-width 0.10, u = 0.050 as declared)
u_B3 = 0.017 / math.sqrt(3)        # translation / cross-country (Rectangular)
u_B4 = 0.026 / math.sqrt(3)        # temporal comparability (Rectangular)
u_B5 = 0.012 / math.sqrt(6)        # residual incl. coordinated campaign (Triangular)

components = {
    "u_A":  u_A,  "u_B1": u_B1, "u_B2": u_B2,
    "u_B3": u_B3, "u_B4": u_B4, "u_B5": u_B5,
}

# ----------------------------------------------------------------------
# 4. Combine (GUM 5.1, independent components -> quadrature)
# ----------------------------------------------------------------------
u_c = math.sqrt(sum(u**2 for u in components.values()))
k   = 2
U   = k * u_c

# ----------------------------------------------------------------------
# 5. Decision (is D distinguishable from zero at the stated coverage?)
# ----------------------------------------------------------------------
ratio = abs(D) / U
distinguishable = ratio > 1.0

# ----------------------------------------------------------------------
# 6. Report
# ----------------------------------------------------------------------
print(__doc__.strip().splitlines()[1])
print("-" * 64)
print(f"{'component':8} {'u_i':>10} {'variance share':>16}")
for name, u in components.items():
    print(f"{name:8} {u:10.4f} {100*u*u/(u_c*u_c):15.2f}%")
print("-" * 64)
print(f"Combined standard uncertainty  u_c = {u_c:.4f}")
print(f"Coverage factor                k   = {k}")
print(f"Expanded uncertainty           U   = {U:.4f}")
print(f"Belief displacement            D   = {D:+.2f}")
print(f"Decision ratio               |D|/U = {ratio:.2f}")
print(f"Distinguishable from zero          = {'YES' if distinguishable else 'no'}")
print("-" * 64)
print("Dominant term: u_B2 (undocumented change of survey instrument),")
print(f"contributing {100*u_B2*u_B2/(u_c*u_c):.0f}% of the combined variance.")
