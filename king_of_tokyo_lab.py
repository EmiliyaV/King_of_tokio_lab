# King of Tokyo survival analysis (exact + 200-trial simulation)
# Reproducible script extracted from the notebook environment.
# Random seed = 2025

import math, random
from collections import Counter
import pandas as pd
import numpy as np

p_keep_target = 1 - (5/6)**3
p_keep_nontarget_face = (5/6)**3 / 5

pH_heartmax = p_keep_target
pC_heartmax = p_keep_nontarget_face

pC_clawmax = p_keep_target
pH_clawmax = p_keep_nontarget_face

def binom_pmf(k, n, p):
    from math import comb
    return comb(n, k) * (p**k) * ((1-p)**(n-k))

def multinom_pmf(h, c, pH, pC):
    n = 6
    o = n - h - c
    if o < 0: 
        return 0.0
    from math import factorial
    pO = 1 - pH - pC
    return math.factorial(n) / (math.factorial(h)*math.factorial(c)*math.factorial(o)) * (pH**h) * (pC**c) * (pO**o)

def exact_survival_probability():
    p_total = 0.0
    p_survive = 0.0
    for h1 in range(7):
        for c1 in range(7 - h1):
            p1 = multinom_pmf(h1, c1, pH_heartmax, pC_heartmax)
            if p1 == 0: continue
            p_total += p1
            L1 = min(10, 2 + h1)
            L2 = 5 - c1
            if c1 <= 1:
                psurv = 0.0
                for c2 in range(7):
                    w2 = binom_pmf(c2, 6, pC_clawmax)
                    if (L1 - c2) > 0:
                        psurv += w2
                p_survive += p1 * psurv
            else:
                if L2 <= 0:
                    psurv = 0.0
                    for c3 in range(7):
                        w3 = binom_pmf(c3, 6, pC_clawmax)
                        if (L1 - c3) > 0:
                            psurv += w3
                    p_survive += p1 * psurv
                else:
                    psurv = 0.0
                    for c2 in range(7):
                        w2 = binom_pmf(c2, 6, pC_heartmax)
                        L1_after_p2 = L1 - c2
                        if L1_after_p2 <= 0:
                            continue
                        if c2 >= 1 and L1_after_p2 <= 3:
                            psurv += w2
                        else:
                            sub = 0.0
                            for c3 in range(7):
                                w3 = binom_pmf(c3, 6, pC_clawmax)
                                if (L1_after_p2 - c3) > 0:
                                    sub += w3
                            psurv += w2 * sub
                    p_survive += p1 * psurv
    return max(0.0, min(1.0, p_survive)), p_total

def simulate_once(seed=None):
    faces = ["1","2","3","heart","energy","claw"]
    def roll_one_die_until_target_or_3(target):
        for attempt in range(3):
            face = random.choice(faces)
            if face == target:
                return face
        return face
    def roll_six_with_strategy(strategy_target):
        from collections import Counter
        dice = []
        for _ in range(6):
            dice.append(roll_one_die_until_target_or_3(strategy_target))
        return Counter(dice)

    L1, L2, L3 = 2, 5, 4
    cnt1 = roll_six_with_strategy("heart")
    H1, C1 = cnt1["heart"], cnt1["claw"]
    L1 = min(10, L1 + H1)
    L2 -= C1
    
    p1_in_tokyo, p2_in_tokyo = False, True
    p2_alive = L2 > 0
    
    if C1 >= 1 and p2_alive:
        if L2 <= 3:
            p2_in_tokyo = False
            p1_in_tokyo = True
    if not p2_alive:
        p2_in_tokyo = False
        if C1 >= 1:
            p1_in_tokyo = True
    
    if p2_alive:
        if p2_in_tokyo:
            cnt2 = roll_six_with_strategy("claw")
            C2 = cnt2["claw"]
            L1 -= C2; L3 -= C2
            if L1 <= 0: 
                return False
            return True
        else:
            cnt2 = roll_six_with_strategy("heart")
            C2 = cnt2["claw"]
            if p1_in_tokyo and C2 > 0:
                L1 -= C2
                if L1 <= 0: return False
                if L1 <= 3:
                    p1_in_tokyo = False
    # P3
    if p2_in_tokyo:
        return L1 > 0
    else:
        if p1_in_tokyo:
            cnt3 = roll_six_with_strategy("claw")
            C3 = cnt3["claw"]
            L1 -= C3
            return L1 > 0
        else:
            return L1 > 0

if __name__ == "__main__":
    random.seed(2025)
    p_exact, _ = exact_survival_probability()
    N = 200
    survivors = sum(simulate_once() for _ in range(N))
    print("Exact probability:", p_exact)
    print("Empirical frequency (200 trials):", survivors / N)
