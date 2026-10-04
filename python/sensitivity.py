# -*- coding: utf-8 -*-
"""Sensitivity and supplementary analyses for the revised manuscript (v2).
Input : data/included.csv, data/effects.csv, data/screening_log.csv, data/prisma_counts.csv, data/excluded_not_indexed_countries.csv (optional)
Output: results/sensitivity.txt and results/S_*.csv
Quantiles follow MATLAB's default definition (numpy method 'hazen'), as in matlab/analiza.m."""
import os, re, collections
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'results'); os.makedirs(RES, exist_ok=True)
D = pd.read_csv(os.path.join(ROOT, 'data', 'included.csv'), dtype=str).fillna('')
E = pd.read_csv(os.path.join(ROOT, 'data', 'effects.csv'), dtype=str).fillna('')
E['value'] = E['value'].astype(float); E['use'] = E['use_in_summary'].astype(int)
D['quant'] = D['quant'].astype(int)
P = pd.read_csv(os.path.join(ROOT, 'data', 'prisma_counts.csv')).set_index('step')['n']
lines = []
out = lines.append

T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7']
Tn = ['Automation and robotics', 'AI, sensors and IoT analytics', 'Digital twins and simulation', 'Blockchain and digital traceability',
      'Firm-level digital transformation', 'Advanced processing', 'Circular valorisation']
Pc = ['P1', 'P2', 'P3', 'P4', 'P5']
Pn = ['Productivity', 'Quality and safety', 'Resource efficiency', 'Supply-chain coordination', 'Revenue and financial performance']
OBS = {'E', 'C'}


def q(v, p):
    return float(np.quantile(np.asarray(v, float), p, method='hazen'))


def r1(x):
    # printf-style rounding of the binary value, identical to MATLAB's fprintf('%.1f')
    return float(f'{float(x):.1f}')


def grade(sub, obs_set):
    n = len(sub)
    obs = sub[sub.design.isin(obs_set)] if obs_set is not None else sub.iloc[0:0]
    no = len(obs); noq = int((obs.quant == 1).sum())
    nmq = int(((sub.design == 'TEA') & (sub.quant == 1)).sum()); pos = int((sub.direction == '+').sum())
    if n >= 5 and no >= 3 and noq >= 2 and pos / n >= 0.8: return 'Strong'
    if n >= 5 and (noq >= 1 or nmq >= 3): return 'Moderate'
    if n >= 3: return 'Limited'
    if n >= 1: return 'Insufficient'
    return 'None'


def evidence_map(Dx, obs_rule):
    rows = []
    for t, tn in zip(T, Tn):
        for p, pn in zip(Pc, Pn):
            s = Dx[(Dx.tech == t) & Dx.channels.str.contains(p)]
            if obs_rule == 'E_only': o = s[s.design == 'E']
            elif obs_rule == 'sms2': o = s[s.design.isin(OBS) & (s.sms.isin(['2', '3', '4', '5']))]
            else: o = s[s.design.isin(OBS)]
            s2 = s.copy(); s2['design'] = np.where(s.index.isin(o.index), 'OBS', np.where(s.design.isin(OBS), 'C_downgraded', s.design))
            rows.append(dict(technology=tn, channel=pn, n=len(s), grade=grade(s2, {'OBS'})))
    return pd.DataFrame(rows)


out(f'N = {len(D)} included studies (main search {int((D.search == "main").sum())}, supplementary search {int((D.search == "supplementary").sum())})')
dg = {'observed': D.design.isin(OBS), 'modelled': D.design == 'TEA', 'perceived': D.design == 'S', 'secondary': D.design.isin(['R', 'X'])}
out('Designs (after full-text check): ' + '; '.join(f'{k} {int(v.sum())} ({100 * v.mean():.1f} %)' for k, v in dg.items()))
out(f'Design changed after full-text check: {int((D.design != D.design_abstract).sum())} studies: ' + ', '.join(f'{a}->{b}' for a, b in zip(D.design_abstract[D.design != D.design_abstract], D.design[D.design != D.design_abstract])))
fts = D[D.ft_checked != '']
out(f'Full-text check: sought {len(fts)}, accessed {int((fts.ft_checked == "1").sum())}')
ob = D[D.design.isin(OBS)]
out(f'Observed studies: {len(ob)} (E {int((ob.design == "E").sum())}, C {int((ob.design == "C").sum())}); with SMS level: ' +
    ', '.join(f'level {k}: {v}' for k, v in sorted(collections.Counter(ob.sms).items())))
out('')

# technology counts and design per technology
out('TECHNOLOGY: n (%) [observed modelled perceived secondary] | main search n')
for t, tn in zip(T + ['T8'], Tn + ['Other (R&D and product innovation)']):
    s = D[D.tech == t]
    out(f'  {tn:40s} {len(s):3d} ({100 * len(s) / len(D):4.1f} %) [{int(s.design.isin(OBS).sum())} {int((s.design == "TEA").sum())} {int((s.design == "S").sum())} {int(s.design.isin(["R", "X"]).sum())}] | main {int((s.search == "main").sum())}')
out('')

# evidence grading under alternative rules
maps = {}
for rule, Dx, lab in [('EC', D, 'Main rule (observed = econometric or case study)'), ('E_only', D, 'Observed = econometric only'),
                      ('sms2', D, 'Observed = E/C with full-text SMS level >= 2'), ('EC', D[D.search == 'main'], 'Main search only (v1 corpus)')]:
    m = evidence_map(Dx, rule); maps[lab] = m
    st = m[m.grade == 'Strong']; mo = m[m.grade == 'Moderate']
    out(f'{lab}: Strong {len(st)} [' + '; '.join(f'{a} x {b} (n={n})' for a, b, n in zip(st.technology, st.channel, st.n)) + f'], Moderate {len(mo)}, Limited {int((m.grade == "Limited").sum())}')
big = maps['Main rule (observed = econometric or case study)'].copy()
for lab, m in maps.items(): big[lab] = m.grade.values
big.to_csv(os.path.join(RES, 'S_evidence_grades.csv'), index=False)
out('')

# effect sizes
M = ['energy_utility_reduction_pct', 'cost_reduction_pct', 'waste_loss_reduction_pct', 'time_reduction_pct', 'throughput_productivity_increase_pct',
     'yield_recovery_increase_pct', 'profit_revenue_increase_pct', 'roi_pct', 'irr_pct', 'payback_years']
Mn = ['Energy/utility use reduction (%)', 'Cost reduction (%)', 'Waste/loss reduction (%)', 'Process time reduction (%)', 'Throughput/productivity gain (%)',
      'Yield/recovery gain (%)', 'Profit/revenue gain (%)', 'Return on investment (%)', 'Internal rate of return (%)', 'Payback period (years)']
tech = D.set_index('id').tech; design = D.set_index('id').design; search = D.set_index('id').search


def study_values(Ex, metric):
    e = Ex[Ex.metric == metric]
    return e.groupby('id').value.median()


def summarise(Ex, lab):
    rows = []
    for m, mn in zip(M, Mn):
        v = study_values(Ex, m)
        if len(v) == 0: rows.append(dict(set=lab, metric=mn, n=0)); continue
        rows.append(dict(set=lab, metric=mn, n=len(v), median=r1(np.median(v)), q1=r1(q(v, .25)), q3=r1(q(v, .75)),
                         min=r1(v.min()), max=r1(v.max()), modelled=int((design[v.index] == 'TEA').sum()),
                         observed=int(design[v.index].isin(OBS).sum()),
                         by_tech='; '.join(f'{t}:{k} ({v[tech[v.index] == t].min():.1f}-{v[tech[v.index] == t].max():.1f})' for t, k in sorted(collections.Counter(tech[v.index]).items()))))
    return pd.DataFrame(rows)


Eu = E[E.use == 1]
sets = {'Primary (abstract values, full-text corrections applied)': Eu,
        'Verified in full text only (confirmed or corrected)': Eu[Eu.ft_status.isin(['confirmed', 'corrected'])],
        'Excluding best-case / scenario values': Eu[Eu.scenario != '1'],
        'Main search only': Eu[Eu.id.map(search) == 'main'],
        'Abstract values without full-text corrections (v1 method)': E[E.use == 1].assign(value=E[E.use == 1].value_abstract.astype(float))}
S = pd.concat([summarise(x, k) for k, x in sets.items()])
S.to_csv(os.path.join(RES, 'S_effect_sizes.csv'), index=False)
for k in sets:
    out(f'EFFECT SIZES - {k} (studies contributing: {Eu.id.nunique() if k.startswith("Primary") else sets[k].id.nunique()})')
    for _, r in S[S.set == k].iterrows():
        if r.n: out(f'  {r.metric:36s} n={int(r.n):2d}  median {r["median"]:.1f}  IQR {r.q1:.1f}-{r.q3:.1f}  range {r["min"]:.1f}-{r["max"]:.1f}  [modelled {int(r.modelled)}, observed {int(r.observed)}]' + (f'  by tech: {r.by_tech}' if k.startswith('Primary') else ''))
    out('')
qs = D[D.quant == 1]
out(f'Quantified studies: {len(qs)}; contributing to summary metrics: {Eu.id.nunique()}; quantified but only non-summarised metrics (e.g. absolute values, efficiency scores, coefficients): {len(set(qs.id) - set(Eu.id))}')
ft_e = E[(E.use == 1)]
out('Full-text status of summary effects: ' + ', '.join(f'{k or "not in sample"} {v}' for k, v in collections.Counter(ft_e.ft_status).items()))
out('')

# conditions
G = {'investment and operating cost': r'cost|capex|capital|investment|expens|afford|financ',
     'scale and firm size': r'scale|size|sme|small',
     'prices, demand and market access': r'price|market|demand|premium',
     'data and system integration': r'data|integrat|interoper|infrastruct|connectiv',
     'policy and subsidies': r'polic|subsid|regulat|government|incentive',
     'skills and workforce': r'skill|training|workforce|labou?r|expert|knowledge|human'}
c = D[D.conditions.str.strip() != ''].conditions.str.lower()
out(f'CONDITIONS recorded in {len(c)} studies: ' + '; '.join(f'{k} {int(c.str.contains(p).sum())}' for k, p in G.items()))
out('')

# regional relevance
CEE = {'Croatia', 'Serbia', 'Slovenia', 'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 'Albania', 'Kosovo', 'Bulgaria', 'Romania', 'Hungary',
       'Poland', 'Czech Republic', 'Czechia', 'Slovakia', 'Lithuania', 'Latvia', 'Estonia', 'Greece', 'Ukraine', 'Moldova'}
ISO = {'HR', 'RS', 'SI', 'BA', 'ME', 'MK', 'AL', 'XK', 'BG', 'RO', 'HU', 'PL', 'CZ', 'SK', 'LT', 'LV', 'EE', 'GR', 'UA', 'MD'}
reg = D.region.apply(lambda r: any(x.strip() in CEE for x in re.split(r'[,;/]| and ', r)))
auth = D.author_countries.apply(lambda r: any(x in ISO for x in r.split(';')))
out(f'REGION: setting in Central/South-East Europe {int(reg.sum())} studies ({", ".join(sorted(set(D.region[reg])))}); '
    f'at least one author affiliated in the region {int(auth.sum())}; setting not stated in abstract {int((D.region.isin(["n/a", ""])).sum())}')
fn = os.path.join(ROOT, 'data', 'excluded_not_indexed_countries.csv')
if os.path.exists(fn):
    X = pd.read_csv(fn, dtype=str).fillna('')
    xa = X.author_countries.apply(lambda r: any(x in ISO for x in r.split(';')))
    out(f'Records excluded by the indexing criterion: {len(X)}; with at least one author in Central/South-East Europe: {int(xa.sum())} ({", ".join(sorted(set(c for r in X.author_countries[xa] for c in r.split(";") if c in ISO)))})')
out('')

# recall estimate from sampled exclusions
k, n = int(P['sampled_exclusions_flagged']), int(P['sampled_exclusions_checked'])
ex_total = int(P['excluded_abstract'] + P['supp_excluded_abstract'])
ub = 3 / n if k == 0 else None
out(f'Sampled exclusions re-assessed in the second pass: {n}, flagged as relevant: {k}; rule-of-three upper 95 % bound of the miss rate {100 * ub:.2f} % '
    f'(about {ub * ex_total:.0f} of {ex_total} records excluded on abstract)')

open(os.path.join(RES, 'sensitivity.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
