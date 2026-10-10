# Reading the identity (mass) section of a peptide CoA

1. **Find which mass the lab reports.** Monoisotopic mass is typical for high-resolution instruments and small peptides. Deconvoluted *average* mass is common for larger peptides (> ~3 kDa), where the isotope envelope is wide. Compare like with like: `monoisotopic_da` or `average_da` in `data/masses.csv`.
2. **Charge states.** ESI rarely gives a clean [M+H]⁺ for anything over ~1.5 kDa. You'll usually see a ladder of [M+2H]²⁺, [M+3H]³⁺ and up. The `mz_*` columns list what to expect. For thymosin β-4, look near m/z 1241 (4+) and 993 (5+), not 4,961.
3. **Tolerance.** A match within a few hundredths of a dalton (or a few ppm on high-resolution data) is agreement. Differences of whole residues point to specific problems:
   - −57 / −71 / −87 Da … a missing Gly / Ala / Ser: a deletion sequence
   - +16 Da: oxidation (often Met)
   - +1 Da on Asn/Gln-containing peptides: deamidation (hard to see at low resolution)
   - +42 Da: unexpected acetylation; −42 Da: a missing expected acetyl
   - +114 Da (TFA adduct) or +22 Da (Na⁺ in place of H⁺) are usually adducts, not the peptide
4. **Disulfides.** A peptide with one intact disulfide is 2.016 Da lighter than the reduced form. If a CoA's oxytocin mass is ~1009 instead of ~1007, the sample may have been analysed reduced. That's worth a question, not necessarily a failure.
5. **Net peptide content is a different number.** A vial labelled 10 mg contains peptide *plus* counter-ions and residual water. Quantitation methods (amino acid analysis, or HPLC against a reference standard) report how much actual peptide is present. That figure can differ from the label fill in either direction and doesn't change the MS identity result.

For laboratory research use only. Not for human or veterinary use.
