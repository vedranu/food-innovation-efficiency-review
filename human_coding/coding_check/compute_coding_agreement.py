# -*- coding: utf-8 -*-
"""Agreement for the human check of design codes, adapted Maryland levels and extracted values.
Usage: python compute_coding_agreement.py provjera_kodiranja.xlsx"""
import sys
import pandas as pd


def kappa(a, b):
    a, b = list(a), list(b); n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return ((po - pe) / (1 - pe) if pe < 1 else 1.0), po


f = sys.argv[1] if len(sys.argv) > 1 else 'provjera_kodiranja.xlsx'
low = lambda d: d.rename(columns=lambda c: str(c).strip().lower())
K = low(pd.read_excel(f, 'Key'))
out = []
dA, dB = low(pd.read_excel(f, 'Dizajn_A')), low(pd.read_excel(f, 'Dizajn_B'))
kd = K[K.sheet == 'Dizajn'].reset_index(drop=True)
# studies excluded from the review after the check was distributed (questionable source) are left out of the agreement
EXCLUDED = {'2-s2.0-105042505619'}
keep = ~kd.id.isin(EXCLUDED)
kd, dA, dB = kd[keep].reset_index(drop=True), dA[keep].reset_index(drop=True), dB[keep].reset_index(drop=True)
out.append(f'Design sheet: {len(kd)} studies (excluded from the review afterwards: {int((~keep).sum())})')
nrm = lambda s: s.astype(str).str.strip().str.upper()
for lab, x, y in [('design A vs B', nrm(dA.design), nrm(dB.design)), ('design A vs LLM', nrm(dA.design), nrm(kd.llm_design)), ('design B vs LLM', nrm(dB.design), nrm(kd.llm_design))]:
    k, po = kappa(x, y); out.append(f'{lab}: agreement {100 * po:.1f} %, kappa {k:.3f}')
lev = lambda s: s.astype(str).str.extract(r'(\d)')[0]
both = lev(dA.maryland).notna() & lev(dB.maryland).notna()
for lab, x, y in [('Maryland A vs B', lev(dA.maryland), lev(dB.maryland)), ('Maryland A vs LLM', lev(dA.maryland), kd.llm_maryland.astype(str).str[0]), ('Maryland B vs LLM', lev(dB.maryland), kd.llm_maryland.astype(str).str[0])]:
    m = x.notna() & y.notna(); k, po = kappa(x[m], y[m])
    out.append(f'{lab} (n = {int(m.sum())}): exact agreement {100 * po:.1f} %, within one level {100 * ((x[m].astype(int) - y[m].astype(int)).abs() <= 1).mean():.1f} %, kappa {k:.3f}')
for c in 'AB':
    v = low(pd.read_excel(f, 'Vrijednosti_' + c))
    out.append(f'values coder {c}: metric correct {100 * (v.metric_correct == 1).mean():.1f} %, value correct {100 * (v.value_correct == 1).mean():.1f} % (n = {len(v)})')
vA, vB = low(pd.read_excel(f, 'Vrijednosti_A')), low(pd.read_excel(f, 'Vrijednosti_B'))
ok = (vA.metric_correct == 1) & (vA.value_correct == 1) & (vB.metric_correct == 1) & (vB.value_correct == 1)
out.append(f'values judged fully correct by both coders: {int(ok.sum())} of {len(vA)}')
open('coding_agreement_results.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n'); print('\n'.join(out))
