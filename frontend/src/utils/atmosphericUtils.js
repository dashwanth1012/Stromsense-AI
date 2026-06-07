/** Safe numeric helpers for operational convective dashboards */

export const DEFAULT_STATION = {
  station: "Visakhapatnam",
  station_code: "43150",
  cape: 2850,
  cin: -45,
  lifted_index: -7.5,
  sweat_index: 340,
  k_index: 38,
  pwat: 68,
  tt_index: 52.5,
  lcl: 850,
  lfc: 810,
  el: 120,
  bulk_shear: 18,
  theta_e: 358,
  moisture_convergence: 12.4,
  forecast: "SEVERE THUNDERSTORM RISK",
  storm_probability: 85,
  sounding_available: true,
  post_convective_stabilization: false,
};

export function safeNum(value, fallback = 0) {
  const n = Number(value);
  if (!Number.isFinite(n)) return fallback;
  return n;
}

export function clampPercent(value, fallback = 0) {
  const n = safeNum(value, fallback);
  return Math.min(100, Math.max(0, Math.round(n)));
}

export function formatIndex(value, decimals = 1) {
  const n = safeNum(value, null);
  if (n === null) return "—";
  return Number.isInteger(n) ? String(n) : n.toFixed(decimals);
}

export function normalizeStation(raw) {
  if (!raw || typeof raw !== "object") return { ...DEFAULT_STATION };
  return {
    ...DEFAULT_STATION,
    ...raw,
    station: raw.station || DEFAULT_STATION.station,
    station_code: raw.station_code || DEFAULT_STATION.station_code,
    cape: safeNum(raw.cape, DEFAULT_STATION.cape),
    cin: safeNum(raw.cin, DEFAULT_STATION.cin),
    lifted_index: safeNum(raw.lifted_index, DEFAULT_STATION.lifted_index),
    sweat_index: safeNum(raw.sweat_index, DEFAULT_STATION.sweat_index),
    k_index: safeNum(raw.k_index, DEFAULT_STATION.k_index),
    pwat: safeNum(raw.pwat, DEFAULT_STATION.pwat),
    tt_index: safeNum(raw.tt_index, DEFAULT_STATION.tt_index),
    lcl: safeNum(raw.lcl, DEFAULT_STATION.lcl),
    lfc: safeNum(raw.lfc, DEFAULT_STATION.lfc),
    el: safeNum(raw.el, DEFAULT_STATION.el),
    bulk_shear: safeNum(raw.bulk_shear, DEFAULT_STATION.bulk_shear),
    theta_e: safeNum(raw.theta_e, DEFAULT_STATION.theta_e),
    moisture_convergence: safeNum(raw.moisture_convergence, DEFAULT_STATION.moisture_convergence),
    storm_probability: clampPercent(raw.storm_probability, DEFAULT_STATION.storm_probability),
    sounding_available: raw.sounding_available !== false,
    post_convective_stabilization: Boolean(raw.post_convective_stabilization),
  };
}

export function validateForecastPayload(data) {
  if (!Array.isArray(data)) return [];
  return data.map(normalizeStation).filter((s) => s.station);
}

/** Operational threshold explainability (IMD CWC coastal corridor) */
export const OPERATIONAL_INDEX_RULES = {
  CAPE: [
    { test: (v) => v >= 4000, label: "Explosive Buoyancy", desc: "Explosive convection setup; violent updrafts likely.", observed: "Severe TS / SQ", color: "#a855f7" },
    { test: (v) => v >= 2500, label: "Explosive Buoyancy", desc: "High thermal energy supports organized severe thunderstorms.", observed: "TS / TSRA", color: "#ef4444" },
    { test: (v) => v >= 1500, label: "Moderate Instability", desc: "Standard thunderstorm development possible if triggered.", observed: "TS / SHRA", color: "#eab308" },
    { test: (v) => v < 100, label: "Post-Convective Depletion", desc: "Buoyancy consumed; stratiform rain may persist on residual moisture.", observed: "SHRA / RA", color: "#10b981" },
    { test: () => true, label: "Weak Instability", desc: "Limited updraft potential.", observed: "NWX", color: "#10b981" },
  ],
  LI: [
    { test: (v) => v <= -6, label: "Deep Instability", desc: "Steep lapse rates; parcels remain strongly buoyant at 500 hPa.", observed: "TS / Severe TS", color: "#ef4444" },
    { test: (v) => v <= -4, label: "Moderate Instability", desc: "Convective initiation probable with forcing.", observed: "TS / TSRA", color: "#eab308" },
    { test: (v) => v > -2, label: "Stable Layer", desc: "Capping limits deep convection.", observed: "NWX / SHRA", color: "#10b981" },
    { test: () => true, label: "Weak Instability", desc: "Marginal buoyancy.", observed: "NWX", color: "#64748b" },
  ],
  SWEAT: [
    { test: (v) => v >= 400, label: "Dangerous Severe Setup", desc: "Strong shear supports supercells and damaging winds.", observed: "SQ / Severe TS", color: "#a855f7" },
    { test: (v) => v >= 300, label: "Organized Severe Convection", desc: "Landward squall lines and organized bands likely.", observed: "SQ / TSRA", color: "#f97316" },
    { test: () => true, label: "Weak Shear", desc: "Pulse storms; limited organization.", observed: "TS", color: "#10b981" },
  ],
  K_Index: [
    { test: (v) => v >= 35, label: "Thunderstorm Support", desc: "Deep mid-level moisture sustains efficient storm cores.", observed: "TS / TSRA", color: "#ef4444" },
    { test: (v) => v >= 30, label: "Moderate Support", desc: "Adequate moisture depth for convection.", observed: "TS / SHRA", color: "#eab308" },
    { test: () => true, label: "Limited Support", desc: "Dry mid-levels may suppress storms.", observed: "NWX", color: "#10b981" },
  ],
  PWAT: [
    { test: (v) => v >= 65, label: "Flash Flood Potential", desc: "Saturated column; torrential rainfall efficiency.", observed: "Heavy Rain / TSRA", color: "#a855f7" },
    { test: (v) => v >= 60, label: "Heavy Rainfall Potential", desc: "Deep moisture loading supports high rain rates.", observed: "Heavy Rain / SHRA", color: "#f97316" },
    { test: (v) => v >= 50, label: "Moderate Rainfall", desc: "Efficient stratiform and convective rainfall.", observed: "SHRA / RA", color: "#eab308" },
    { test: () => true, label: "Moderate Moisture", desc: "Normal rain potential.", observed: "NWX", color: "#10b981" },
  ],
  CIN: [
    { test: (v) => v <= -80, label: "Strong Capping", desc: "Significant inhibition; explosive release if cap breaks.", observed: "Delayed TS", color: "#f97316" },
    { test: (v) => v <= -40, label: "Moderate CIN", desc: "Some suppression before initiation.", observed: "TS", color: "#eab308" },
    { test: () => true, label: "Weak CIN", desc: "Low barrier to convection.", observed: "TS / NWX", color: "#10b981" },
  ],
  TT: [
    { test: (v) => v >= 55, label: "Severe Environment", desc: "Totals Totals indicate violent convection potential.", observed: "Severe TS", color: "#ef4444" },
    { test: (v) => v >= 50, label: "Thunderstorm Favored", desc: "Elevated total totals support storms.", observed: "TS / TSRA", color: "#eab308" },
    { test: () => true, label: "Stable Totals", desc: "Limited convective potential.", observed: "NWX", color: "#10b981" },
  ],
  Bulk_Shear: [
    { test: (v) => v >= 20, label: "Strong Deep Shear", desc: "Supports organized squall lines and supercells.", observed: "SQ", color: "#ef4444" },
    { test: (v) => v >= 12, label: "Moderate Shear", desc: "Storm organization and propagation likely.", observed: "TSRA", color: "#eab308" },
    { test: () => true, label: "Weak Shear", desc: "Pulse convection dominant.", observed: "TS", color: "#10b981" },
  ],
};

export function interpretOperationalIndex(key, val) {
  const rules = OPERATIONAL_INDEX_RULES[key];
  if (!rules || val === null || val === undefined || !Number.isFinite(Number(val))) {
    return { label: "UNKNOWN", desc: "No telemetry.", color: "#64748b", observed: "—" };
  }
  const v = Number(val);
  const match = rules.find((r) => r.test(v));
  return match
    ? { label: match.label, desc: match.desc, color: match.color, observed: match.observed }
    : { label: "NOMINAL", desc: "Standard environment.", color: "#10b981", observed: "NWX" };
}
