# Lab Work No.1 — *Classical Definition of Probability* (King of Tokyo)

This repository contains the materials for a probability theory lab assignment based on the board game **King of Tokyo**.  
The task is to calculate and compare the **theoretical probability** of player 1 surviving until their next turn, and the **empirical frequency** of survival obtained via simulation.

---

## Overview

- **Topic:** Applying classical probability (addition/multiplication rules, binomial and multinomial distributions, law of total probability).  
- **Scenario:** Three players in *King of Tokyo* with fixed strategies:
  - Healing when outside Tokyo with ≤3 lives,
  - Attacking otherwise,
  - Exiting Tokyo when dropping to ≤3 lives.  
- **Goal:** Compute the exact probability of survival for Player 1 and validate it against simulation (200 trials).

---

## Contents

- `king_of_tokyo_lab.py` — Python script that:
  - Calculates the theoretical probability,
  - Runs 200 Monte Carlo simulations,
  - Produces comparison plots and trial logs.
- `report.pdf` — Full PDF report with formulas, proofs, and detailed explanation.  
- `trials_200.csv` — Simulation log (200 trials).  
- `compare_survival.png` — Plot comparing theory vs. empirical results.  
- `README.md` — This file.

---

## Results

- **Theoretical probability:** ~0.8271  
- **Empirical frequency (200 trials):** ~0.835  
- The results agree within the expected statistical error.

---

## How to Run

### Requirements
- Python 3.9+  
- Packages: `pandas`, `numpy`, `matplotlib`

Install with:
```bash
pip install pandas numpy matplotlib
