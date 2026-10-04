# Technological innovation and economic efficiency in food processing and supply chains

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23145835.svg)](https://doi.org/10.5281/zenodo.23145835)

Replication package for the structured review *Technological innovation and economic efficiency in food processing and supply chains: a structured review of mechanisms and evidence strength* (manuscript submitted to *Agroekonomika*).

**Authors:** Ljiljana Nanjara, Vedran Uroš, Emilija Friganović, Damir Mihanović

The package contains the search strings, the screening and coding protocol, the screening log of all 4,503 screened records, the coded data set of the 309 included studies, the extracted effect values with their full-text status, the human validation of the screening and of the coding, and the MATLAB and Python scripts that produce every number, table and figure in the paper.

## Search and sample

- Search date: 3 October 2026, publication years 2015-2026.
- Main search: OpenAlex 1,310, Scopus 1,025 and Web of Science Core Collection 710 records.
- Supplementary search with efficiency-measurement terms: OpenAlex 2,056, Scopus 1,924 and Web of Science 1,526 records.
- 4,503 unique records screened; 309 studies included (205 from the main search, 104 from the supplementary search). Two studies were excluded at the full-text check, one for the outcome and one for the source.

## Contents

| Path | Content |
|---|---|
| `protocol/` | Search strings for all databases (main and supplementary search) and the screening and coding protocol |
| `data/screening_log.csv` | All screened records with search, stage, decision and reason |
| `data/included.csv` | Coded data set of the 309 included studies: technology, channels, design after the full-text check, design coded from the abstract, full-text status, adapted Maryland level, region, direction, effect statement, author countries, reference |
| `data/effects.csv` | Extracted effect values: value used, value from the abstract, full-text status (confirmed, corrected, not_found, not_accessed), scenario flag, source sentence, use in summary metrics |
| `data/prisma_counts.csv` | Counts for the PRISMA flow diagram, agreement statistics and full-text check |
| `data/excluded_not_indexed_countries.csv` | Records excluded by the indexing criterion, with author countries |
| `data/v1/` | Data of the first manuscript version (194 studies) |
| `matlab/analiza.m` | Main statistics (MATLAB R2023b): `results/*.csv`, `results/rezultati.txt` |
| `python/sensitivity.py` | Sensitivity analyses (grading rules, full-text verified values, scenario values, main search only), conditions, regional analysis: `results/sensitivity.txt`, `results/S_*.csv` |
| `python/figures.py` | Figures 1-3: `figures/*.png` (600 dpi) and `*.pdf` |
| `human_coding/` | Human validation of the LLM-assisted screening (pilot round, decision guide in Croatian, calibration set, validation sample, `compute_agreement.py` with the recall calculation) and the human check of design codes, Maryland levels and extracted values (`coding_check/`) |

## Reproduction

1. Run `matlab/analiza.m` in MATLAB (R2023b or later).
2. Run `python python/sensitivity.py` and `python python/figures.py` (Python 3.10+, see `requirements.txt`).
3. Run `python human_coding/round2/compute_agreement.py human_coding/round2/human_coding_sample_v2.xlsx` and `python human_coding/coding_check/compute_coding_agreement.py human_coding/coding_check/provjera_kodiranja.xlsx` from the respective folders to reproduce the validation statistics.

## Notes

- **Abstracts are not included.** Scopus and Web of Science licences do not allow redistribution of abstracts, so the abstract columns in the human-coding workbooks were removed. Records can be retrieved by their DOI or database ID. Short effect statements of one sentence are kept, because they document the extracted values.
- **Use of generative AI.** Screening, coding and value extraction were carried out by a large language model (Claude, Anthropic) under the written protocol in `protocol/`. Two authors validated the screening on a stratified sample of 100 records and checked the coding of 38 studies and 20 values without AI assistance (`human_coding/`).

## Licence

Data and documentation: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: MIT (see `LICENSE`).

## Citation

Nanjara, L., Uroš, V., Friganović, E., Mihanović, D. (2026). Replication package for: Technological innovation and economic efficiency in food processing and supply chains: a structured review of mechanisms and evidence strength (v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23145835

The concept DOI https://doi.org/10.5281/zenodo.23145834 always resolves to the latest version. Please also cite the paper once published.
