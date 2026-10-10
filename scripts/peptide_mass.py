#!/usr/bin/env python3
"""Compute average and monoisotopic masses for linear peptides built from the
20 standard amino acids, with a few common terminal modifications and
disulfide bonds. Also prints [M+nH]n+ m/z values for ESI charge states.

Usage:
    python scripts/peptide_mass.py GEPPPGKPADDAGLV
    python scripts/peptide_mass.py CYIQNCPLG --c-amide --disulfides 1
    python scripts/peptide_mass.py --csv data/peptides.csv   # rebuild data/masses.csv

Masses are residue masses (i.e. amino acid minus H2O). Average masses use
IUPAC standard atomic weights; monoisotopic masses use the most abundant
isotope of each element. Values are for the neutral free peptide, not a salt.
"""
import argparse, csv, sys

# residue: (monoisotopic, average)
RESIDUE = {
    "G": (57.021464, 57.0513), "A": (71.037114, 71.0779), "S": (87.032028, 87.0773),
    "P": (97.052764, 97.1152), "V": (99.068414, 99.1311), "T": (101.047679, 101.1039),
    "C": (103.009185, 103.1429), "L": (113.084064, 113.1576), "I": (113.084064, 113.1576),
    "N": (114.042927, 114.1026), "D": (115.026943, 115.0874), "Q": (128.058578, 128.1292),
    "K": (128.094963, 128.1723), "E": (129.042593, 129.1140), "M": (131.040485, 131.1961),
    "H": (137.058912, 137.1393), "F": (147.068414, 147.1739), "R": (156.101111, 156.1857),
    "Y": (163.063329, 163.1733), "W": (186.079313, 186.2099),
}
WATER = (18.010565, 18.0153)
PROTON = 1.007276
MODS = {
    "n_acetyl": (42.010565, 42.0367),     # +C2H2O
    "c_amide": (-0.984016, -0.9848),      # OH -> NH2
    "n_pyroglu_from_q": (-17.026549, -17.0305),  # N-terminal Gln cyclised, -NH3
    "n_pyroglu_from_e": (-18.010565, -18.0153),  # N-terminal Glu cyclised, -H2O
    "disulfide": (-2.015650, -2.0159),    # per S-S bond, -2H
}

def mass(seq, n_acetyl=False, c_amide=False, pyroglu=False, disulfides=0):
    seq = seq.strip().upper()
    bad = set(seq) - set(RESIDUE)
    if bad:
        raise ValueError(f"non-standard residue(s): {''.join(sorted(bad))}")
    mono = sum(RESIDUE[a][0] for a in seq) + WATER[0]
    avg = sum(RESIDUE[a][1] for a in seq) + WATER[1]
    def add(key, n=1):
        nonlocal mono, avg
        mono += MODS[key][0] * n; avg += MODS[key][1] * n
    if n_acetyl: add("n_acetyl")
    if c_amide: add("c_amide")
    if pyroglu:
        if seq[0] == "Q": add("n_pyroglu_from_q")
        elif seq[0] == "E": add("n_pyroglu_from_e")
        else: raise ValueError("pyroglutamate needs N-terminal Q or E")
    if disulfides: add("disulfide", disulfides)
    return mono, avg

def mz(mono, z):
    return (mono + z * PROTON) / z

def truthy(v):
    return str(v).strip().lower() in ("1", "true", "yes", "y")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("sequence", nargs="?")
    p.add_argument("--n-acetyl", action="store_true")
    p.add_argument("--c-amide", action="store_true")
    p.add_argument("--pyroglu", action="store_true")
    p.add_argument("--disulfides", type=int, default=0)
    p.add_argument("--csv", help="input peptides.csv; writes data/masses.csv")
    a = p.parse_args()
    if a.csv:
        rows = list(csv.DictReader(open(a.csv, newline="")))
        out = open("data/masses.csv", "w", newline="")
        w = csv.writer(out)
        w.writerow(["name", "length", "monoisotopic_da", "average_da",
                    "mz_1plus", "mz_2plus", "mz_3plus", "mz_4plus", "mz_5plus"])
        for r in rows:
            m, v = mass(r["sequence"], truthy(r["n_acetyl"]), truthy(r["c_amide"]),
                        truthy(r["pyroglu"]), int(r["disulfides"] or 0))
            w.writerow([r["name"], len(r["sequence"]), f"{m:.4f}", f"{v:.2f}"] +
                       [f"{mz(m, z):.4f}" for z in range(1, 6)])
        out.close()
        print(f"wrote data/masses.csv ({len(rows)} rows)")
        return
    if not a.sequence:
        p.error("give a sequence or --csv")
    m, v = mass(a.sequence, a.n_acetyl, a.c_amide, a.pyroglu, a.disulfides)
    print(f"monoisotopic {m:.4f} Da | average {v:.2f} Da")
    for z in range(1, 6):
        print(f"  [M+{z}H]{z}+  m/z {mz(m, z):.4f}")

if __name__ == "__main__":
    main()
