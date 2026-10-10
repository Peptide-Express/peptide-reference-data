# peptide-reference-data

*Maintained by Peptide.Express, a supplier of research peptides.*

Reference masses for common research peptides, plus a small script to compute them, so you can check the identity section of a certificate of analysis (CoA) without doing the arithmetic by hand.

A CoA's HPLC figure tells you how *pure* a sample is. The LC-MS line tells you *what* it is. This repo covers the second part: the theoretical mass to compare against, and the m/z values you'd expect to see for each charge state in electrospray.

## What's here

| Path | Contents |
| --- | --- |
| `data/peptides.csv` | 23 peptides: sequence, terminal modifications, disulfide count, source/reference, notes |
| `data/masses.csv` | Computed monoisotopic and average masses, and [M+H]⁺ … [M+5H]⁵⁺ m/z |
| `scripts/peptide_mass.py` | Standalone Python 3 calculator (no dependencies) |
| `docs/reading-the-identity-section.md` | How to compare a CoA mass result against these numbers |

## Quick use

```bash
python scripts/peptide_mass.py GEPPPGKPADDAGLV
# monoisotopic 1418.7042 Da | average 1419.54 Da
#   [M+2H]2+  m/z 710.3594 ...

python scripts/peptide_mass.py CYIQNCPLG --c-amide --disulfides 1   # oxytocin
python scripts/peptide_mass.py --csv data/peptides.csv              # rebuild masses.csv
```

Options: `--n-acetyl`, `--c-amide`, `--pyroglu` (N-terminal Q or E), `--disulfides N`.

## Why "TB-500" has two rows

The name is used for two different molecules: full-length thymosin β-4 (43 residues, N-acetylated, average mass ≈ 4,963 Da) and short fragments around the LKKTET motif, such as Ac-LKKTETQ (≈ 889 Da). Both can pass HPLC at 99 %. The mass is the only field on a CoA that tells them apart.

## Scope and limits

- **Standard residues only.** Peptides containing non-standard residues or lipidation (e.g. semaglutide, tirzepatide, retatrutide, ipamorelin, SS-31, tesamorelin) are deliberately left out rather than approximated. PRs with properly sourced structures are welcome.
- **Free peptide, neutral form.** Real lyophilized material usually carries counter-ions (TFA or acetate) and water. Those change the weighed mass, not the MS parent mass. See the doc for how that shows up as "net peptide content".
- **Sequences.** Natural peptides were checked against the cited UniProt entries. Synthetic sequences follow the originating literature. Report anything you find wrong via an issue; corrections get a changelog line.
- **Average masses** use IUPAC standard atomic weights. Expect ±0.01–0.05 Da differences from other calculators depending on the element table used.

## Background reading

A public set of real certificates to practise on is published by [Peptide.Express](https://peptide.express/lab-results), who maintain this repo.

## License

Data (`data/`, `docs/`): [CC BY 4.0](LICENSE-DATA). Code (`scripts/`): [MIT](LICENSE).

---

For laboratory research use only. Not for human or veterinary use. Nothing in this repository is dosing, clinical or medical information.
