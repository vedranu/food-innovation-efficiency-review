# -*- coding: utf-8 -*-
"""Human validation of LLM-assisted screening (response to review point 3.2).
Input : human_coding_sample.xlsx with sheets 'Coder_A' and 'Coder_B' (filled independently by two authors, without AI help),
        'Consensus' (disagreements resolved by discussion) and the hidden sheet 'Key' (LLM-assisted decisions and sampling stratum).
Sample: 100 records drawn at random in three strata: 40 finally included, 10 excluded at the second screening pass, 50 excluded on abstract
        (round 2: human_coding_sample_v2.xlsx, coded after calibration; round 1 is kept as a pilot).
Output: agreement_results.txt with
        - Cohen's kappa between the two human coders,
        - precision, recall, F1 and kappa of the LLM-assisted decision against the human consensus (unweighted sample),
        - recall weighted by the inverse sampling fraction of each stratum (estimate for the full set of assessed records).
Usage : python compute_agreement.py human_coding_sample.xlsx"""
import sys
import pandas as pd

# records assessed on title and abstract, by stratum (from data/prisma_counts.csv, main + supplementary search).
# 'included' = records judged relevant after the second pass and the third run, before the indexing criterion
# (276 - 15 + 132 - 13 = 380); the indexing criterion is not a relevance decision, so these records count as relevant.
POP = {'included': 380, 'second_pass_excluded': 28, 'abstract_excluded': 3337}


def kappa(a, b):
    a, b = list(a), list(b); n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return ((po - pe) / (1 - pe) if pe < 1 else 1.0), po


f = sys.argv[1] if len(sys.argv) > 1 else 'human_coding_sample.xlsx'
yes = lambda s: s.astype(str).str.strip().str.lower().isin(['1', '1.0', 'yes', 'y', 'da', 'include', 'true'])
low = lambda df: df.rename(columns=lambda c: str(c).strip().lower())
A, B, K, C = (low(pd.read_excel(f, s)) for s in ('Coder_A', 'Coder_B', 'Key', 'Consensus'))
assert A['include'].notna().all() and B['include'].notna().all(), 'Both coder sheets must be complete.'
a, b = yes(A['include']), yes(B['include'])
k_h, po_h = kappa(a, b)
out = [f'Records: {len(A)}', f'Human coder A vs B: agreement {100 * po_h:.1f} %, Cohen kappa = {k_h:.3f}',
       f'Disagreements between the coders: {int((a != b).sum())}']
if C['include'].notna().all():
    h = yes(C['include'])
else:
    h = a & b
    out.append('Consensus sheet incomplete: consensus approximated as include only if both coders include.')
m = yes(K['llm_include'])
tp, fp, fn, tn = int((m & h).sum()), int((m & ~h).sum()), int((~m & h).sum()), int((~m & ~h).sum())
prec = tp / (tp + fp) if tp + fp else float('nan'); rec = tp / (tp + fn) if tp + fn else float('nan')
f1 = 2 * prec * rec / (prec + rec) if prec + rec else float('nan')
k_m, po_m = kappa(m, h)
out += [f'LLM-assisted decision vs human consensus (sample): TP {tp}, FP {fp}, FN {fn}, TN {tn}',
        f'Precision {prec:.3f}, recall {rec:.3f}, F1 {f1:.3f}, agreement {100 * po_m:.1f} %, kappa {k_m:.3f}']
# stratum-weighted estimate of recall in the full set of assessed records
wt_tp = wt_fn = 0.0
for s, n_pop in POP.items():
    sel = K['stratum'] == s; n_s = int(sel.sum())
    if n_s == 0: continue
    w = n_pop / n_s
    wt_tp += w * int((m & h & sel).sum()); wt_fn += w * int((~m & h & sel).sum())
    out.append(f'  Stratum {s}: n = {n_s}, human include = {int((h & sel).sum())}, LLM include = {int((m & sel).sum())}, weight = {w:.1f}')
if wt_tp + wt_fn:
    out.append(f'Recall weighted to the full set of assessed records: {wt_tp / (wt_tp + wt_fn):.3f} (estimated relevant records missed: {wt_fn:.0f})')

# LLM-assisted decisions against the records on which both human coders agreed (no consensus step needed)
ag = a == b
ha, ma, sa = a[ag], m[ag], K['stratum'][ag]
tp2, fp2, fn2, tn2 = int((ma & ha).sum()), int((ma & ~ha).sum()), int((~ma & ha).sum()), int((~ma & ~ha).sum())
k2, po2 = kappa(ma, ha)
out += [f'LLM-assisted decision vs records where both coders agree (n = {int(ag.sum())}): TP {tp2}, FP {fp2}, FN {fn2}, TN {tn2}',
        f'Precision {tp2 / (tp2 + fp2):.3f}, recall {tp2 / (tp2 + fn2):.3f}, agreement {100 * po2:.1f} %, kappa {k2:.3f}']
w_tp = w_fn = 0.0
for s_, n_pop in POP.items():
    n_s = int((K['stratum'] == s_).sum())
    if n_s == 0: continue
    sel = sa == s_
    w_tp += n_pop / n_s * int((ma & ha & sel).sum()); w_fn += n_pop / n_s * int((~ma & ha & sel).sum())
if w_tp + w_fn:
    out.append(f'Recall weighted to the full set of assessed records (agreed records): {w_tp / (w_tp + w_fn):.3f} (estimated relevant records missed: {w_fn:.0f})')

# Lower bound of recall: recall = N_inc / (N_inc + missed_second_pass + p * N_abstract), with N_inc counted as relevant
# (precision on agreed records is 1.00) and p the miss rate among abstract-stage exclusions.
N_inc, N_sp, N_abs = POP['included'], POP['second_pass_excluded'], POP['abstract_excluded']
sp, ab = K['stratum'] == 'second_pass_excluded', K['stratum'] == 'abstract_excluded'
miss_sp_agreed = N_sp * int((a & b & sp).sum()) / int(sp.sum())
miss_sp_either = N_sp * int(((a | b) & sp).sum()) / int(sp.sum())
n_ab, k_both, k_either = int(ab.sum()), int((a & b & ab).sum()), int(((a | b) & ab).sum())
rec = lambda msp, p: N_inc / (N_inc + msp + p * N_abs)
out += [f'Abstract-stage exclusions in the sample: {n_ab}; relevant by both authors: {k_both}; by either author: {k_either}',
        f'Recall, agreed rule, point estimate: {rec(miss_sp_agreed, k_both / n_ab):.3f}',
        f'Recall, agreed rule, 95% lower bound (rule of three, p = 3/{n_ab} = {3 / n_ab:.3f}): {rec(miss_sp_agreed, 3 / n_ab):.3f}',
        f'Recall, either-author rule, point estimate (second pass {int(((a | b) & sp).sum())}/{int(sp.sum())}, abstract {k_either}/{n_ab}): {rec(miss_sp_either, k_either / n_ab):.3f}',
        f'Recall, either-author rule applied to the abstract stratum only (second pass as agreed): {rec(miss_sp_agreed, k_either / n_ab):.3f}']
open('agreement_results.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
