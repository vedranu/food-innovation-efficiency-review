# -*- coding: utf-8 -*-
"""Figures for the structured review (Agroekonomika). Style follows the WSN/UAV papers.
Inputs : ../data/included.csv, ../data/prisma_counts.csv
Outputs: ../figures/Figure1_PRISMA.png|pdf, Figure2_design_by_technology.png|pdf, Figure3_evidence_map.png|pdf
Usage  : python figures.py"""
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, OUT = os.path.join(ROOT, 'data'), os.path.join(ROOT, 'figures'); os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7, 'axes.linewidth': 0.5, 'axes.edgecolor': '#52514e',
                     'text.color': '#0b0b0b', 'axes.labelcolor': '#0b0b0b', 'xtick.color': '#52514e', 'ytick.color': '#52514e',
                     'xtick.major.width': 0.5, 'ytick.major.width': 0.5})
SEQ = LinearSegmentedColormap.from_list('seq', ['#f4f8fd', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b'])
INK2 = '#52514e'; C1, C2, C3, C4 = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'; GRAY = '#a8a7a2'

def save(fig, name):
    for ext in ('png', 'pdf'):
        fig.savefig(os.path.join(OUT, f'{name}.{ext}'), dpi=600 if ext == 'png' else None, bbox_inches='tight', facecolor='white')
    plt.close(fig)
def clean(ax):
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
def fmt(n): return f'{n:,}'

D = pd.read_csv(os.path.join(DATA, 'included.csv'), dtype=str)
P = pd.read_csv(os.path.join(DATA, 'prisma_counts.csv')).set_index('step')['n']
pc = lambda k: int(P[k])
T = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7']
TN = ['Automation and robotics', 'AI, sensors and IoT analytics', 'Digital twins and simulation', 'Blockchain and digital traceability',
      'Firm-level digital transformation', 'Advanced processing', 'Circular valorisation']
CH = ['P1', 'P2', 'P3', 'P4', 'P5']
CHN = ['Productivity', 'Quality and\nsafety', 'Resource\nefficiency', 'Supply-chain\ncoordination', 'Revenue and\nfinancial\nperformance']
DG = [(['E', 'C'], 'Observed (econometric, case study)', C1), (['TEA'], 'Modelled (techno-economic, simulation)', C2),
      (['S'], 'Perceived (survey)', C3), (['R', 'X'], 'Secondary (review, conceptual)', GRAY)]

# ---------------- Figure 1: PRISMA flow (main search and supplementary search) ----------------
fig, ax = plt.subplots(figsize=(7.0, 6.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis('off')
FS = 4.9
def box(x, y, w, h, lines, edge, fill='white', bold_first=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.2,rounding_size=0.8', fc=fill, ec=edge, lw=0.7))
    n = len(lines); step = 2.15
    for i, s in enumerate(lines):
        yy = y + h / 2 + (n - 1) * step / 2 - i * step
        ax.text(x + w / 2, yy, s, ha='center', va='center', fontsize=FS, fontweight='bold' if (i == 0 and bold_first) else 'normal')
def arr(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='-|>', color=INK2, lw=0.6, mutation_scale=7))
# columns: main flow, main exclusions, supplementary flow, supplementary exclusions
X = [(5, 20), (27.5, 22.5), (52.5, 20), (75, 24.5)]
ax.text(X[0][0] + 22, 99.0, 'Main search (October 2026)', ha='center', fontsize=6.6, fontweight='bold', color=C1)
ax.text(X[2][0] + 23, 99.0, 'Supplementary search with efficiency terms', ha='center', fontsize=6.6, fontweight='bold', color=C1)
rows = [(83, 13), (66, 13), (50, 11), (35, 10), (21, 9)]
def col(c, r, lines, edge, fill='white'):
    x, w = X[c]; y, h = rows[r]; box(x, y, w, h, lines, edge, fill)
# main search
col(0, 0, ['Records identified', f'OpenAlex {fmt(pc("openalex_records"))}', f'Scopus {fmt(pc("scopus_records"))}', f'Web of Science {fmt(pc("wos_records"))}'], C1)
col(1, 0, ['Removed before screening', f'Duplicates {fmt(pc("duplicates_removed"))}', f'No DOI match in Scopus {pc("scopus_no_resolvable_doi")}', f'(matched by title in the', 'supplementary search:', f'{pc("scopus_no_doi_title_duplicates")} duplicates, {pc("scopus_no_doi_screened_in_update")} screened)'], GRAY)
col(0, 1, ['Records screened', f'(n = {fmt(pc("records_screened"))})'], C1)
col(1, 1, [f'Excluded on title ({pc("excluded_title_only")})', f'outcome {pc("excluded_title_outcome")}, setting {pc("excluded_title_setting")},', f'technology {pc("excluded_title_technology")}, off-topic {pc("excluded_title_offtopic")},', f'type {pc("excluded_title_type")}', f'No abstract ({pc("abstract_not_retrievable")})'], GRAY)
col(0, 2, ['Assessed on abstract', f'(n = {fmt(pc("assessed_title_abstract"))})'], C1)
col(1, 2, [f'Excluded ({fmt(pc("excluded_abstract"))})', f'outcome {pc("excluded_abstract_outcome")}, setting {pc("excluded_abstract_setting")},', f'technology {pc("excluded_abstract_technology")}, type {pc("excluded_abstract_type")},', f'off-topic {pc("excluded_abstract_offtopic")}'], GRAY)
col(0, 3, ['Included after first pass', f'(n = {pc("included_first_pass")})'], C1)
col(1, 3, ['Excluded', f'Second screening pass {pc("excluded_second_pass")}', f'Not in Scopus or WoS {pc("excluded_not_scopus_indexed")}'], GRAY)
col(0, 4, ['From main search', f'(n = {pc("included_final") - pc("excluded_full_text_main")}; {pc("included_final")} after screening,', f'{pc("excluded_full_text_main")} excluded at full text)'], C1)
# supplementary search
col(2, 0, ['Records identified', f'OpenAlex {fmt(pc("supp_openalex_records"))}', f'Scopus {fmt(pc("supp_scopus_records"))}', f'Web of Science {fmt(pc("supp_wos_records"))}'], C1)
col(3, 0, ['Removed before screening', 'Duplicates within the supplementary', f'search and with main search {fmt(pc("supp_duplicates_removed"))}'], GRAY)
col(2, 1, ['Records screened', f'(n = {fmt(pc("supp_records_screened"))}, incl. {pc("scopus_no_doi_screened_in_update")}', 'from main search)'], C1)
col(3, 1, [f'Excluded on title ({pc("supp_excluded_title_only")})', f'outcome {pc("supp_excluded_title_outcome")}, setting {pc("supp_excluded_title_setting")},', f'technology {pc("supp_excluded_title_technology")}, off-topic {pc("supp_excluded_title_offtopic")},', f'type {pc("supp_excluded_title_type")}', f'No abstract, not indexed ({pc("supp_abstract_not_retrievable_not_indexed")})'], GRAY)
col(2, 2, ['Assessed on abstract', f'(n = {fmt(pc("supp_assessed_title_abstract"))})'], C1)
col(3, 2, [f'Excluded ({fmt(pc("supp_excluded_abstract"))})', f'outcome {fmt(pc("supp_excluded_abstract_outcome"))}, setting {pc("supp_excluded_abstract_setting")},', f'technology {pc("supp_excluded_abstract_technology")}, type {pc("supp_excluded_abstract_type")},', f'off-topic {pc("supp_excluded_abstract_offtopic")}'], GRAY)
col(2, 3, ['Included after first pass', f'(n = {pc("supp_included_first_pass")})'], C1)
col(3, 3, ['Excluded', f'Second screening pass {pc("supp_excluded_second_pass")}', f'Not in Scopus or WoS {pc("supp_excluded_not_indexed")}'], GRAY)
col(2, 4, ['From supplementary search', f'(n = {pc("supp_included_final") - pc("excluded_full_text_supp")}; {pc("supp_included_final")} after screening,', f'{pc("excluded_full_text_supp")} excluded at full text)'], C1)
for c in (0, 2):
    x, w = X[c]; cx = x + w / 2
    for r in range(4): arr(cx, rows[r][0] - 0.3, cx, rows[r + 1][0] + rows[r + 1][1] + 0.3)
    for r in range(4): arr(x + w + 0.3, rows[r][0] + rows[r][1] / 2, X[c + 1][0] - 0.3, rows[r][0] + rows[r][1] / 2)
# included and full-text verification
box(28.5, 4, 30, 9, ['Studies included in the review', f'(n = {pc("included_total")})'], C2, fill='#fdf0ea')
box(63, 0.5, 36.5, 17, ['Full-text verification', f'Studies checked (observed or in', f'summary metrics) {pc("ft_sought")}; accessed {pc("ft_accessed")}', f'Excluded {pc("excluded_full_text_check")} (outcome 1, source 1)', f'Design reclassified {pc("ft_design_changed")}', f'Summary values checked {pc("ft_summary_values_checked")}:', f'{pc("ft_summary_values_checked") - pc("ft_summary_values_corrected") - pc("ft_summary_values_not_found")} confirmed, {pc("ft_summary_values_corrected")} corrected, {pc("ft_summary_values_not_found")} abstract only'], C3)
arr(X[0][0] + X[0][1] / 2, 21 - 0.3, 28.5 + 6, 13.3); arr(X[2][0] + X[2][1] / 2, 21 - 0.3, 28.5 + 24, 13.3)
arr(58.8, 8.5, 62.7, 8.5)
for y, s in [(89.5, 'Identification'), (50, 'Screening'), (8.5, 'Included')]:
    ax.text(1.5, y, s, fontsize=6.6, fontweight='bold', color=INK2, va='center', ha='center', rotation=90)
save(fig, 'Figure1_PRISMA')

# ---------------- Figure 2: evidence type by technology ----------------
M = np.array([[((D.tech == t) & D.design.isin(g)).sum() for g, _, _ in DG] for t in T])
o = np.argsort(M.sum(1))
fig, ax = plt.subplots(figsize=(6.3, 2.9))
left = np.zeros(len(T))
for j, (_, lab, col) in enumerate(DG):
    v = M[o, j]; ax.barh(range(len(T)), v, left=left, color=col, height=0.62, label=lab, edgecolor='white', linewidth=0.4)
    for i, (l, x) in enumerate(zip(left, v)):
        if x >= 3: ax.text(l + x / 2, i, str(x), ha='center', va='center', fontsize=6, color='white')
    left += v
for i, tot in enumerate(M[o].sum(1)): ax.text(tot + 0.8, i, f'{tot}', va='center', fontsize=6.5, color=INK2)
ax.set_yticks(range(len(T))); ax.set_yticklabels([TN[k] for k in o]); ax.set_xlabel('Number of studies')
ax.set_xlim(0, M.sum(1).max() * 1.08); clean(ax); ax.grid(axis='x', color='#e6e5e0', lw=0.4); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=6.5, loc='lower right')
ax.set_title(f'Included studies by technology group and evidence type (n = {len(D)})', fontsize=7.5, loc='left')
nO = int((D.tech == 'T8').sum())
fig.text(0.01, -0.04, f'{nO} studies coded as "other technology" are not shown. Observed = {int(D.design.isin(["E","C"]).sum())}, modelled = {int((D.design=="TEA").sum())}, '
         f'perceived = {int((D.design=="S").sum())}, secondary = {int(D.design.isin(["R","X"]).sum())} studies.', fontsize=6, color=INK2)
save(fig, 'Figure2_design_by_technology')

# ---------------- Figure 3: evidence map ----------------
n = np.zeros((len(T), len(CH)), int); g = np.zeros_like(n)
for i, t in enumerate(T):
    for k, c in enumerate(CH):
        s = (D.tech == t) & D.channels.str.contains(c)
        nn = int(s.sum()); obs = int((s & D.design.isin(['E', 'C'])).sum()); obsQ = int((s & D.design.isin(['E', 'C']) & (D.quant == '1')).sum())
        modQ = int((s & (D.design == 'TEA') & (D.quant == '1')).sum()); pos = int((s & (D.direction == '+')).sum())
        n[i, k] = nn
        g[i, k] = 3 if (nn >= 5 and obs >= 3 and obsQ >= 2 and pos / nn >= 0.8) else 2 if (nn >= 5 and (obsQ >= 1 or modQ >= 3)) else 1 if nn >= 3 else 0
fig, ax = plt.subplots(figsize=(6.3, 3.9))
im = ax.imshow(n, cmap=SEQ, vmin=0, vmax=n.max(), aspect='auto')
for i in range(len(T)):
    for k in range(len(CH)):
        tc = 'white' if n[i, k] > 0.55 * n.max() else '#0b0b0b'
        if n[i, k] == 0: ax.text(k, i, '·', ha='center', va='center', color=INK2, fontsize=8); continue
        ax.text(k, i - 0.14, str(n[i, k]), ha='center', va='center', fontsize=7.5, fontweight='bold', color=tc)
        if g[i, k] >= 1: ax.text(k, i + 0.24, '●' * g[i, k], ha='center', va='center', fontsize=5.5, color=C2)
ax.set_xticks(range(len(CH))); ax.set_xticklabels(CHN, fontsize=6.5); ax.xaxis.tick_top()
ax.set_yticks(range(len(T))); ax.set_yticklabels(TN, fontsize=7)
ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xticks(np.arange(-.5, len(CH), 1), minor=True); ax.set_yticks(np.arange(-.5, len(T), 1), minor=True)
ax.grid(which='minor', color='white', lw=1.5); ax.tick_params(which='minor', length=0)
cb = fig.colorbar(im, ax=ax, orientation='horizontal', fraction=0.045, pad=0.04, aspect=40)
cb.set_label('Number of studies', fontsize=6.5); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=6)
ax.set_title('Evidence map: technology group × efficiency channel', fontsize=7.5, loc='left', pad=34)
fig.text(0.01, 0.0, 'Evidence grade: ●●● strong, ●● moderate, ● limited, no dot insufficient (rules in Table 1); · = no study. A study may address several channels.',
         fontsize=6, color=INK2)
save(fig, 'Figure3_evidence_map')
print('figures written to', OUT)
