# Screening and extraction protocol

Review question: through which channels do technological innovations affect the economic efficiency of food-processing firms and food supply chains, and how strong is the evidence?

Read every record (title + abstract) in your batch file and output ONE JSON object per record.

## Eligibility (all must hold for include=true)
1. SETTING: food processing / food manufacturing firms, food industry, or the post-farm food supply chain (processing, packaging, storage, distribution, food retail logistics, food service operations). Agri-food supply chain studies are eligible if they cover post-farm stages. EXCLUDE studies confined to primary agriculture (on-farm crop/livestock production, precision farming, irrigation, agricultural machinery, farm TFP) with no processing or supply-chain stage.
2. TECHNOLOGY: a technological innovation, i.e. automation/robotics, AI/ML/computer vision/sensors/IoT/analytics, digital twins/simulation, blockchain/traceability/digital supply-chain platforms, firm-level digital transformation/Industry 4.0, advanced or novel processing (high pressure, PEF, cold plasma, ultrasound, ohmic, microwave, membrane, extrusion, 3D printing etc.), circular-economy/valorisation/waste-to-energy technologies.
3. ECONOMIC OUTCOME: the study reports or substantively analyses an economic or operational-efficiency outcome: costs, cost savings, productivity, TFP, labour productivity, throughput, OEE, yield/raw-material efficiency, energy or water cost, waste reduction with economic meaning, inventory, lead time, forecast accuracy linked to cost, profitability, ROI, NPV, IRR, payback, minimum selling price, revenue, firm/financial performance, market premium. A purely technical study (microbial reduction, product quality, model accuracy) with no economic/efficiency outcome is EXCLUDED. A single passing sentence like "this may reduce costs" is NOT enough.
4. STUDY TYPE: empirical (econometric, survey, case study), techno-economic / cost-benefit / simulation with economic results, or systematic/structured review focused on economic effects. Exclude editorials, pure opinion/conceptual pieces with no evidence, and studies not about technology (e.g. pure policy, consumer willingness to pay for food attributes without a technology-efficiency link).

## Output fields (JSON, one object per line)
- id: as in input
- include: true/false
- reason: if excluded, one code: SETTING | TECH | OUTCOME | TYPE | OFFTOPIC ; if included: ""
- tech: one main code: T1 automation_robotics | T2 AI_ML_sensors_IoT | T3 digital_twin_simulation | T4 blockchain_traceability_digitalSC | T5 firm_digital_transformation_I40 | T6 advanced_processing | T7 circular_valorisation | T8 other
- channels: list of codes affected: P1 productivity (labour, equipment, throughput, OEE, TFP) | P2 quality_safety (defects, rejects, recalls, shelf-life losses, compliance) | P3 resource_efficiency (energy, water, raw-material yield, waste, emissions with cost meaning) | P4 supply_chain_coordination (inventory, lead time, forecasting, traceability, logistics cost) | P5 revenue_financial (revenue, premium, profitability, ROI/NPV/payback, firm financial performance)
- design: E econometric_secondary_data | S survey_perception_SEM | C case_study_real_implementation | TEA techno_economic_or_simulation | R review | X conceptual
- region: country or region of the empirical setting (e.g. "China", "EU", "Italy", "India", "global", "n/a")
- subsector: e.g. dairy, meat, bakery, beverages, fruit_veg, seafood, general_food, supply_chain
- quant: true if the abstract reports at least one NUMERIC economic/efficiency effect (%, money, years, ratio, coefficient)
- effect_quote: if quant=true, copy the shortest VERBATIM fragment of the abstract containing the key numeric economic result (exact characters, max ~300 chars). Otherwise "". NEVER paraphrase, NEVER invent numbers.
- direction: "+" improvement, "-" worsening/no gain, "mixed", or "" if none reported
- conditions: up to 12 words on moderators/barriers mentioned (e.g. "firm size, skills, investment cost"), or ""
- note: up to 15 words summarising the finding in your own words

Be strict on criterion 3. When in doubt between include and exclude on criterion 3, exclude. Precision matters more than recall.
