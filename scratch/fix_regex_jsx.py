import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'frontend/src/components/modules/ResearchHub.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Step 5 formulas replacements
f5_1_target = 'Theta-E = Theta_dry * exp((2.5e6 * w_s) / (1005.7 * T_LCL))'
f5_1_repl = '{"Theta-E = Theta_dry * exp((2.5e6 * w_s) / (1005.7 * T_LCL))"}'

f5_2_target = 'T_LCL = 55 / (1/(Td - 56) + ln(T/Td)/800) + 56'
f5_2_repl = '{"T_LCL = 55 / (1/(Td - 56) + ln(T/Td)/800) + 56"}'

f5_3_target = 'CAPE = g * Integrate[ (T_parcel - T_env)/T_env, {"{ z_LFC, z_EL }"} ]'
f5_3_repl = '{"CAPE = g * Integrate[ (T_parcel - T_env) / T_env, { z_LFC, z_EL } ]"}'

content = content.replace(f5_1_target, f5_1_repl)
content = content.replace(f5_2_target, f5_2_repl)
content = content.replace(f5_3_target, f5_3_repl)

# Step 7 formula replacement
f7_target = 'Weight_i = (Dev_i / Sum(Dev_j)) * 100%'
f7_repl = '{"Weight_i = (Dev_i / Sum(Dev_j)) * 100%"}'
content = content.replace(f7_target, f7_repl)

# Step 10 list item replacements
f10_1_target = '<li>CSI = Hits / (Hits + Misses + FalseAlarms) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.csi ?? "0.92"}</li>'
f10_1_repl = '<li>{"CSI = Hits / (Hits + Misses + FalseAlarms) = "}{historicalAnalysis.forecast_vs_observed?.validation_metrics?.csi ?? "0.92"}</li>'

f10_2_target = '<li>POD = Hits / (Hits + Misses) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.pod ?? "0.95"}</li>'
f10_2_repl = '<li>{"POD = Hits / (Hits + Misses) = "}{historicalAnalysis.forecast_vs_observed?.validation_metrics?.pod ?? "0.95"}</li>'

f10_3_target = '<li>FAR = FalseAlarms / (Hits + FalseAlarms) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.far ?? "0.08"}</li>'
f10_3_repl = '<li>{"FAR = FalseAlarms / (Hits + FalseAlarms) = "}{historicalAnalysis.forecast_vs_observed?.validation_metrics?.far ?? "0.08"}</li>'

f10_4_target = '<li>HSS = 2*(ad - bc) / [(a+c)(c+d) + (a+b)(b+d)] = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.hss ?? "0.85"}</li>'
f10_4_repl = '<li>{"HSS = 2*(ad - bc) / [(a+c)(c+d) + (a+b)(b+d)] = "}{historicalAnalysis.forecast_vs_observed?.validation_metrics?.hss ?? "0.85"}</li>'

f10_5_target = '<li>BIAS = (Hits + FalseAlarms) / (Hits + Misses) = {historicalAnalysis.forecast_vs_observed?.validation_metrics?.bias ?? "1.02"}</li>'
f10_5_repl = '<li>{"BIAS = (Hits + FalseAlarms) / (Hits + Misses) = "}{historicalAnalysis.forecast_vs_observed?.validation_metrics?.bias ?? "1.02"}</li>'

content = content.replace(f10_1_target, f10_1_repl)
content = content.replace(f10_2_target, f10_2_repl)
content = content.replace(f10_3_target, f10_3_repl)
content = content.replace(f10_4_target, f10_4_repl)
content = content.replace(f10_5_target, f10_5_repl)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Replaced all division symbols inside JSX text nodes.")
