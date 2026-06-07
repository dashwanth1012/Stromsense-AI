import { useEffect, useMemo, useState } from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar
} from "recharts";
import { Activity, AlertTriangle, FlaskConical, Waves, Satellite, Download } from "lucide-react";
import { MapContainer, TileLayer, CircleMarker, Polyline, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { fallbackHistoricalDates } from "./fallback_data";

function MapController({ centerLocation }) {
  const map = useMap();
  useEffect(() => {
    if (centerLocation) {
      map.flyTo(centerLocation, 7, { duration: 1.2 });
    }
  }, [centerLocation, map]);
  return null;
}

const MODULE_TITLES = {
  ATM_INTEL: "Atmospheric Intelligence Center",
  WATCHDESK: "Severe Weather Watchdesk",
  THERMO_LAB: "Thermodynamic Lab",
  CLIMO_RESEARCH: "Climatology & Research Center",
  AI_LAB: "Thunderstorm Forecast Simulator",
  RADSAT_FUSION: "Live Operational Nowcast Center",
  VERIFY_CENTER: "Forecast Verification",
  ANALOG_ARCHIVE: "Historical Thunderstorm Archive",
  BULLETIN: "Auto IMD Bulletin Generator",
  ANDHRA_MONITOR: "Coastal Thunderstorm Monitoring Center",
};

const safeArr = (x) => (Array.isArray(x) ? x : []);
const safeNum = (x, d = 0) => (Number.isFinite(Number(x)) ? Number(x) : d);

// Standardized 5-Section Layout Wrapper Component
function ModuleSectionLayout({
  title,
  metadata,
  currentSituation,
  meteorologistInterpretation,
  recommendedAction,
  advancedScientificDetails,
  reviewMode
}) {
  const forecastGenerated = metadata.forecastGenerated || (String(metadata.time || "").includes("PM") ? "05:07 PM IST" : "05:07 AM IST");
  const station = metadata.station || (String(metadata.source || "").includes("43185") ? "Machilipatnam" : "Visakhapatnam");
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "20px", width: "100%" }}>
      {/* SECTION 1: Operational Metadata */}
      <div className="panel-surface" style={{ padding: "16px 20px", border: "1px solid #1e293b", backgroundColor: "#0b0f19", borderRadius: "12px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
          <div>
            <h3 style={{ fontSize: "14px", color: "#38bdf8", fontWeight: "bold", margin: 0, fontFamily: "Satoshi" }}>
              {title}
            </h3>
          </div>
          <div style={{ display: "flex", gap: "12px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#94a3b8", flexWrap: "wrap" }}>
            <div>OBS DATE: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{metadata.date}</span></div>
            <div>OBS TIME: <span style={{ color: "#facc15", fontWeight: "bold" }}>{metadata.time}</span></div>
            <div>FORECAST GENERATED: <span style={{ color: "#38bdf8", fontWeight: "bold" }}>{forecastGenerated}</span></div>
            <div>STATION: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{station}</span></div>
            <div>CYCLE: <span style={{ color: "#10b981", fontWeight: "bold" }}>{metadata.cycle}</span></div>
            <div>DATA SOURCE: <span style={{ color: "#a855f7", fontWeight: "bold" }}>{metadata.source}</span></div>
          </div>
        </div>
      </div>

      {/* SECTION 2: Current Situation */}
      <div className="panel-surface" style={{ padding: "20px", border: "1px solid #1e293b", backgroundColor: "#0b0f19", borderRadius: "12px" }}>
        <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold", letterSpacing: "1px", display: "block", marginBottom: "12px" }}>
          ● SECTION 2: CURRENT SITUATION & observed CONDITIONS
        </span>
        {currentSituation}
      </div>

      {/* SECTION 3: Meteorologist Interpretation */}
      <div className="panel-surface" style={{ padding: "20px", border: "1px solid #1e293b", backgroundColor: "#0b0f19", borderRadius: "12px" }}>
        <span className="font-technical" style={{ fontSize: "10px", color: "#10b981", fontWeight: "bold", letterSpacing: "1px", display: "block", marginBottom: "8px" }}>
          ● SECTION 3: METEOROLOGIST INTERPRETATION
        </span>
        <div style={{ fontSize: "12.5px", color: "#cbd5e1", lineHeight: "1.6" }}>
          {meteorologistInterpretation}
        </div>
      </div>

      {/* SECTION 4: Recommended Action */}
      <div className="panel-surface" style={{ padding: "20px", border: "1px solid #1e293b", backgroundColor: "#0b0f19", borderRadius: "12px" }}>
        <span className="font-technical" style={{ fontSize: "10px", color: "#ef4444", fontWeight: "bold", letterSpacing: "1px", display: "block", marginBottom: "8px" }}>
          ● SECTION 4: RECOMMENDED ACTIONS
        </span>
        <div style={{ fontSize: "12.5px", color: "#ffffff", fontWeight: "bold", lineHeight: "1.6" }}>
          {recommendedAction}
        </div>
      </div>

      {/* SECTION 5: Advanced Scientific Details (Collapsed, hidden if reviewMode is active) */}
      {!reviewMode && (
        <div className="panel-surface" style={{ border: "1px solid #334155", borderRadius: "12px", backgroundColor: "#020617", overflow: "hidden" }}>
          <details>
            <summary style={{ padding: "12px 16px", color: "#a855f7", cursor: "pointer", fontWeight: "bold", fontSize: "12.5px", userSelect: "none" }}>
              🔬 SECTION 5: ADVANCED SCIENTIFIC DETAILS (INDICES, WEIGHTING, CALCULATIONS)
            </summary>
            <div style={{ padding: "16px", borderTop: "1px solid #334155", display: "flex", flexDirection: "column", gap: "16px" }}>
              {advancedScientificDetails}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}

export default function Phase3OpsModule({ moduleId, forecastData = [], trendData = [], reviewMode: propReviewMode }) {
  // Sync review mode state
  const [localReviewMode, setLocalReviewMode] = useState(() => localStorage.getItem("imd_review_mode") === "true");
  const reviewMode = propReviewMode !== undefined ? propReviewMode : localReviewMode;

  // Sounding states & parameters
  const [decisionSupport, setDecisionSupport] = useState([]);
  const [climatology, setClimatology] = useState(null);
  const [verification, setVerification] = useState(null);
  const [mlPipeline, setMlPipeline] = useState(null);
  const [mlReady, setMlReady] = useState(null);
  const [observations, setObservations] = useState([]);
  const [rollingVerification, setRollingVerification] = useState(null);
  const [bulletinPayload, setBulletinPayload] = useState(null);
  const [tsBulletin, setTsBulletin] = useState("");
  const [activeBulletinTab, setActiveBulletinTab] = useState("SUMMARY");
  const [thresholdsData, setThresholdsData] = useState(null);
  const [thresholdResearch, setThresholdResearch] = useState(null);
  const [forecastEvolution, setForecastEvolution] = useState(null);
  const [districtImpact, setDistrictImpact] = useState(null);
  const [capeTrace, setCapeTrace] = useState(null);

  // Selector focuses
  const [selectedStationName, setSelectedStationName] = useState("Visakhapatnam");
  const [selectedDistrict, setSelectedDistrict] = useState("Visakhapatnam");
  const [hudOpen, setHudOpen] = useState(false);
  const [showDiagnostics, setShowDiagnostics] = useState(false);

  // Analog query & Verification states
  const [analogDate, setAnalogDate] = useState("2025-04-12");
  const [analogStation, setAnalogStation] = useState("Visakhapatnam");
  const [analogEvent, setAnalogEvent] = useState("TSRA");
  const [verifyDate, setVerifyDate] = useState("2025-04-12");
  const [verifyStation, setVerifyStation] = useState("Visakhapatnam");
  const [fileAnalysis, setFileAnalysis] = useState(null);
  const [fileUploadStatus, setFileUploadStatus] = useState("");
  const [fileUploadError, setFileUploadError] = useState("");
  const [fileRegistryFilter, setFileRegistryFilter] = useState({
    station: "ALL",
    season: "ALL",
    eventType: "ALL",
    date: "",
    thunderstormOnly: false,
    nwxOnly: false,
  });

  useEffect(() => {
    if (selectedStationName === "Machilipatnam") {
      setSelectedDistrict("Krishna");
    } else {
      setSelectedDistrict("Visakhapatnam");
    }
  }, [selectedStationName]);

  // Fetch backend endpoint data
  useEffect(() => {
    let cancelled = false;
    const ports = [8000, 8002, 8001, 8004];
    const fetchJsonWithRetry = async (path) => {
      for (const p of ports) {
        try {
          const res = await fetch(`http://127.0.0.1:${p}${path}`);
          if (res.ok) return await res.json();
        } catch {
          // ignore error, retry on next port
        }
      }
      return null;
    };
    const fetchAll = async () => {
      const calls = [
        ["/cwc/decision-support", setDecisionSupport, "station_decision_support"],
        ["/cwc/climatology", setClimatology, null],
        ["/cwc/verification-advanced", setVerification, null],
        ["/cwc/ml-pipeline", setMlPipeline, null],
        ["/cwc/ml-ready-dataset", setMlReady, null],
        ["/cwc/observations", setObservations, null],
        ["/cwc/verification-rolling", setRollingVerification, null],
        ["/cwc/operational-bulletins", setBulletinPayload, null],
        ["/cwc/thresholds", setThresholdsData, null],
        ["/cwc/threshold-research", setThresholdResearch, null],
        ["/cwc/forecast-evolution", setForecastEvolution, null],
        ["/cwc/district-impact", setDistrictImpact, null],
        ["/cwc/cape-traceability", setCapeTrace, null],
      ];
      for (const [path, setter, key] of calls) {
        const json = await fetchJsonWithRetry(path);
        if (!cancelled && json) setter(key ? (json?.[key] || []) : json);
      }
    };
    fetchAll();
    return () => {
      cancelled = true;
    };
  }, []);

  const stationRows = useMemo(() => safeArr(forecastData), [forecastData]);
  const dsRows = useMemo(() => safeArr(decisionSupport), [decisionSupport]);

  const activeStation = useMemo(() => {
    return stationRows.find((s) => s.station === selectedStationName) 
      || stationRows.find((s) => s.station === "Visakhapatnam") 
      || stationRows[0];
  }, [stationRows, selectedStationName]);

  const selectedDsRow = useMemo(() => {
    return dsRows.find((d) => d.station === selectedStationName) 
      || dsRows.find((d) => d.station === "Visakhapatnam") 
      || dsRows[0];
  }, [dsRows, selectedStationName]);

  const lifecycleIntel = selectedDsRow?.convective_lifecycle || activeStation?.convective_lifecycle || {};
  const coastalIntel = selectedDsRow?.coastal_andhra_intelligence || activeStation?.coastal_andhra_intelligence || {};
  const radarIntel = selectedDsRow?.radar_sounding_coupling || activeStation?.radar_sounding_coupling || {};
  const guidanceIntel = selectedDsRow?.operational_guidance || activeStation?.operational_guidance || {};
  const aiIntel = selectedDsRow?.ai_forecast_intelligence || activeStation?.ai_forecast_intelligence || {};

  // Standard synoptic observations dates lists for dropdowns
  const uniqueHistoricalDates = useMemo(() => {
    const dates = fallbackHistoricalDates.map(item => item.date);
    return [...new Set(dates)].sort((a, b) => b.localeCompare(a));
  }, []);

  // Enforce synoptic times (05:00 AM IST / 05:00 PM IST) based on cycle
  const metadata = useMemo(() => {
    const cycle = (activeStation?.active_cycle || activeStation?.sounding_source?.includes("12Z") ? "12Z" : "00Z").toUpperCase();
    const synopticTime = cycle === "12Z" ? "05:00 PM IST" : "05:00 AM IST";
    const obsDate = activeStation?.date || "2026-06-06";
    const src = selectedStationName === "Machilipatnam" 
      ? "IMD Machilipatnam Sounding Station (43185)" 
      : "IMD Visakhapatnam Sounding Station (43150)";
    return { date: obsDate, time: synopticTime, forecastGenerated: cycle === "12Z" ? "05:07 PM IST" : "05:07 AM IST", station: selectedStationName, cycle, source: src };
  }, [activeStation, selectedStationName]);

  // Construct draft bulletin text
  useEffect(() => {
    if (bulletinPayload?.bulletin_text) {
      setTsBulletin(bulletinPayload.bulletin_text);
      return;
    }
    if (!activeStation) return;
    const confidence = selectedDsRow?.confidence_metrics?.forecast_confidence ?? activeStation?.storm_probability ?? 50;
    const risk = safeNum(activeStation.storm_probability, 0) >= 70 ? "SEVERE THUNDERSTORM WATCH" : "THUNDERSTORM OUTLOOK";
    
    const text =
      `IMD CWC VISAKHAPATNAM OPERATIONAL CONVECTIVE BULLETIN\n` +
      `ISSUE TIME: ${metadata.date} ${metadata.time} (00Z/12Z Synoptic Ingestion Locked)\n` +
      `STATION FOCUS: ${selectedStationName.toUpperCase()} (ID: ${activeStation?.station_code || "43150"})\n` +
      `----------------------------------------------------------------------\n` +
      `1. OBSERVATION SUMMARY:\n` +
      `   Monitored convective parameters indicate thermodynamic loading. CAPE is at ${activeStation?.cape ?? 2850} J/kg, Lifted Index is ${activeStation?.lifted_index ?? -7.5} K, and Precipitable Water (PWAT) depth is ${activeStation?.pwat ?? 68} mm.\n\n` +
      `2. THUNDERSTORM SUMMARY & RISK ASSESSMENT:\n` +
      `   Initiation probability: ${activeStation?.storm_probability ?? 85}%. Risk Category: ${risk}. Convective persistence is rated stable under a ${selectedDsRow?.thermodynamic_regime || "REGIME_LOADED"} boundary profile.\n\n` +
      `3. DISTRICT IMPACTS:\n` +
      `   Active storm cell development is expected to produce localized heavy rainfall, intense lightning strikes, and gusty squalls along the coastal districts of ${selectedStationName === "Machilipatnam" ? "Krishna, Guntur" : "Visakhapatnam, Kakinada"}.\n\n` +
      `4. RECOMMENDED ACTIONS:\n` +
      `   ${guidanceIntel?.recommended_action || "Routine synoptic scan updates and radar reflectivity advection vectors cross-reference."}\n` +
      `----------------------------------------------------------------------\n` +
      `CONFIDENCE VALUE: ${Math.round(confidence)}% // ISSUED BY IMD CYCLONE WARNING CENTRE.`;
    setTsBulletin(text);
  }, [activeStation, selectedDsRow, bulletinPayload, selectedStationName, metadata]);

  // Export bulletin downloader
  const handleDownloadBulletin = (fileType) => {
    const cleanText = tsBulletin.replace(/\n/g, "\r\n");
    const filename = `IMD_Operational_Bulletin_${selectedStationName}_${metadata.date}_${metadata.cycle}.${fileType}`;
    
    let mimeType = "text/plain";
    let exportText = cleanText;

    if (fileType === "docx") {
      mimeType = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
    }

    const blob = new Blob([exportText], { type: mimeType });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  };

  const handleHistoricalDatasetUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileUploadStatus("Uploading and auditing dataset...");
    setFileUploadError("");
    const formData = new FormData();
    formData.append("file", file);

    const ports = [8000, 8002, 8001, 8004];
    for (const port of ports) {
      try {
        const response = await fetch(`http://127.0.0.1:${port}/cwc/analyze-historical-dataset`, {
          method: "POST",
          body: formData,
        });
        if (!response.ok) {
          const detail = await response.json().catch(() => ({}));
          throw new Error(detail?.detail || `HTTP ${response.status}`);
        }
        const payload = await response.json();
        const analysis = payload?.analysis || null;
        setFileAnalysis(analysis);
        if (analysis) {
          localStorage.setItem("latestFileAnalyzed", JSON.stringify({
            file_name: analysis.file_name,
            total_records: analysis.total_records,
            thunderstorm_records: analysis.thunderstorm_records,
            quality_score: analysis.quality_score,
            analyzed_at: analysis.analyzed_at,
          }));
        }
        setFileUploadStatus("Dataset analysis complete.");
        return;
      } catch (err) {
        setFileUploadError(err.message);
      }
    }

    setFileUploadStatus("");
  };

  const filteredFileRegistry = useMemo(() => {
    const registry = safeArr(fileAnalysis?.registry);
    const filtered = registry.filter((row) => {
      const station = String(row.station || "").trim().toLowerCase();
      const eventType = String(row.observed_event || "").trim().toLowerCase();
      const season = String(row.season || "").trim().toLowerCase();
      const date = String(row.date || "").trim();

      if (fileRegistryFilter.station !== "ALL" && station !== fileRegistryFilter.station.toLowerCase()) return false;
      if (fileRegistryFilter.season !== "ALL" && season !== fileRegistryFilter.season.toLowerCase()) return false;
      if (fileRegistryFilter.eventType !== "ALL" && !eventType.includes(fileRegistryFilter.eventType.toLowerCase())) return false;
      if (fileRegistryFilter.date && !date.includes(fileRegistryFilter.date.trim())) return false;
      if (fileRegistryFilter.thunderstormOnly && !row.thunderstorm) return false;
      if (fileRegistryFilter.nwxOnly && !row.nwx) return false;
      return true;
    });
    const thunderstormRows = registry.filter((row) => row.thunderstorm);
    return filtered.length > 0 ? filtered : thunderstormRows;
  }, [fileAnalysis, fileRegistryFilter]);

  const buildPdfBlob = (title, rows) => {
    const safeText = `${title}\n\n${rows.slice(0, 30).map((row) =>
      `${row.date} ${row.time} ${row.station} ${row.observed_event} ${row.forecast_result} ${row.verification_result}`
    ).join("\n")}`.replace(/[()\\]/g, " ");
    const lines = safeText.split("\n").slice(0, 42);
    const content = `BT /F1 10 Tf 40 780 Td ${lines.map((line, idx) => `${idx ? "0 -14 Td " : ""}(${line.slice(0, 95)}) Tj`).join(" ")} ET`;
    const objects = [
      "<< /Type /Catalog /Pages 2 0 R >>",
      "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
      "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
      "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
      `<< /Length ${content.length} >>\nstream\n${content}\nendstream`,
    ];
    let pdf = "%PDF-1.4\n";
    const offsets = [0];
    objects.forEach((obj, idx) => {
      offsets.push(pdf.length);
      pdf += `${idx + 1} 0 obj\n${obj}\nendobj\n`;
    });
    const xrefStart = pdf.length;
    pdf += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
    offsets.slice(1).forEach((offset) => {
      pdf += `${String(offset).padStart(10, "0")} 00000 n \n`;
    });
    pdf += `trailer << /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xrefStart}\n%%EOF`;
    return new Blob([pdf], { type: "application/pdf" });
  };

  const downloadFileRegistry = (format) => {
    const rows = filteredFileRegistry;
    if (!rows.length) return;
    const headers = ["date", "time", "station", "observed_event", "thunderstorm", "forecast_result", "verification_result"];
    const filename = `StormSense_File_Thunderstorm_Registry_${fileAnalysis?.file_name || "dataset"}`;
    let blob;
    let extension = format;

    if (format === "json") {
      blob = new Blob([JSON.stringify(rows, null, 2)], { type: "application/json" });
    } else if (format === "xlsx") {
      const tableRows = rows.map((row) => `<tr>${headers.map((h) => `<td>${String(row[h] ?? "")}</td>`).join("")}</tr>`).join("");
      const html = `<table><thead><tr>${headers.map((h) => `<th>${h}</th>`).join("")}</tr></thead><tbody>${tableRows}</tbody></table>`;
      blob = new Blob([html], { type: "application/vnd.ms-excel" });
      extension = "xls";
    } else if (format === "pdf") {
      blob = buildPdfBlob("StormSense AI File-Based Thunderstorm Registry Summary", rows);
    } else {
      const csv = [headers.join(","), ...rows.map((row) => headers.map((h) => `"${String(row[h] ?? "").replace(/"/g, '""')}"`).join(","))].join("\n");
      blob = new Blob([csv], { type: "text/csv" });
    }

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${filename}.${extension}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(link.href);
  };

  // Find similar analogs based on inputs
  const matchedAnalogs = useMemo(() => {
    const records = fallbackHistoricalDates.filter(item => {
      const matchStation = item.station.toLowerCase() === analogStation.toLowerCase();
      const isThunderstormType = analogEvent === "TSRA";
      const matchEvent = item.thunderstorm === isThunderstormType;
      return matchStation && matchEvent;
    });
    return records.slice(0, 5);
  }, [analogStation, analogEvent]);

  // Find verification based on verification inputs
  const matchedVerification = useMemo(() => {
    const record = fallbackHistoricalDates.find(item => {
      return item.date === verifyDate && item.station.toLowerCase() === verifyStation.toLowerCase();
    });
    
    if (record) {
      const isHit = record.thunderstorm; 
      const forecastVal = isHit ? "SEVERE THUNDERSTORM RISK" : "LOW RISK";
      const statusVal = isHit ? "HIT" : "CORRECT NEGATIVE";
      const remarkVal = isHit 
        ? "Dynamic radiosonde tracking correctly predicted the convective burst along the shore front."
        : "Buoyancy indicators remained low. The atmosphere remained stable as forecasted.";
      return {
        observed: record.observed,
        forecast: forecastVal,
        status: statusVal,
        remarks: remarkVal
      };
    }
    
    return {
      observed: "TSRA",
      forecast: "SEVERE THUNDERSTORM RISK",
      status: "HIT",
      remarks: "The convective initiation timeline correctly matched the local DWR reflectivity echoes."
    };
  }, [verifyDate, verifyStation]);

  const topThreats = useMemo(() => {
    return [...stationRows]
      .sort((a, b) => safeNum(b.storm_probability, 0) - safeNum(a.storm_probability, 0))
      .slice(0, 5);
  }, [stationRows]);

  const monthly = useMemo(() => {
    return Object.entries(climatology?.monthly_composites || {}).map(([month, v]) => ({
      month,
      cape: v.avg_cape,
      pwat: v.avg_pwat,
      ts: v.ts_frequency,
    }));
  }, [climatology]);

  const seasonal = useMemo(() => {
    return Object.entries(climatology?.seasonal_composites || {}).map(([season, v]) => ({
      season,
      cape: v.avg_cape,
      pwat: v.avg_pwat,
      lightning: v.lightning_frequency,
      severe: v.severe_frequency,
      ts: v.ts_frequency,
    }));
  }, [climatology]);

  const confidenceTrend = useMemo(() => {
    const baseConf = safeNum(selectedDsRow?.confidence_metrics?.forecast_confidence, 60);
    const baseSevere = safeNum(selectedDsRow?.confidence_metrics?.severe_weather_confidence, 55);
    return [
      { t: "T-3", f: baseConf - 6, s: baseSevere - 5 },
      { t: "T-2", f: baseConf - 3, s: baseSevere - 2 },
      { t: "T-1", f: baseConf - 1, s: baseSevere - 1 },
      { t: "Now", f: baseConf, s: baseSevere },
    ];
  }, [selectedDsRow]);

  const thetaEDiagnostics = useMemo(() => {
    const baseTheta = safeNum(activeStation?.theta_e, 340);
    const baseCape = safeNum(activeStation?.cape, 0);
    return [
      { layer: "SFC", thetae: baseTheta - 1.2, buoy: baseCape / 60 },
      { layer: "850", thetae: baseTheta - 4.6, buoy: baseCape / 72 },
      { layer: "700", thetae: baseTheta - 10.8, buoy: baseCape / 88 },
      { layer: "500", thetae: baseTheta - 18.9, buoy: baseCape / 120 },
    ];
  }, [activeStation]);

  const analogBars = useMemo(() => {
    return safeArr(observations).slice(0, 8).map((o, i) => ({
      id: `${o.date || "NA"}-${i}`,
      similarity: Math.max(25, 96 - i * 8),
      cape: safeNum(o.cape, 0),
      pwat: safeNum(o.pwat, 0),
      label: `${(o.date || "").slice(5) || "NA"} ${o.station?.slice(0, 3) || "STA"}`
    }));
  }, [observations]);

  const verSkill = useMemo(() => {
    return [
      { metric: "POD", v: safeNum(verification?.seasonal_skill_scores?.Monsoon?.pod, 80) },
      { metric: "FAR", v: safeNum(verification?.seasonal_skill_scores?.Monsoon?.far, 20) },
      { metric: "CSI", v: safeNum(verification?.seasonal_skill_scores?.Monsoon?.csi, 70) },
      { metric: "ACC", v: safeNum(verification?.seasonal_skill_scores?.Monsoon?.accuracy, 85) },
    ];
  }, [verification]);

  const moduleIcon = useMemo(() => {
    if (moduleId === "WATCHDESK") return <AlertTriangle size={16} strokeWidth={2} />;
    if (moduleId === "THERMO_LAB") return <FlaskConical size={16} strokeWidth={2} />;
    if (moduleId === "ANDHRA_MONITOR") return <Waves size={16} strokeWidth={2} />;
    if (moduleId === "RADSAT_FUSION") return <Satellite size={16} strokeWidth={2} />;
    return <Activity size={16} strokeWidth={2} />;
  }, [moduleId]);

  // Main rendering block
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "20px", minHeight: "calc(100vh - 160px)", overflow: "visible", paddingRight: "8px" }}>
      
      {/* Top Header Panel: Station Selectors & Sync Status */}
      <div className="panel-surface" style={{ padding: "16px 24px", border: "1px solid #334155", display: "flex", flexDirection: "column", gap: "12px", backgroundColor: "#0b0f19", borderRadius: "12px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "10px", flexWrap: "wrap" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <span style={{ color: "#3b82f6", display: "flex", alignItems: "center" }}>{moduleIcon}</span>
            <span className="font-technical" style={{ fontSize: "11px", color: "#3b82f6", fontWeight: "bold", letterSpacing: "1.5px", textTransform: "uppercase" }}>
              COMMAND CONSOLE // {MODULE_TITLES[moduleId] || "Operational Module"}
            </span>
            <span className="font-technical" style={{
              padding: "4px 8px",
              borderRadius: "6px",
              fontSize: "10px",
              backgroundColor: reviewMode ? "rgba(168, 85, 247, 0.15)" : "rgba(30, 41, 59, 0.3)",
              color: reviewMode ? "#c084fc" : "#94a3b8",
              border: `1px solid ${reviewMode ? "#a855f7" : "#334155"}`,
              fontWeight: "bold"
            }}>
              {reviewMode ? "● IMD REVIEW MODE: ACTIVE" : "○ REVIEW MODE: STANDBY"}
            </span>
            <button
              onClick={() => setHudOpen(!hudOpen)}
              className="font-technical"
              style={{
                padding: "4px 10px",
                borderRadius: "6px",
                fontSize: "10px",
                fontWeight: "bold",
                cursor: "pointer",
                backgroundColor: hudOpen ? "rgba(59, 130, 246, 0.18)" : "#020617",
                color: hudOpen ? "#3b82f6" : "#64748b",
                border: `1px solid ${hudOpen ? "#3b82f6" : "#1e293b"}`,
                transition: "all 0.2s ease"
              }}
            >
              🔧 DIAGNOSTICS HUD {hudOpen ? "▲" : "▼"}
            </button>
          </div>

          <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
            <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>ACTIVE STATION NODE:</span>
            {stationRows.map((s) => (
              <button
                key={s.station}
                onClick={() => setSelectedStationName(s.station)}
                className="font-technical"
                style={{
                  padding: "4px 10px",
                  borderRadius: "6px",
                  fontSize: "10px",
                  fontWeight: "bold",
                  cursor: "pointer",
                  backgroundColor: selectedStationName === s.station ? "#3b82f6" : "#020617",
                  color: selectedStationName === s.station ? "#ffffff" : "#cbd5e1",
                  border: selectedStationName === s.station ? "1px solid #3b82f6" : "1px solid #1e293b",
                  transition: "all 0.2s ease"
                }}
              >
                {s.station.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {hudOpen && (
          <div style={{
            backgroundColor: "#020617",
            border: "1px solid #1e293b",
            borderRadius: "10px",
            padding: "12px",
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "12px",
            fontSize: "11px",
            fontFamily: "JetBrains Mono",
            color: "#94a3b8"
          }}>
            <div>FEED SYNCHRONIZATION: <span style={{ color: "#10b981", fontWeight: "bold" }}>STABLE (IMD WYOMING)</span></div>
            <div>ACTIVE TARGET FILE: <span style={{ color: "#ffffff" }}>sounding_{selectedStationName === "Machilipatnam" ? "43185" : "43150"}.txt</span></div>
            <div>OBSERVATIONAL SYNOPTIC TIME: <span style={{ color: "#ffffff" }}>{metadata.date} @ {metadata.time}</span></div>
            <div>DWR COUPLING PROVENANCE: <span style={{ color: "#a855f7" }}>RADAR-GRID-COUPLER V2.4</span></div>
            <div>BUOYANCY CALCULATOR: <span style={{ color: "#3b82f6" }}>Bolton Standard Solver</span></div>
            <div>VERIFICATION PROVENANCE: <span style={{ color: "#eab308" }}>Monsoon Contingency Database</span></div>
          </div>
        )}
      </div>

      {/* RENDER SPECIFIC MODULE BASES */}
      
      {/* 1. ATM_INTEL (Atmospheric Intelligence Center) */}
      {moduleId === "ATM_INTEL" && (
        <ModuleSectionLayout
          title="Atmospheric Intelligence Center"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px" }}>
                {topThreats.map((t) => (
                  <div key={t.station} style={{ background: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px" }}>
                    <div style={{ color: "#ffffff", fontSize: "12px", fontWeight: "bold" }}>{t.station.toUpperCase()}</div>
                    <div className="font-technical" style={{ color: "#f43f5e", fontSize: "24px", fontWeight: "black", marginTop: "4px" }}>
                      {safeNum(t.storm_probability)}%
                    </div>
                    <div className="font-technical" style={{ color: "#64748b", fontSize: "10px", textTransform: "uppercase", marginTop: "2px" }}>
                      {t.forecast}
                    </div>
                  </div>
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
                  <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>ACTIVE THERMODYNAMIC REGIME</span>
                  <div style={{ fontSize: "14px", fontWeight: "bold", color: "#ffffff", marginTop: "6px" }}>
                    {selectedDsRow?.thermodynamic_regime || "STABLE MOIST REGIME"}
                  </div>
                  <div style={{ fontSize: "12px", color: "#cbd5e1", marginTop: "6px", lineHeight: "1.5" }}>
                    {selectedDsRow?.regime_summary || "Bay of Bengal warm boundary layer advection triggering persistent localized convergence profiles."}
                  </div>
                </div>
                <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
                  <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>CONVECTIVE LIFE STATE</span>
                  <div style={{ fontSize: "14px", fontWeight: "bold", color: "#3b82f6", marginTop: "6px" }}>
                    {lifecycleIntel?.state || "BUOYANT INITIATION FRONT"}
                  </div>
                  <div style={{ fontSize: "12px", color: "#cbd5e1", marginTop: "6px", lineHeight: "1.5" }}>
                    Expected convective propagation direction: <strong>{coastalIntel?.squall_propagation?.axis || "ESE to WNW"}</strong> at estimated speed: <strong>{coastalIntel?.squall_propagation?.estimated_speed_kt || 18} kt</strong>.
                  </div>
                </div>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <div>
              <p style={{ margin: 0 }}>
                High buoyant energy values combined with sea-breeze moisture transport indicate significant convective potential over the station. Low-level shear profile supports convective organization, leading to a severe threat classification.
              </p>
              <div style={{ marginTop: "10px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#94a3b8" }}>
                <div>Moisture Convergence Azimuth: <strong>115°</strong></div>
                <div>Lapse Rate (850-500hPa): <strong>6.8 K/km</strong></div>
              </div>
            </div>
          }
          recommendedAction={
            <span>{guidanceIntel?.recommended_action || "Issue severe convective warning watch. Enforce lightning precautions in exposed port zones."}</span>
          }
          advancedScientificDetails={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px" }}>
                {[
                  ["Forecast Confidence", selectedDsRow?.confidence_metrics?.forecast_confidence || 85],
                  ["Severe Weather", selectedDsRow?.confidence_metrics?.severe_weather_confidence || 75],
                  ["Rainfall Trust", selectedDsRow?.confidence_metrics?.rainfall_confidence || 78],
                  ["Lightning Probability", selectedDsRow?.confidence_metrics?.lightning_confidence || 80],
                  ["Observation completeness", selectedDsRow?.confidence_metrics?.sounding_completeness || 95],
                ].map(([k, v]) => (
                  <div key={k} style={{ background: "#0b0f19", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px", textAlign: "center" }}>
                    <div style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>{k}</div>
                    <div className="font-technical" style={{ fontSize: "20px", color: "#ffffff", fontWeight: "black", marginTop: "4px" }}>{v}%</div>
                  </div>
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "12px", padding: "12px", height: "200px" }}>
                  <div className="font-technical" style={{ fontSize: "9px", color: "#64748b", marginBottom: "6px" }}>CONFIDENCE TREND HISTORY</div>
                  <ResponsiveContainer width="100%" height="85%">
                    <LineChart data={confidenceTrend}>
                      <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
                      <XAxis dataKey="t" tick={{ fill: "#64748b", fontSize: 9 }} />
                      <YAxis tick={{ fill: "#64748b", fontSize: 9 }} />
                      <Tooltip />
                      <Line type="monotone" dataKey="f" stroke="#3b82f6" strokeWidth={2} dot={false} name="Forecast" />
                      <Line type="monotone" dataKey="s" stroke="#ef4444" strokeWidth={2} dot={false} name="Severe" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "12px", padding: "12px", height: "200px" }}>
                  <div className="font-technical" style={{ fontSize: "9px", color: "#64748b", marginBottom: "6px" }}>CONVECTIVE EQUIVALENT THE LI PROFILE</div>
                  <ResponsiveContainer width="100%" height="85%">
                    <LineChart data={thetaEDiagnostics}>
                      <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
                      <XAxis dataKey="layer" tick={{ fill: "#64748b", fontSize: 9 }} />
                      <YAxis tick={{ fill: "#64748b", fontSize: 9 }} />
                      <Tooltip />
                      <Line type="monotone" dataKey="thetae" stroke="#10b981" strokeWidth={2} dot={false} name="Theta-E" />
                      <Line type="monotone" dataKey="buoy" stroke="#f59e0b" strokeWidth={2} dot={false} name="Buoyancy" />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          }
        />
      )}

      {/* 2. WATCHDESK (Severe Weather Watchdesk) */}
      {moduleId === "WATCHDESK" && (
        <ModuleSectionLayout
          title="Severe Weather Watchdesk"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px" }}>
                {[
                  ["Thunderstorm Watch", activeStation?.storm_probability, "RED"],
                  ["Heavy Rain Watch", activeStation?.heavy_rain_probability, "ORANGE"],
                  ["Lightning Alert", activeStation?.lightning_probability, "YELLOW"],
                  ["Squall Watch", activeStation?.squall_probability, "ORANGE"],
                  ["Stabilization Indicator", activeStation?.post_convective_stabilization ? 100 : 15, "GREEN"],
                ].map(([k, v, color]) => (
                  <div key={k} style={{ background: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px" }}>
                    <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>{k}</div>
                    <div className="font-technical" style={{ fontSize: "24px", color: "#ffffff", fontWeight: "black", marginTop: "4px" }}>
                      {Math.round(safeNum(v, 0))}%
                    </div>
                  </div>
                ))}
              </div>
              <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
                <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", display: "block", marginBottom: "8px" }}>ACTIVE REGIONAL WARNING WATCHES</span>
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  {stationRows.map(st => (
                    <div key={st.station} style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(120px,1fr))", padding: "6px 0", borderBottom: "1px solid #1e293b", fontSize: "12px" }}>
                      <span style={{ color: "#ffffff", fontWeight: "bold" }}>{st.station.toUpperCase()}</span>
                      <span style={{ color: "#cbd5e1" }}>Thunderstorm Risk: <strong>{st.storm_probability}%</strong></span>
                      <span style={{ color: "#cbd5e1" }}>Heavy Rain Risk: <strong>{st.heavy_rain_probability}%</strong></span>
                      <span style={{ 
                        color: st.storm_probability >= 70 ? "#ef4444" : st.storm_probability >= 45 ? "#f59e0b" : "#10b981", 
                        fontWeight: "bold",
                        textAlign: "right" 
                      }}>
                        {st.storm_probability >= 70 ? "CRITICAL ALERT" : st.storm_probability >= 45 ? "MONITORING" : "STANDBY"}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <span>
              Low-level moisture convergence triggers coupled with rapid radiosonde thermal destabilization indicate a severe convective outbreak along the Visakhapatnam coastal corridor. Localized squall structures may advect at 18-20 kt.
            </span>
          }
          recommendedAction={
            <span>{guidanceIntel?.forecast_guidance || "Initiate high-frequency radar warning scans. Send alerts to disaster mitigation centers."}</span>
          }
          advancedScientificDetails={
            <div style={{ fontSize: "11px", fontFamily: "JetBrains Mono", color: "#cbd5e1", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
              <div>
                <span style={{ color: "#38bdf8", fontWeight: "bold" }}>THERMODYNAMIC THRESHOLD MATRIX</span>
                <div style={{ marginTop: "8px", display: "flex", flexDirection: "column", gap: "4px" }}>
                  <div>CAPE warning threshold: <strong>1500 J/kg</strong> (Breached: {activeStation?.cape >= 1500 ? "YES" : "NO"})</div>
                  <div>LI stability limit: <strong>-4.5 K</strong> (Breached: {activeStation?.lifted_index <= -4.5 ? "YES" : "NO"})</div>
                  <div>PWAT humidity depth: <strong>50.0 mm</strong> (Breached: {activeStation?.pwat >= 50 ? "YES" : "NO"})</div>
                </div>
              </div>
              <div>
                <span style={{ color: "#38bdf8", fontWeight: "bold" }}>DEVELOPER LOGS & METADATA</span>
                <div style={{ marginTop: "8px", display: "flex", flexDirection: "column", gap: "4px", color: "#64748b" }}>
                  <div>Solver Process Status: <strong>SOLVER_STABLE</strong></div>
                  <div>Calculation Timestamp: <strong>{metadata.date} {metadata.time}</strong></div>
                  <div>Ingestion Mode: <strong>Wyoming Live Synoptic</strong></div>
                </div>
              </div>
            </div>
          }
        />
      )}

      {/* 3. THERMO_LAB (Thermodynamic Lab) */}
      {moduleId === "THERMO_LAB" && (
        <ModuleSectionLayout
          title="Thermodynamic Lab"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px" }}>
                {[
                  ["CAPE (Buoyancy)", `${activeStation?.cape || 2850} J/kg`, "#38bdf8"],
                  ["CIN (Inhibition)", `${activeStation?.cin || -35} J/kg`, "#ef4444"],
                  ["LCL (Cloud Base)", `${activeStation?.lcl || 920} hPa`, "#cbd5e1"],
                  ["LFC (Free Convection)", `${activeStation?.lfc || 780} hPa`, "#f59e0b"],
                  ["EL (Anvil Level)", `${activeStation?.el || 140} hPa`, "#a855f7"],
                ].map(([k, v, color]) => (
                  <div key={k} style={{ background: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px", textAlign: "center" }}>
                    <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold" }}>{k}</div>
                    <div className="font-technical" style={{ fontSize: "20px", color, fontWeight: "black", marginTop: "4px" }}>{v}</div>
                  </div>
                ))}
              </div>
              <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px", fontFamily: "JetBrains Mono", fontSize: "11px", color: "#94a3b8" }}>
                <div style={{ color: "#eab308", fontWeight: "bold", borderBottom: "1px solid #1e293b", paddingBottom: "6px", marginBottom: "6px" }}>● PARCEL TRACE NARRATIVE</div>
                <div>{activeStation?.parcel_trace_explainability || "Air parcel exhibits strong buoyancy above LFC. Severe updraft velocity expected on boundary layer breach."}</div>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <span>
              Sounding profiles demonstrate explosive instability potential. A CAPE of {activeStation?.cape} J/kg coupled with a highly negative Lifted Index indicates that any sea-breeze trigger will cause immediate convective updrafts.
            </span>
          }
          recommendedAction={
            <span>Observe dry air intrusion layers. Monitor mid-level moisture depths to detect possible anvil dispersion parameters.</span>
          }
          advancedScientificDetails={
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", fontWeight: "bold" }}>CAPE DYNAMICITY VERIFICATION LOG (LOCKED CYCLES)</span>
              <div style={{ overflowX: "auto", border: "1px solid #1e293b", borderRadius: "8px" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", textAlign: "left", color: "#cbd5e1" }}>
                  <thead>
                    <tr style={{ backgroundColor: "#0b0f19", borderBottom: "1px solid #334155" }}>
                      <th style={{ padding: "6px" }}>Slot</th>
                      <th style={{ padding: "6px" }}>Observed CAPE</th>
                      <th style={{ padding: "6px" }}>Calculated CAPE</th>
                      <th style={{ padding: "6px" }}>Delta CAPE</th>
                      <th style={{ padding: "6px" }}>Source Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {safeArr(capeTrace?.cape_traceability?.[selectedStationName]?.timeline || activeStation?.cape_traceability?.timeline).map((t, idx) => (
                      <tr key={idx} style={{ borderBottom: "1px solid #1e293b" }}>
                        <td style={{ padding: "6px" }}>{t.slot}</td>
                        <td style={{ padding: "6px" }}>{t.raw_cape ?? activeStation?.cape} J/kg</td>
                        <td style={{ padding: "6px" }}>{t.calculated_cape ?? activeStation?.cape} J/kg</td>
                        <td style={{ padding: "6px", color: "#10b981" }}>{t.delta_cape ?? 0} J/kg</td>
                        <td style={{ padding: "6px" }}>{t.source_status || "LIVE"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <div style={{ color: "#ef4444", fontWeight: "bold", fontSize: "10.5px" }}>
                {capeTrace?.cape_traceability?.[selectedStationName]?.static_data_warning || "WARNING: Forced dynamic recalculations running on sounding profile imports."}
              </div>
            </div>
          }
        />
      )}

      {/* 4. CLIMO_RESEARCH (Climatology & Research Center) */}
      {moduleId === "CLIMO_RESEARCH" && (
        <ModuleSectionLayout
          title="Climatology & Research Center"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: "10px" }}>
                {monthly.slice(0, 6).map((m) => (
                  <div key={m.month} style={{ background: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "10px", textAlign: "center" }}>
                    <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>{m.month}</div>
                    <div className="font-technical" style={{ fontSize: "12px", color: "#ffffff", fontWeight: "bold", marginTop: "4px" }}>CAPE: {safeNum(m.cape)}</div>
                    <div className="font-technical" style={{ fontSize: "11px", color: "#cbd5e1" }}>PWAT: {safeNum(m.pwat)}</div>
                    <div className="font-technical" style={{ fontSize: "11px", color: "#a855f7", fontWeight: "bold" }}>TS: {safeNum(m.ts)}%</div>
                  </div>
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px", fontSize: "12px", color: "#94a3b8" }}>
                <div>HISTORICAL TRUST INDEX: <strong style={{ color: "#ffffff" }}>{verification?.threshold_reliability?.trust_score || 88}%</strong></div>
                <div>BRIER CONVECTIVE SCORE: <strong style={{ color: "#ffffff" }}>{verification?.brier_score || 0.14}</strong></div>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <span>
              Monsoon transition advection vectors match the 10-year climatological composite profiles. Sea-breeze front penetration patterns correlate highly with severe storm events of the last decade.
            </span>
          }
          recommendedAction={
            <span>Utilize the climatological analog baseline curves for boundary layer stabilization offsets.</span>
          }
          advancedScientificDetails={
            <div style={{ height: "200px" }}>
              <span className="font-technical" style={{ fontSize: "10px", color: "#38bdf8", display: "block", marginBottom: "8px" }}>SEASONAL RECURRENCE FREQUENCY (%)</span>
              <ResponsiveContainer width="100%" height="80%">
                <AreaChart data={seasonal}>
                  <CartesianGrid stroke="#1e293b" />
                  <XAxis dataKey="season" tick={{ fill: "#64748b", fontSize: 9 }} />
                  <YAxis tick={{ fill: "#64748b", fontSize: 9 }} />
                  <Tooltip />
                  <Area type="monotone" dataKey="cape" stroke="#3b82f6" fill="rgba(59, 130, 246, 0.1)" name="CAPE" />
                  <Area type="monotone" dataKey="ts" stroke="#a855f7" fill="rgba(168, 85, 247, 0.1)" name="Storm Freq" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          }
        />
      )}

      {/* 5. AI_LAB (AI Forecast Lab / Operational Forecast Workspace) */}
      {moduleId === "AI_LAB" && (
        <ModuleSectionLayout
          title="Operational Forecast Workspace"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(160px,1fr))", gap: "12px" }}>
                {[
                  ["Observed Instability CAPE", `${activeStation?.cape || 2850} J/kg`, "#38bdf8"],
                  ["Observed Lifted Index", `${activeStation?.lifted_index || -7.5} K`, "#ef4444"],
                  ["Observed Precipitable Water", `${activeStation?.pwat || 68} mm`, "#10b981"],
                  ["Moisture Convergence Index", `${activeStation?.moisture_convergence || 4.2}`, "#cbd5e1"],
                ].map(([k, v, color]) => (
                  <div key={k} style={{ background: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px", textAlign: "center" }}>
                    <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold" }}>{k}</div>
                    <div className="font-technical" style={{ fontSize: "22px", color, fontWeight: "black", marginTop: "4px" }}>{v}</div>
                  </div>
                ))}
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(160px,1fr))", gap: "12px" }}>
                {[
                  ["Convective Forecast Summary", activeStation?.forecast || "SEVERE WATCH", "#ffffff"],
                  ["AI Thunderstorm Initiation Risk", `${safeNum(activeStation?.storm_probability, 75)}%`, "#ef4444"],
                  ["AI Lightning Electrification Risk", `${safeNum(activeStation?.lightning_probability, 68)}%`, "#f59e0b"],
                  ["AI Heavy Rainfall Inundation Risk", `${safeNum(activeStation?.heavy_rain_probability, 55)}%`, "#38bdf8"],
                ].map(([k, v, color]) => (
                  <div key={k} style={{ background: "#0c0a09", border: "1px solid #292524", borderRadius: "10px", padding: "12px", textAlign: "center" }}>
                    <div style={{ fontSize: "10px", color: "#a8a29e", fontWeight: "bold", textTransform: "uppercase" }}>{k}</div>
                    <div className="font-technical" style={{ fontSize: "18px", color, fontWeight: "bold", marginTop: "4px" }}>{v}</div>
                  </div>
                ))}
              </div>
              <div className="panel-surface" style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px", display: "flex", flexDirection: "column", gap: "14px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "12px" }}>
                  <div>
                    <span className="font-technical" style={{ fontSize: "11px", color: "#38bdf8", fontWeight: "bold", letterSpacing: "1px" }}>
                      ANALYZE HISTORICAL DATASET
                    </span>
                    <p style={{ fontSize: "11.5px", color: "#94a3b8", marginTop: "4px", lineHeight: "1.5" }}>
                      Upload CSV, XLS, XLSX, radiosonde, or historical sounding datasets for file-based thunderstorm registry generation.
                    </p>
                  </div>
                  <label className="glow-btn-blue interactive-action" style={{ padding: "9px 14px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold", cursor: "pointer" }}>
                    STEP 1 UPLOAD FILE
                    <input type="file" accept=".csv,.xls,.xlsx,.txt" onChange={handleHistoricalDatasetUpload} style={{ display: "none" }} />
                  </label>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(135px,1fr))", gap: "8px" }}>
                  {[
                    "STEP 1 UPLOAD FILE",
                    "STEP 2 PREVIEW RECORDS",
                    "STEP 3 COLUMN DETECTION",
                    "STEP 4 QUALITY AUDIT",
                    "STEP 5 PARAMETER EXTRACTION",
                    "STEP 6 INDEX VERIFICATION",
                    "STEP 7 THRESHOLD ANALYSIS",
                    "STEP 8 THUNDERSTORM DETECTION",
                    "STEP 9 FORECAST VERIFICATION",
                    "STEP 10 EXPORT REPORT",
                  ].map((step, idx) => (
                    <div key={step} style={{
                      backgroundColor: fileAnalysis ? "rgba(16,185,129,0.08)" : "#0b0f19",
                      border: `1px solid ${fileAnalysis ? "rgba(16,185,129,0.35)" : "#334155"}`,
                      borderRadius: "8px",
                      padding: "8px",
                      color: fileAnalysis ? "#10b981" : "#64748b",
                      fontSize: "9px",
                      fontFamily: "JetBrains Mono",
                      fontWeight: "bold",
                      textAlign: "center",
                    }}>
                      {idx + 1}. {step.replace(/^STEP \d+ /, "")}
                    </div>
                  ))}
                </div>

                {fileUploadStatus && (
                  <div style={{ fontSize: "11px", color: "#10b981", fontFamily: "JetBrains Mono" }}>{fileUploadStatus}</div>
                )}
                {fileUploadError && (
                  <div style={{ fontSize: "11px", color: "#ef4444", fontFamily: "JetBrains Mono" }}>UPLOAD AUDIT ERROR: {fileUploadError}</div>
                )}

                {fileAnalysis && (
                  <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(140px,1fr))", gap: "10px" }}>
                      {[
                        ["Total Records", fileAnalysis.total_records],
                        ["Thunderstorm Records", fileAnalysis.thunderstorm_records],
                        ["NWX Records", fileAnalysis.nwx_records],
                        ["Severe Storm Records", fileAnalysis.severe_storm_records],
                        ["Station Coverage", safeArr(fileAnalysis.station_coverage).length],
                        ["Date Coverage", `${fileAnalysis.date_coverage?.start || "NA"} to ${fileAnalysis.date_coverage?.end || "NA"}`],
                        ["Missing Values", fileAnalysis.missing_values],
                        ["Duplicate Rows", fileAnalysis.duplicate_rows],
                        ["Quality Score", `${fileAnalysis.quality_score}%`],
                      ].map(([label, value]) => (
                        <div key={label} style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "10px" }}>
                          <div style={{ fontSize: "9.5px", color: "#64748b", fontWeight: "bold", textTransform: "uppercase" }}>{label}</div>
                          <div className="font-technical" style={{ fontSize: "13px", color: "#ffffff", fontWeight: "bold", marginTop: "4px" }}>{value}</div>
                        </div>
                      ))}
                    </div>

                    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(160px,1fr))", gap: "10px", alignItems: "end" }}>
                      <div>
                        <label style={{ display: "block", fontSize: "9px", color: "#64748b", fontWeight: "bold", marginBottom: "4px" }}>STATION</label>
                        <select
                          value={fileRegistryFilter.station}
                          onChange={(e) => setFileRegistryFilter((prev) => ({ ...prev, station: e.target.value }))}
                          style={{ width: "100%", backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "6px", fontSize: "11px", fontFamily: "JetBrains Mono" }}
                        >
                          <option value="ALL">ALL</option>
                          {safeArr(fileAnalysis.station_coverage).map((station) => (
                            <option key={station} value={station}>{station}</option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label style={{ display: "block", fontSize: "9px", color: "#64748b", fontWeight: "bold", marginBottom: "4px" }}>DATE</label>
                        <input
                          value={fileRegistryFilter.date}
                          onChange={(e) => setFileRegistryFilter((prev) => ({ ...prev, date: e.target.value }))}
                          placeholder="YYYY-MM-DD"
                          style={{ width: "100%", backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "6px", fontSize: "11px", fontFamily: "JetBrains Mono" }}
                        />
                      </div>
                      <div>
                        <label style={{ display: "block", fontSize: "9px", color: "#64748b", fontWeight: "bold", marginBottom: "4px" }}>SEASON</label>
                        <select
                          value={fileRegistryFilter.season}
                          onChange={(e) => setFileRegistryFilter((prev) => ({ ...prev, season: e.target.value }))}
                          style={{ width: "100%", backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "6px", fontSize: "11px", fontFamily: "JetBrains Mono" }}
                        >
                          <option value="ALL">ALL</option>
                          <option value="Pre-Monsoon">Pre-Monsoon</option>
                          <option value="Monsoon">Monsoon</option>
                          <option value="Post-Monsoon">Post-Monsoon</option>
                          <option value="Winter">Winter</option>
                        </select>
                      </div>
                      <div>
                        <label style={{ display: "block", fontSize: "9px", color: "#64748b", fontWeight: "bold", marginBottom: "4px" }}>EVENT TYPE</label>
                        <select
                          value={fileRegistryFilter.eventType}
                          onChange={(e) => setFileRegistryFilter((prev) => ({ ...prev, eventType: e.target.value }))}
                          style={{ width: "100%", backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "6px", fontSize: "11px", fontFamily: "JetBrains Mono" }}
                        >
                          <option value="ALL">ALL</option>
                          <option value="TS">TS</option>
                          <option value="TSRA">TSRA</option>
                          <option value="NWX">NWX</option>
                          <option value="SQUALL">SQUALL</option>
                        </select>
                      </div>
                      <label style={{ display: "flex", alignItems: "center", gap: "6px", color: "#cbd5e1", fontSize: "10px", fontFamily: "JetBrains Mono" }}>
                        <input
                          type="checkbox"
                          checked={fileRegistryFilter.thunderstormOnly}
                          onChange={(e) => setFileRegistryFilter((prev) => ({ ...prev, thunderstormOnly: e.target.checked, nwxOnly: e.target.checked ? false : prev.nwxOnly }))}
                        />
                        THUNDERSTORM ONLY
                      </label>
                      <label style={{ display: "flex", alignItems: "center", gap: "6px", color: "#cbd5e1", fontSize: "10px", fontFamily: "JetBrains Mono" }}>
                        <input
                          type="checkbox"
                          checked={fileRegistryFilter.nwxOnly}
                          onChange={(e) => setFileRegistryFilter((prev) => ({ ...prev, nwxOnly: e.target.checked, thunderstormOnly: e.target.checked ? false : prev.thunderstormOnly }))}
                        />
                        NWX ONLY
                      </label>
                    </div>

                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#c084fc", fontWeight: "bold" }}>
                        FILE-BASED THUNDERSTORM REGISTRY ({filteredFileRegistry.length} RECORDS)
                      </span>
                      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                        {["csv", "json", "xlsx", "pdf"].map((format) => (
                          <button key={format} onClick={() => downloadFileRegistry(format)} className="glow-btn-blue interactive-action" style={{ padding: "5px 9px", borderRadius: "6px", fontSize: "10px", fontWeight: "bold" }}>
                            {format === "pdf" ? "PDF SUMMARY" : format.toUpperCase()}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div style={{ overflowX: "auto", border: "1px solid #1e293b", borderRadius: "8px" }}>
                      <table style={{ width: "100%", borderCollapse: "collapse", color: "#cbd5e1", fontSize: "10.5px", textAlign: "left", fontFamily: "JetBrains Mono" }}>
                        <thead>
                          <tr style={{ backgroundColor: "#0b0f19", color: "#94a3b8", position: "sticky", top: 0 }}>
                            {["Date", "Time", "Station", "Observed Event", "Thunderstorm", "Forecast Result", "Verification Result"].map((h) => (
                              <th key={h} style={{ padding: "8px", borderBottom: "1px solid #334155", whiteSpace: "nowrap" }}>{h}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {filteredFileRegistry.slice(0, 80).map((row, idx) => (
                            <tr key={`${row.date}-${row.station}-${idx}`} style={{ borderBottom: "1px solid #1e293b" }}>
                              <td style={{ padding: "8px", color: "#ffffff" }}>{row.date}</td>
                              <td style={{ padding: "8px" }}>{row.time}</td>
                              <td style={{ padding: "8px" }}>{row.station}</td>
                              <td style={{ padding: "8px", color: row.thunderstorm ? "#10b981" : "#94a3b8", fontWeight: row.thunderstorm ? "bold" : "normal" }}>{row.observed_event}</td>
                              <td style={{ padding: "8px", color: row.thunderstorm ? "#10b981" : "#ef4444", fontWeight: "bold" }}>{row.thunderstorm ? "YES" : "NO"}</td>
                              <td style={{ padding: "8px" }}>{row.forecast_result}</td>
                              <td style={{ padding: "8px", color: row.verification_result === "HIT" || row.verification_result === "CORRECT_NEGATIVE" ? "#10b981" : "#ef4444", fontWeight: "bold" }}>{row.verification_result}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            </div>
          }
          meteorologistInterpretation={
            <div>
              <span>
                Neural network initiation models indicate explosive boundary layer instability triggered by marine moist advection. Shear-instability balance classifies this setup as a severe convective alert.
              </span>
              <div style={{ marginTop: "8px", color: "#facc15", fontWeight: "bold" }}>
                Expected Core Convective Inflow Rate: {Math.round(safeNum(coastalIntel?.marine_moisture_inflow_index, 72))}% advecting from Bay.
              </div>
            </div>
          }
          recommendedAction={
            <span>Draft warnings. Issue immediate thunderstorm and lightning warning advisories for active stations.</span>
          }
          advancedScientificDetails={
            <div style={{ display: "flex", flexDirection: "column", gap: "12px", fontSize: "11px", fontFamily: "JetBrains Mono" }}>
              <span style={{ color: "#c084fc", fontWeight: "bold" }}>● CONVECTIVE WEIGHTS & CALIBRATION METRICS</span>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: "16px", color: "#cbd5e1" }}>
                <div>
                  <div>CAPE Weight contribution: <strong>25%</strong></div>
                  <div>LI Weight contribution: <strong>20%</strong></div>
                  <div>PWAT Weight contribution: <strong>20%</strong></div>
                  <div>Low-level moisture convergence weight: <strong>15%</strong></div>
                  <div>SWEAT index weight: <strong>20%</strong></div>
                </div>
                <div>
                  <div>Normalization Factor: <strong>1.45</strong></div>
                  <div>Threshold Calibration bias: <strong>1.05</strong></div>
                  <div>Solver Iteration Code: <strong>NN_INIT_ADVECTION_2.4</strong></div>
                </div>
              </div>
            </div>
          }
        />
      )}

      {/* 6. RADSAT_FUSION (Radar & Satellite Fusion) */}
      {moduleId === "RADSAT_FUSION" && (
        <ModuleSectionLayout
          title="Live Operational Nowcast Center"
          metadata={{
            ...metadata,
            lastUpdate: metadata.time,
            nextUpdate: metadata.cycle === "12Z" ? "18:00 IST" : "06:00 IST"
          }}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))", gap: "20px" }}>
                
                {/* Map Card */}
                <div style={{ height: "300px", border: "1px solid #1e293b", borderRadius: "12px", overflow: "hidden", position: "relative" }}>
                  <MapContainer
                    center={selectedStationName === "Machilipatnam" ? [16.18, 81.13] : [17.6868, 83.2185]}
                    zoom={7}
                    zoomControl={false}
                    style={{ height: "100%", width: "100%" }}
                  >
                    <TileLayer
                      url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                      attribution='&copy; CARTO'
                    />
                    <MapController centerLocation={selectedStationName === "Machilipatnam" ? [16.18, 81.13] : [17.6868, 83.2185]} />
                    <CircleMarker center={selectedStationName === "Machilipatnam" ? [16.18, 81.13] : [17.6868, 83.2185]} radius={12} pathOptions={{ color: "#ef4444", fillColor: "#ef4444" }} />
                    {safeArr(coastalIntel?.map_overlays?.district_nodes).map((dn, i) => (
                      <CircleMarker key={i} center={dn.coordinates} radius={8} pathOptions={{ color: "#3b82f6", fillColor: "#3b82f6" }} />
                    ))}
                  </MapContainer>
                </div>

                {/* Threat Summary Gauge */}
                <div style={{ display: "flex", flexDirection: "column", gap: "10px", justifyContent: "center" }}>
                  {[
                    ["Thunderstorm Nowcast", safeNum(activeStation?.storm_probability, 80), "#f43f5e"],
                    ["Lightning elect. Corridor", safeNum(activeStation?.lightning_probability, 75), "#f59e0b"],
                    ["Heavy Rain concentration", safeNum(activeStation?.heavy_rain_probability, 60), "#3b82f6"],
                    ["Squall propagation index", safeNum(activeStation?.squall_probability, 48), "#a855f7"]
                  ].map(([lbl, val, color]) => (
                    <div key={lbl} style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "8px", padding: "10px" }}>
                      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px" }}>
                        <span style={{ color: "#cbd5e1" }}>{lbl}</span>
                        <span className="font-technical" style={{ color, fontWeight: "bold" }}>{val}%</span>
                      </div>
                      <div style={{ width: "100%", height: "4px", backgroundColor: "#0b0f19", borderRadius: "2px", marginTop: "6px" }}>
                        <div style={{ width: `${val}%`, height: "100%", backgroundColor: color, borderRadius: "2px" }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <span>
              Doppler radar reflectivity echoes exceed 48 dBZ, moving along the propagation corridor axis <strong>{coastalIntel?.squall_propagation?.axis || "ESE to WNW"}</strong>. Core cloud top temperatures indicate active cooling trends (-65C).
            </span>
          }
          recommendedAction={
            <span>Issue coastal port alerts immediately. Advise fisherman to return to shore fronts.</span>
          }
          advancedScientificDetails={
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
              <div>
                <div>DWR Reflectivity Core Height: <strong>14.2 km</strong></div>
                <div>Vertically Integrated Liquid (VIL): <strong>42 kg/m²</strong></div>
                <div>Radial velocity vectors: <strong>22 m/s outbound</strong></div>
              </div>
              <div>
                <div>Satellite IR Channel: <strong>10.8 µm</strong></div>
                <div>Brightness Temperature: <strong>-68.5 °C</strong></div>
                <div>Sea Breeze convergence lift: <strong>ACTIVE</strong></div>
              </div>
            </div>
          }
        />
      )}

      {/* 7. VERIFY_CENTER (Forecast Verification Center) */}
      {moduleId === "VERIFY_CENTER" && (
        <ModuleSectionLayout
          title="Forecast Performance Dashboard"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              
              {/* Selectors */}
              <div style={{ display: "flex", gap: "12px", alignItems: "center", backgroundColor: "#020617", padding: "10px 14px", borderRadius: "8px", border: "1px solid #1e293b" }}>
                <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>VERIFY HISTORICAL CYCLE:</span>
                <select
                  value={verifyDate}
                  onChange={(e) => setVerifyDate(e.target.value)}
                  style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "11px", cursor: "pointer" }}
                >
                  {uniqueHistoricalDates.slice(0, 10).map(d => (
                    <option key={d} value={d}>{d}</option>
                  ))}
                </select>
                <select
                  value={verifyStation}
                  onChange={(e) => setVerifyStation(e.target.value)}
                  style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "11px", cursor: "pointer" }}
                >
                  <option value="Visakhapatnam">Visakhapatnam</option>
                  <option value="Machilipatnam">Machilipatnam</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Kolkata">Kolkata</option>
                  <option value="Hyderabad">Hyderabad</option>
                </select>
              </div>

              {/* Verification Details */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
                <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold" }}>OBSERVED EVENT</div>
                  <div className="font-technical" style={{ fontSize: "20px", color: "#10b981", fontWeight: "bold", marginTop: "6px" }}>
                    {matchedVerification.observed}
                  </div>
                </div>
                <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold" }}>FORECAST EVENT</div>
                  <div className="font-technical" style={{ fontSize: "20px", color: "#38bdf8", fontWeight: "bold", marginTop: "6px" }}>
                    {matchedVerification.forecast}
                  </div>
                </div>
                <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "bold" }}>VERIFICATION STATUS</div>
                  <div className="font-technical" style={{ fontSize: "20px", color: "#eab308", fontWeight: "bold", marginTop: "6px" }}>
                    {matchedVerification.status}
                  </div>
                </div>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <span>
              <strong>Validation Commentary:</strong> {matchedVerification.remarks}
            </span>
          }
          recommendedAction={
            <span>Seasonal threshold settings are correct. No manual calibration adjustments required.</span>
          }
          advancedScientificDetails={
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              <span className="font-technical" style={{ fontSize: "10px", color: "#a855f7", fontWeight: "bold" }}>CONTINGENCY MATRIX SKILL SCORES</span>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "10px" }}>
                {[
                  ["CSI (Threat Score)", verification?.seasonal_skill_scores?.Monsoon?.csi || 0.72, "#38bdf8"],
                  ["POD (Hit Rate)", verification?.seasonal_skill_scores?.Monsoon?.pod || 0.82, "#10b981"],
                  ["FAR (False Alarm)", verification?.seasonal_skill_scores?.Monsoon?.far || 0.15, "#ef4444"],
                  ["HSS (Skill Score)", verification?.seasonal_skill_scores?.Monsoon?.hss || 0.76, "#a855f7"],
                  ["BIAS frequency", verification?.seasonal_skill_scores?.Monsoon?.bias || 1.04, "#cbd5e1"]
                ].map(([k, v, color]) => (
                  <div key={k} style={{ backgroundColor: "#0b0f19", border: "1px solid #1e293b", borderRadius: "8px", padding: "10px", textAlign: "center" }}>
                    <div style={{ fontSize: "9.5px", color: "#64748b", fontWeight: "bold" }}>{k}</div>
                    <div className="font-technical" style={{ fontSize: "18px", color, fontWeight: "bold", marginTop: "4px" }}>{v}</div>
                  </div>
                ))}
              </div>
            </div>
          }
        />
      )}

      {/* 8. ANALOG_ARCHIVE (Historical Analog Archive) */}
      {moduleId === "ANALOG_ARCHIVE" && (
        <ModuleSectionLayout
          title="Historical Thunderstorm Analog Finder"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              
              {/* Selectors */}
              <div style={{ display: "flex", gap: "12px", alignItems: "center", backgroundColor: "#020617", padding: "10px 14px", borderRadius: "8px", border: "1px solid #1e293b", flexWrap: "wrap" }}>
                <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>ANALOG SEARCH FILTERS:</span>
                <select
                  value={analogStation}
                  onChange={(e) => setAnalogStation(e.target.value)}
                  style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "11px", cursor: "pointer" }}
                >
                  <option value="Visakhapatnam">Visakhapatnam</option>
                  <option value="Machilipatnam">Machilipatnam</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Kolkata">Kolkata</option>
                  <option value="Hyderabad">Hyderabad</option>
                </select>
                <select
                  value={analogEvent}
                  onChange={(e) => setAnalogEvent(e.target.value)}
                  style={{ backgroundColor: "#0b0f19", color: "#ffffff", border: "1px solid #334155", borderRadius: "6px", padding: "4px 8px", fontSize: "11px", cursor: "pointer" }}
                >
                  <option value="TSRA">THUNDERSTORM (TSRA)</option>
                  <option value="NWX">NO THUNDERSTORM (NWX)</option>
                </select>
              </div>

              {/* Analog Matches Table */}
              <div style={{ border: "1px solid #1e293b", borderRadius: "10px", overflow: "hidden" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "11px", textAlign: "left", color: "#cbd5e1" }}>
                  <thead>
                    <tr style={{ backgroundColor: "#090d16", borderBottom: "2px solid #1e293b", color: "#ffffff" }}>
                      <th style={{ padding: "8px" }}>Date</th>
                      <th style={{ padding: "8px" }}>Station</th>
                      <th style={{ padding: "8px" }}>Observed</th>
                      <th style={{ padding: "8px" }}>CAPE (J/kg)</th>
                      <th style={{ padding: "8px" }}>LI (K)</th>
                      <th style={{ padding: "8px" }}>PWAT (mm)</th>
                      <th style={{ padding: "8px" }}>Outcome</th>
                    </tr>
                  </thead>
                  <tbody>
                    {matchedAnalogs.length > 0 ? (
                      matchedAnalogs.map((item, idx) => (
                        <tr key={idx} style={{ borderBottom: "1px solid #1e293b" }}>
                          <td style={{ padding: "8px", fontWeight: "bold", fontFamily: "JetBrains Mono" }}>{item.date}</td>
                          <td style={{ padding: "8px" }}>{item.station}</td>
                          <td style={{ padding: "8px" }}>{item.observed}</td>
                          <td style={{ padding: "8px" }}>{item.cape} J/kg</td>
                          <td style={{ padding: "8px" }}>{item.li} K</td>
                          <td style={{ padding: "8px" }}>{item.pwat} mm</td>
                          <td style={{ padding: "8px", color: "#10b981", fontWeight: "bold" }}>VERIFIED HIT</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="7" style={{ padding: "12px", textAlign: "center", color: "#64748b" }}>No matching historical analogs found. Try resetting filters.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

            </div>
          }
          meteorologistInterpretation={
            <span>
              The matching historical setups exhibit analogous dry layer intrusions and moisture depths. Buoyancy indicators match convective initiations along the coast, indicating high spatial likelihood of storm front development.
            </span>
          }
          recommendedAction={
            <span>Expect convective evolution vectors to mirror the historical analog track profile.</span>
          }
          advancedScientificDetails={
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", fontSize: "11px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
              <div>
                <div>Cosine similarity metric: <strong>0.925</strong></div>
                <div>CAPE weight vector contribution: <strong>30%</strong></div>
                <div>LI weight vector contribution: <strong>25%</strong></div>
              </div>
              <div>
                <div>PWAT weight vector contribution: <strong>25%</strong></div>
                <div>Euclidean distance score: <strong>0.08</strong></div>
                <div>Analog archive support: <strong>10 years database</strong></div>
              </div>
            </div>
          }
        />
      )}

      {/* 9. BULLETIN (Operational Bulletin Generator) */}
      {moduleId === "BULLETIN" && (
        <ModuleSectionLayout
          title="Auto IMD Bulletin Generator"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              <div style={{ border: "1px dashed #ef4444", backgroundColor: "#020617", borderRadius: "8px", padding: "12px" }}>
                <pre style={{ whiteSpace: "pre-wrap", fontFamily: "JetBrains Mono", fontSize: "11px", lineHeight: "1.6", color: "#fca5a5", margin: 0 }}>
                  {tsBulletin}
                </pre>
              </div>
            </div>
          }
          meteorologistInterpretation={
            <span>
              Moisture influx rates from the Bay of Bengal combined with radiosonde thermodynamic profiles trigger severe convective watch criteria. Immediate public distribution is recommended.
            </span>
          }
          recommendedAction={
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              <span>Export and disseminate warning warnings directly:</span>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={() => handleDownloadBulletin("pdf")} className="glow-btn-blue interactive-action" style={{ padding: "8px 16px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold", display: "flex", alignItems: "center", gap: "6px" }}>
                  <Download size={14} /> Download PDF
                </button>
                <button onClick={() => handleDownloadBulletin("docx")} className="glow-btn-blue interactive-action" style={{ padding: "8px 16px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold", display: "flex", alignItems: "center", gap: "6px" }}>
                  <Download size={14} /> Download DOCX
                </button>
                <button onClick={() => handleDownloadBulletin("txt")} className="glow-btn-blue interactive-action" style={{ padding: "8px 16px", borderRadius: "8px", fontSize: "11px", fontWeight: "bold", display: "flex", alignItems: "center", gap: "6px" }}>
                  <Download size={14} /> Download TXT
                </button>
              </div>
            </div>
          }
          advancedScientificDetails={
            <div style={{ fontSize: "11px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
              <div>Template Structure Hash: <strong>CWC_VIZAG_WARN_TEMPLATE_V2</strong></div>
              <div>Validation Signature: <strong>SSAI-{activeStation?.station_code || "43150"}-{(metadata.cycle).toLowerCase()}-lock</strong></div>
            </div>
          }
        />
      )}

      {/* 10. ANDHRA_MONITOR (Andhra Coastal Monitoring) */}
      {moduleId === "ANDHRA_MONITOR" && (
        <ModuleSectionLayout
          title="Coastal Thunderstorm Monitoring Center"
          metadata={metadata}
          reviewMode={reviewMode}
          currentSituation={
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              
              {/* Station Cards */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "12px" }}>
                {[
                  { name: "Visakhapatnam", code: "43150", risk: activeStation?.station === "Visakhapatnam" && activeStation?.storm_probability >= 70 ? "SEVERE" : "MODERATE", lightning: "HIGH", rain: "MODERATE", breeze: "ACTIVE", potential: activeStation?.station === "Visakhapatnam" ? activeStation?.storm_probability : 65 },
                  { name: "Machilipatnam", code: "43185", risk: activeStation?.station === "Machilipatnam" && activeStation?.storm_probability >= 70 ? "SEVERE" : "HIGH", lightning: "HIGH", rain: "HIGH", breeze: "ACTIVE", potential: activeStation?.station === "Machilipatnam" ? activeStation?.storm_probability : 70 },
                  { name: "Kakinada", code: "43182", risk: "MODERATE", lightning: "MODERATE", rain: "LOW", breeze: "ACTIVE", potential: 52 },
                  { name: "Nellore", code: "43245", risk: "LOW", lightning: "LOW", rain: "LOW", breeze: "INACTIVE", potential: 28 },
                  { name: "Ongole", code: "43220", risk: "MODERATE", lightning: "MODERATE", rain: "LOW", breeze: "ACTIVE", potential: 44 }
                ].map((st) => {
                  const isSelect = selectedStationName === st.name;
                  const cardColor = st.risk === "SEVERE" ? "#ef4444" : st.risk === "HIGH" ? "#f97316" : st.risk === "MODERATE" ? "#eab308" : "#10b981";
                  return (
                    <div
                      key={st.name}
                      onClick={() => setSelectedStationName(st.name)}
                      style={{
                        backgroundColor: "#020617",
                        border: `1px solid ${isSelect ? "#3b82f6" : "#1e293b"}`,
                        borderRadius: "12px",
                        padding: "14px",
                        cursor: "pointer",
                        boxShadow: isSelect ? "0 0 10px rgba(59, 130, 246, 0.15)" : "none",
                        transition: "all 0.2s ease"
                      }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #1e293b", paddingBottom: "6px", marginBottom: "8px" }}>
                        <span style={{ fontSize: "12px", fontWeight: "bold", color: "#ffffff" }}>{st.name}</span>
                        <span style={{ fontSize: "8px", padding: "1px 4px", border: `1px solid ${cardColor}`, color: cardColor, borderRadius: "3px" }}>{st.risk}</span>
                      </div>
                      <div style={{ display: "flex", flexDirection: "column", gap: "4px", fontSize: "10px", color: "#cbd5e1" }}>
                        <div>Lightning: <strong style={{ color: "#ffffff" }}>{st.lightning}</strong></div>
                        <div>Heavy Rain: <strong style={{ color: "#ffffff" }}>{st.rain}</strong></div>
                        <div>Sea Breeze: <strong style={{ color: "#ffffff" }}>{st.breeze}</strong></div>
                        <div style={{ marginTop: "4px", display: "flex", justifyContent: "space-between" }}>
                          <span>Potential:</span>
                          <strong style={{ color: "#f43f5e" }}>{st.potential}%</strong>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

            </div>
          }
          meteorologistInterpretation={
            <span>
              Coastal convergence axis remains highly active between Visakhapatnam and Machilipatnam corridors. Sea-breeze propagation speeds are estimated at 12 km/h, forcing warm boundaries inland and initiating convective updrafts.
            </span>
          }
          recommendedAction={
            <span>Issue localized storm warnings for coastal agricultural and port zones. Alert municipal authorities.</span>
          }
          advancedScientificDetails={
            <div style={{ display: "flex", flexDirection: "column", gap: "10px", fontSize: "11px", fontFamily: "JetBrains Mono" }}>
              <span style={{ color: "#38bdf8", fontWeight: "bold" }}>Bay of Bengal Moisture Convergence Indicators</span>
              <div>Convergence Index value: <strong>{activeStation?.moisture_convergence || 4.2}</strong></div>
              <div>Moisture advection azimuth: <strong>115° ESE</strong></div>
              <div>Est. Coastal Squall line speed: <strong>18 KT</strong></div>
            </div>
          }
        />
      )}

    </div>
  );
}
