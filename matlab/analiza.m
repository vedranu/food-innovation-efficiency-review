%% analiza.m - Technological innovation and economic efficiency in the food industry: structured review
% Input : data\included.csv, data\effects.csv, data\prisma_counts.csv
% Output: results\*.csv, results\rezultati.txt (figures: python\figures.py; sensitivity analyses: python\sensitivity.py)
% v2 (revision): 309 studies (main + supplementary search); designs and effect values after full-text verification
clear; clc; rng(42);
root = fileparts(fileparts(mfilename('fullpath')));
res = fullfile(root, 'results'); fig = fullfile(root, 'figures');
if ~exist(res, 'dir'), mkdir(res); end
if ~exist(fig, 'dir'), mkdir(fig); end

blue = [42 120 214]/255; orange = [235 104 52]/255; aqua = [27 175 122]/255; gray = [138 138 134]/255;
set(groot, 'defaultAxesFontName', 'Times New Roman', 'defaultTextFontName', 'Times New Roman', ...
    'defaultAxesFontSize', 10, 'defaultAxesBox', 'off', 'defaultAxesTickDir', 'out', 'defaultAxesGridAlpha', 0.15);
exportf = @(f, name) exportBoth(f, fig, name);

%% data
opts = detectImportOptions(fullfile(root, 'data', 'included.csv'), 'TextType', 'string');
opts = setvartype(opts, intersect(opts.VariableNames, {'id','doi','title','source','db','tech','tech_label','channels','design','region','subsector','direction','conditions','note','effect_quote','reference','search','author_countries','design_abstract'}), 'string');
D = readtable(fullfile(root, 'data', 'included.csv'), opts); N = height(D);
E = readtable(fullfile(root, 'data', 'effects.csv'), 'TextType', 'string');
Pc = readtable(fullfile(root, 'data', 'prisma_counts.csv'), 'TextType', 'string');
pc = @(s) Pc.n(Pc.step == s);

T  = ["T1","T2","T3","T4","T5","T6","T7"];
Tn = ["Automation and robotics","AI, sensors and IoT analytics","Digital twins and simulation", ...
      "Blockchain and digital traceability","Firm-level digital transformation","Advanced processing","Circular valorisation"];
P  = ["P1","P2","P3","P4","P5"];
Pn = ["Productivity","Quality and safety","Resource efficiency","Supply-chain coordination","Revenue and financial performance"];
Pshort = ["Productivity","Quality & safety","Resource efficiency","SC coordination","Revenue & financial"];
DG = {["E","C"], "TEA", "S", ["R","X"]}; DGn = ["Observed (econometric, case)","Modelled (techno-economic, simulation)","Perceived (survey)","Secondary (review, conceptual)"];

fid = fopen(fullfile(res, 'rezultati.txt'), 'w', 'n', 'UTF-8'); out = @(varargin) fprintf(fid, varargin{:});
out('N = %d included studies (main search %d, supplementary search %d)\n', N, sum(D.search=="main"), sum(D.search=="supplementary"));
out('Source: OpenAlex and Scopus %d, Scopus only %d, OpenAlex (Scopus-indexed) %d, Web of Science only %d, OpenAlex (WoS-indexed) %d\n', sum(D.db=="both"), sum(D.db=="Scopus"), sum(D.db=="OpenAlex (Scopus-indexed)"), sum(D.db=="Web of Science"), sum(D.db=="OpenAlex (WoS-indexed)"));
out('Years: 2015-2020 %d; 2021-2023 %d; 2024-2026 %d; median %g\n', sum(D.year<=2020), sum(D.year>=2021 & D.year<=2023), sum(D.year>=2024), median(D.year));
out('Agreement between screening passes, main search (n=%d): %.1f %%, kappa = %.3f; all double-assessed records (n=%d): %.1f %%, kappa = %.3f\n\n', pc("double_coded_records"), 100*pc("double_coded_agreement")/pc("double_coded_records"), pc("double_coded_kappa"), pc("all_double_coded_records"), 100*pc("all_double_coded_agreement")/pc("all_double_coded_records"), pc("all_double_coded_kappa"));

%% technology and design
cntT = arrayfun(@(t) sum(D.tech == t), T);
desM = zeros(numel(T), numel(DG));
for i = 1:numel(T), for j = 1:numel(DG), desM(i, j) = sum(D.tech == T(i) & ismember(D.design, DG{j})); end, end
out('TECHNOLOGY (n, %%) and design [observed modelled perceived secondary]\n');
for i = 1:numel(T), out('  %-40s %3d (%4.1f %%)  [%d %d %d %d]\n', Tn(i), cntT(i), 100*cntT(i)/N, desM(i, :)); end
out('  Other: %d\n', sum(D.tech == "T8"));
tot = sum(desM, 1) + [sum(D.tech=="T8" & ismember(D.design, DG{1})) sum(D.tech=="T8" & D.design=="TEA") sum(D.tech=="T8" & D.design=="S") sum(D.tech=="T8" & ismember(D.design, DG{4}))];
out('  Design totals: observed %d (%.1f %%), modelled %d (%.1f %%), perceived %d (%.1f %%), secondary %d (%.1f %%)\n', tot(1), 100*tot(1)/N, tot(2), 100*tot(2)/N, tot(3), 100*tot(3)/N, tot(4), 100*tot(4)/N);
out('  Quantified effect in abstract: %d (%.1f %%); positive direction: %d (%.1f %%), mixed %d, negative %d\n\n', sum(D.quant==1), 100*mean(D.quant==1), sum(D.direction=="+"), 100*mean(D.direction=="+"), sum(D.direction=="mixed"), sum(D.direction=="-"));
writetable(array2table([cntT' desM], 'VariableNames', {'n','observed','modelled','perceived','secondary'}, 'RowNames', cellstr(Tn)), fullfile(res, 'T_technology_design.csv'), 'WriteRowNames', true);

%% evidence map: technology x channel, with grading
ch = @(k) contains(D.channels, P(k));
nM = zeros(numel(T), numel(P)); G = strings(numel(T), numel(P)); Gs = zeros(numel(T), numel(P));
obsM = nM; obsQM = nM; modQM = nM; posM = nM;
for i = 1:numel(T), for k = 1:numel(P)
    s = D.tech == T(i) & ch(k);
    n = sum(s); obs = sum(s & ismember(D.design, ["E","C"])); obsQ = sum(s & ismember(D.design, ["E","C"]) & D.quant == 1);
    modQ = sum(s & D.design == "TEA" & D.quant == 1); pos = sum(s & D.direction == "+");
    nM(i,k) = n; obsM(i,k) = obs; obsQM(i,k) = obsQ; modQM(i,k) = modQ; posM(i,k) = pos;
    if n >= 5 && obs >= 3 && obsQ >= 2 && pos/n >= 0.8, G(i,k) = "Strong"; Gs(i,k) = 3;
    elseif n >= 5 && (obsQ >= 1 || modQ >= 3), G(i,k) = "Moderate"; Gs(i,k) = 2;
    elseif n >= 3, G(i,k) = "Limited"; Gs(i,k) = 1;
    elseif n >= 1, G(i,k) = "Insufficient"; Gs(i,k) = 0;
    else, G(i,k) = "None"; Gs(i,k) = -1; end
end, end
out('EVIDENCE MAP (n studies; grade)\n');
for i = 1:numel(T)
    out('  %-40s', Tn(i)); for k = 1:numel(P), out(' %2d %-12s', nM(i,k), G(i,k)); end; out('\n');
end
chTot = arrayfun(@(k) sum(ch(k)), 1:numel(P));
out('  Channel totals (studies may address several channels):'); for k = 1:numel(P), out(' %s %d (%.1f %%);', Pn(k), chTot(k), 100*chTot(k)/N); end; out('\n\n');
Tm = table(repelem(Tn', numel(P)), repmat(Pn', numel(T), 1), reshape(nM', [], 1), reshape(obsM', [], 1), reshape(obsQM', [], 1), reshape(modQM', [], 1), reshape(posM', [], 1), reshape(G', [], 1), ...
    'VariableNames', {'technology','channel','n','observed','observed_quantified','modelled_quantified','positive','grade'});
writetable(Tm, fullfile(res, 'T_evidence_map.csv'));

%% channel-level summary (for Table 2)
out('CHANNEL SUMMARY\n');
for k = 1:numel(P)
    s = ch(k);
    out('  %-34s n=%3d | observed %2d, modelled %2d, perceived %2d, secondary %2d | quantified %2d | positive %.0f %%\n', Pn(k), sum(s), ...
        sum(s & ismember(D.design, ["E","C"])), sum(s & D.design=="TEA"), sum(s & D.design=="S"), sum(s & ismember(D.design, ["R","X"])), sum(s & D.quant==1), 100*mean(D.direction(s)=="+"));
end
out('\n');

%% effect sizes (one value per study and metric = study median)
M  = ["energy_utility_reduction_pct","cost_reduction_pct","waste_loss_reduction_pct","time_reduction_pct","throughput_productivity_increase_pct","yield_recovery_increase_pct","profit_revenue_increase_pct","roi_pct","irr_pct","payback_years"];
Mn = ["Energy/utility use reduction (%)","Cost reduction (%)","Waste/loss reduction (%)","Process time reduction (%)","Throughput/productivity gain (%)","Yield/recovery gain (%)","Profit/revenue gain (%)","Return on investment (%)","Internal rate of return (%)","Payback period (years)"];
Eu = E(E.use_in_summary == 1, :);
S = table('Size', [numel(M) 7], 'VariableTypes', {'string','double','double','double','double','double','double'}, 'VariableNames', {'metric','n_studies','median','q1','q3','min','max'});
V = cell(numel(M), 1);
out('EFFECT SIZES (study-level medians)\n');
for m = 1:numel(M)
    e = Eu(Eu.metric == M(m), :); ids = unique(e.id); v = zeros(numel(ids), 1);
    for j = 1:numel(ids), v(j) = median(e.value(e.id == ids(j))); end
    V{m} = v; q = quantile(v, [0.25 0.75]);
    S(m, :) = {Mn(m), numel(v), median(v), q(1), q(2), min(v), max(v)};
    out('  %-36s n=%2d  median %.1f  IQR %.1f-%.1f  range %.1f-%.1f\n', Mn(m), numel(v), median(v), q(1), q(2), min(v), max(v));
end
writetable(S, fullfile(res, 'T_effect_sizes.csv'));
out('\nNegative/mixed findings: %d studies; examples listed in results\\T_negative_mixed.csv\n', sum(D.direction=="-" | D.direction=="mixed"));
writetable(D(D.direction=="-" | D.direction=="mixed", {'id','tech','channels','design','note','reference'}), fullfile(res, 'T_negative_mixed.csv'));
fclose(fid);

fprintf('Done: %s\n', res);

function s = addc(n)
s = regexprep(sprintf('%d', n), '(\d)(?=(\d{3})+$)', '$1,');
end

function exportBoth(f, fig, name)
exportgraphics(f, fullfile(fig, [name '.png']), 'Resolution', 300, 'BackgroundColor', 'white');
exportgraphics(f, fullfile(fig, [name '.tif']), 'Resolution', 300, 'BackgroundColor', 'white');
end
