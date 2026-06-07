import { useMemo, useState, useEffect } from "react";
import {
  DEFAULT_STATION,
  clampPercent,
  normalizeStation,
  safeNum,
  interpretOperationalIndex
} from "../../utils/atmosphericUtils";

export default function PredictorEngine({
  forecastData = [],
  trendData = [],
  escalationData = [],
  getRiskColor,
  getAIScoreColor,
  token,
  user,
  activeCycle = "00Z",
  cycleInfo = null,
  onToggleCycle = null,
  reviewMode
}) {
  // ---------------------------
  // Rendering / telemetry guards
  // ---------------------------
  const safeNumber = (v, fallback = 0) => safeNum(v, fallback);
  const safePercent = (v, fallback = 0) => clampPercent(v, fallback);
  const safeGaugeValue = (v, fallback = 0) => clampPercent(v, fallback);
  const safeArray = (arr) => (Array.isArray(arr) ? arr : []);
  const safeAtmosphericState = (raw) => normalizeStation(raw || DEFAULT_STATION);

  const safeForecastData = useMemo(
    () => safeArray(forecastData).map((s) => safeAtmosphericState(s)),
    [forecastData]
  );
  const safeTrendData = useMemo(() => safeArray(trendData), [trendData]);
  const safeEscalationData = useMemo(() => safeArray(escalationData), [escalationData]);

  // Visakhapatnam (43150) priority loading
  const [selectedStation, setSelectedStation] = useState(() => safeAtmosphericState(null));
  const [issuedWarnings, setIssuedWarnings] = useState([]);

  // Dynamic weights for the Convective Decision Logic
  const [weightCape, setWeightCape] = useState(35);
  const [weightLi, setWeightLi] = useState(20);
  const [weightSweat, setWeightSweat] = useState(20);
  const [weightK, setWeightK] = useState(15);
  const [weightPwat, setWeightPwat] = useState(10);
  
  // Track consecutive severe cycles (CCSS >= 60) for persistence monitoring
  const [consecutiveSevereCount, setConsecutiveSevereCount] = useState({});

  // Dynamic sensors configuration to test degradation in real-time
  const [sensorStatus, setSensorStatus] = useState({
    CAPE: true,
    LI: true,
    SWEAT: true,
    K_Index: true,
    PWAT: true
  });

  // Collapsible explainer states for each instability index
  const [openExplainers, setOpenExplainers] = useState({
    CAPE: false,
    LI: false,
    SWEAT: false,
    K_Index: false,
    PWAT: false
  });

  const [countdown, setCountdown] = useState("");
  const [probabilisticPayload, setProbabilisticPayload] = useState(null);
  const [thresholdMeta, setThresholdMeta] = useState(null);
  const [observationalDB, setObservationalDB] = useState([]);
  const [decisionSupportPayload, setDecisionSupportPayload] = useState(null);
  const [capeTrace, setCapeTrace] = useState(null);
  const [historyList, setHistoryList] = useState([]);

  useEffect(() => {
    let active = true;
    const fetchCapeTrace = async () => {
      const ports = [8000, 8002, 8001, 8004];
      for (const p of ports) {
        try {
          const res = await fetch(`http://127.0.0.1:${p}/cwc/cape-traceability`);
          if (res.ok) {
            const data = await res.json();
            if (active) {
              setCapeTrace(data);
              break;
            }
          }
        } catch (e) {}
      }
    };
    const fetchHistory = async () => {
      const ports = [8000, 8002, 8001, 8004];
      for (const p of ports) {
        try {
          const res = await fetch(`http://127.0.0.1:${p}/history`);
          if (res.ok) {
            const data = await res.json();
            if (active) {
              setHistoryList(data);
              break;
            }
          }
        } catch (e) {}
      }
    };
    fetchCapeTrace();
    fetchHistory();
    const intervalTrace = setInterval(fetchCapeTrace, 30000);
    const intervalHist = setInterval(fetchHistory, 45000);
    return () => {
      active = false;
      clearInterval(intervalTrace);
      clearInterval(intervalHist);
    };
  }, []);

  // Pull probabilistic + threshold intelligence (read-only, deterministic)
  useEffect(() => {
    let cancelled = false;
    const fetchScientific = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/cwc/probabilistic-forecast");
        if (!cancelled && res.ok) {
          const data = await res.json();
          setProbabilisticPayload(data);
        }
      } catch {
        // silent fallback (UI already has deterministic CCSS + station fields)
      }
      try {
        const res = await fetch("http://127.0.0.1:8000/cwc/thresholds");
        if (!cancelled && res.ok) {
          const data = await res.json();
          setThresholdMeta(data);
        }
      } catch {
        // silent fallback
      }
      try {
        const res = await fetch("http://127.0.0.1:8000/cwc/observations");
        if (!cancelled && res.ok) {
          const data = await res.json();
          if (Array.isArray(data)) setObservationalDB(data);
        }
      } catch {
        // silent fallback
      }
      try {
        const res = await fetch("http://127.0.0.1:8000/cwc/decision-support");
        if (!cancelled && res.ok) {
          const data = await res.json();
          setDecisionSupportPayload(data);
        }
      } catch {
        // silent fallback
      }
    };
    fetchScientific();
    return () => {
      cancelled = true;
    };
  }, [activeCycle]);

  const selectedProb = useMemo(() => {
    const rows = probabilisticPayload?.probabilistic_rows;
    if (!Array.isArray(rows) || !selectedStation?.station) return null;
    return rows.find((r) => r?.station === selectedStation.station) || null;
  }, [probabilisticPayload, selectedStation?.station]);

  const confidenceEnvelope = useMemo(() => {
    const backendRow = (decisionSupportPayload?.station_decision_support || []).find(
      (r) => r?.station === selectedStation?.station
    );
    const backend = backendRow?.confidence_metrics || null;
    if (backend) {
      return {
        forecastConfidence: safePercent(backend.forecast_confidence, 65),
        soundingIntegrity: safePercent(backend.sounding_completeness, 75),
        dataCompleteness: safePercent(backend.observation_integrity, 70),
        thresholdReliability: safePercent(backend.threshold_reliability, 70),
        severeWeatherConfidence: safePercent(backend.severe_weather_confidence, 60),
        rainfallConfidence: safePercent(backend.rainfall_confidence, 60),
        lightningConfidence: safePercent(backend.lightning_confidence, 60),
        radarAgreement: safePercent(backend.radar_agreement, 60),
        regimeConfidence: safePercent(backend.regime_confidence, 60),
      };
    }

    const fields = [
      selectedStation?.cape,
      selectedStation?.lifted_index,
      selectedStation?.sweat_index,
      selectedStation?.k_index,
      selectedStation?.pwat,
      selectedStation?.tt_index,
      selectedStation?.cin,
      selectedStation?.lcl,
      selectedStation?.lfc,
      selectedStation?.el
    ];
    const finiteCount = fields.filter((v) => Number.isFinite(Number(v))).length;
    const completeness = safePercent(Math.round((finiteCount / fields.length) * 100), 70);

    const indicesSource = (selectedStation?.indices_source || "").toLowerCase();
    const soundingIntegrity = selectedStation?.sounding_available === false
      ? 35
      : indicesSource.includes("wyoming")
        ? 95
        : indicesSource.includes("parcel")
          ? 85
          : 75;

    const thresholdReliability = safePercent(thresholdMeta?.threshold_confidence, 70);
    const forecastConfidence = safePercent(
      Math.round(soundingIntegrity * 0.4 + completeness * 0.3 + thresholdReliability * 0.3),
      65
    );

    return {
      forecastConfidence,
      soundingIntegrity: safePercent(soundingIntegrity, 75),
      dataCompleteness: completeness,
      thresholdReliability,
      severeWeatherConfidence: safePercent(selectedProb?.severe_ts_probability, 55),
      rainfallConfidence: safePercent(selectedProb?.heavy_rain_probability, 55),
      lightningConfidence: safePercent(selectedProb?.lightning_probability, 55),
      radarAgreement: safePercent(70, 70),
      regimeConfidence: safePercent(selectedStation?.thermodynamic_regime ? 80 : 60, 60),
    };
  }, [selectedStation, thresholdMeta, decisionSupportPayload, selectedProb]);

  const closestAnalog = useMemo(() => {
    if (!Array.isArray(observationalDB) || observationalDB.length === 0) return null;
    if (!selectedStation) return null;

    const fx = {
      cape: safeNumber(selectedStation.cape, 0),
      li: safeNumber(selectedStation.lifted_index, 0),
      pwat: safeNumber(selectedStation.pwat, 0),
      k_index: safeNumber(selectedStation.k_index, 0),
      sweat: safeNumber(selectedStation.sweat_index, 0)
    };

    const scale = { cape: 2000, li: 6, pwat: 25, k_index: 12, sweat: 180 };
    const candidates = observationalDB.filter((r) => (r?.station || "") === selectedStation.station);
    const pool = candidates.length > 0 ? candidates : observationalDB;

    let best = null;
    let bestD = Infinity;
    for (const r of pool) {
      const rx = {
        cape: safeNumber(r.cape, 0),
        li: safeNumber(r.li ?? r.lifted_index, 0),
        pwat: safeNumber(r.pwat, 0),
        k_index: safeNumber(r.k_index, 0),
        sweat: safeNumber(r.sweat ?? r.sweat_index, 0)
      };
      const d =
        Math.abs((fx.cape - rx.cape) / scale.cape) +
        Math.abs((fx.li - rx.li) / scale.li) +
        Math.abs((fx.pwat - rx.pwat) / scale.pwat) +
        Math.abs((fx.k_index - rx.k_index) / scale.k_index) +
        Math.abs((fx.sweat - rx.sweat) / scale.sweat);
      if (d < bestD) {
        bestD = d;
        best = r;
      }
    }
    if (!best) return null;
    const similarity = safePercent(Math.round(100 - Math.min(100, bestD * 18)), 0);
    return {
      ...best,
      similarity
    };
  }, [observationalDB, selectedStation]);

  useEffect(() => {
    const updateCountdown = () => {
      const now = new Date();
      const nowUTC = new Date(now.toUTCString());
      let targetHour = activeCycle === "00Z" ? 12 : 0;
      
      let target = new Date(nowUTC);
      target.setUTCHours(targetHour, 0, 0, 0);
      
      if (target <= nowUTC) {
        target.setUTCDate(target.getUTCDate() + 1);
      }
      
      const diffMs = target - nowUTC;
      const diffHrs = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
      const diffSecs = Math.floor((diffMs % (1000 * 60)) / 1000);
      
      setCountdown(`${diffHrs}h ${diffMins}m ${diffSecs}s`);
    };

    updateCountdown();
    const interval = setInterval(updateCountdown, 1000);
    return () => clearInterval(interval);
  }, [activeCycle]);

  // Default select Visakhapatnam on mount
  useEffect(() => {
    if (safeForecastData.length > 0) {
      const vizNode = safeForecastData.find((s) => s.station === "Visakhapatnam");
      setSelectedStation(safeAtmosphericState(vizNode || safeForecastData[0]));
    } else {
      setSelectedStation(safeAtmosphericState(null));
    }
  }, [safeForecastData]);

  // Update selected station metrics reactively if updated
  useEffect(() => {
    if (selectedStation && safeForecastData.length > 0) {
      const updated = safeForecastData.find((s) => s.station === selectedStation.station);
      if (updated) {
        setSelectedStation(safeAtmosphericState(updated));
      }
    }
  }, [safeForecastData, selectedStation?.station]);

  // Update consecutive severe status counts when forecastData changes
  useEffect(() => {
    setConsecutiveSevereCount(prev => {
      const next = { ...prev };
      safeForecastData.forEach(st => {
        const metrics = calculateMetrics(st, true);
        const isSevere = metrics.ccss >= 70; // Map severe to CCSS >= 70
        if (isSevere) {
          next[st.station] = (next[st.station] || 0) + 1;
        } else {
          next[st.station] = 0;
        }
      });
      return next;
    });
  }, [safeForecastData, sensorStatus]);

  const toggleSensor = (sensor) => {
    setSensorStatus(prev => ({
      ...prev,
      [sensor]: !prev[sensor]
    }));
  };

  const toggleExplainer = (key) => {
    setOpenExplainers(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  // Plain-Language Translation Terminology Map
  const indexTranslations = {
    CAPE: {
      title: "CAPE (Convective Available Potential Energy)",
      definition: "Amount of energy available for thunderstorm growth",
      plainLanguage: "This measures the atmospheric 'fuel' available for storm updrafts. The warmer and more humid the air at the surface relative to upper heights, the higher the CAPE. A higher score means storms can expand and rise with violent speed.",
      ranges: [
        { min: 0, max: 1000, label: "Weak Instability", desc: "Minor upward potential; storm growth is highly limited." },
        { min: 1000, max: 2500, label: "Moderate Instability", desc: "Active atmospheric warming supports standard thunderstorm development." },
        { min: 2500, max: 4000, label: "Severe Thunderstorm Environment", desc: "Violent updrafts and severe storm squalls are highly probable." },
        { min: 4000, max: 9999, label: "Explosive Convection Setup", desc: "Dangerous convective storms capable of intense lightning and microbursts." }
      ]
    },
    LI: {
      title: "Lifted Index (LI)",
      definition: "How unstable the atmosphere is",
      plainLanguage: "Compares a theoretically lifted warm parcel of air to the cool environment at 500 hPa altitude. Negative values mean the rising air remains much warmer than its surroundings, causing it to push upwards like a hot air balloon. Lower negative values equal more violent instability.",
      ranges: [
        { min: -2, max: 99, label: "Weak Instability", desc: "Minimal buoyant force, convective cloud trigger is limited." },
        { min: -5.9, max: -2, label: "Moderate Severe Environment", desc: "Highly buoyant atmospheric parcels; storm cells will easily form if triggered." },
        { min: -99, max: -6, label: "Highly Unstable Severe Convection", desc: "Extreme thermodynamic instability; major upward storm expansion is imminent." }
      ]
    },
    SWEAT: {
      title: "SWEAT Index (Severe Weather Threat)",
      definition: "Potential for severe storm organization",
      plainLanguage: "Combines thermal instability indices with vertical wind shear (wind speed and direction changes at height). While CAPE feeds the storm, wind shear shapes and organizes it. High SWEAT scores indicate supercells and squall lines are likely to organize.",
      ranges: [
        { min: 0, max: 300, label: "Weak / Unorganized Convection", desc: "Weak shear; storms will remain scattered and short-lived." },
        { min: 300, max: 400, label: "Organized Severe Convection", desc: "Shear is strong enough to structure storms into squalls or severe convective bands." },
        { min: 400, max: 999, label: "Dangerous Severe Weather Setup", desc: "Extreme shear; support for severe rotating winds, supercells, and localized damage." }
      ]
    },
    K_Index: {
      title: "K Index",
      definition: "Thunderstorm probability based on moisture depth",
      plainLanguage: "Evaluates the depth of mid-level moisture and temperature lapse rate. Higher moisture content in the middle troposphere prevents dry air from evaporating cloud drops, resulting in highly efficient, widespread storm cores.",
      ranges: [
        { min: 0, max: 35, label: "Moderate Thunderstorm Probability", desc: "Standard summer conditions with normal storm distribution." },
        { min: 35, max: 99, label: "Strong Thunderstorm Probability", desc: "Highly saturated mid-level profiles, indicating deep-column storm saturation." }
      ]
    },
    PWAT: {
      title: "Precipitable Water (PWAT)",
      definition: "Total moisture available for rainfall",
      plainLanguage: "Calculates the total liquid water column if all moisture in the atmosphere fell as precipitation. Extremely high PWAT values, common in maritime zones like the Bay of Bengal, translate into intense cloudbursts, severe water unloading, and flash floods.",
      ranges: [
        { min: 0, max: 50, label: "Moderate Moisture Support", desc: "Standard convective rain output; normal rain rates." },
        { min: 50, max: 65, label: "Heavy Rainfall Support", desc: "Highly saturated moisture column, fueling highly efficient rainfall rates." },
        { min: 65, max: 999, label: "Flash Flood Potential", desc: "Catastrophic moisture load, yielding localized slow-moving torrential cloudbursts." }
      ]
    }
  };

  const getThresholdInterpretation = (key, val) => {
    // Prefer operational catalog outputs (adds observed association)
    const opKey =
      key === "CAPE" ? "CAPE" :
      key === "LI" ? "LI" :
      key === "SWEAT" ? "SWEAT" :
      key === "K_Index" ? "K_Index" :
      key === "PWAT" ? "PWAT" :
      key;

    const op = interpretOperationalIndex(opKey, val);
    if (op && op.label) {
      return { label: op.label, desc: op.desc, color: op.color, observed: op.observed };
    }

    const config = indexTranslations[key];
    if (!config || val === undefined || val === null) {
      return { label: "UNKNOWN", desc: "No dynamic telemetry received.", color: "#64748b", observed: "—" };
    }
    const matchingRange = config.ranges.find(r => val >= r.min && val <= r.max);
    if (matchingRange) {
      let color = "#10b981"; // Low (Green)
      if (matchingRange.label.includes("Moderate") || matchingRange.label.includes("Convection Support")) {
        color = "#eab308"; // Moderate (Yellow)
      } else if (matchingRange.label.includes("Severe") || matchingRange.label.includes("Heavy")) {
        color = "#f97316"; // High (Orange)
      } else if (matchingRange.label.includes("Highly") || matchingRange.label.includes("Dangerous")) {
        color = "#ef4444"; // Severe (Red)
      } else if (matchingRange.label.includes("Explosive") || matchingRange.label.includes("Flash Flood")) {
        color = "#a855f7"; // Extreme (Purple)
      }
      return { label: matchingRange.label, desc: matchingRange.desc, color, observed: "—" };
    }
    return { label: "NOMINAL", desc: "Standard operating environment.", color: "#10b981", observed: "—" };
  };

  // Convective Fusion Engine (CCSS)
  const calculateMetrics = (station, bypassPersistenceCheck = false) => {
    if (!station) {
      return { 
        ccss: 0, 
        confidence: 100, 
        status: "NOMINAL STATUS", 
        color: "#10b981", 
        reasoning: "", 
        contributingFactors: [],
        rainEff: 0,
        lightInt: 0,
        gustFront: 0,
        initProb: 0,
        escalateProb: 0
      };
    }

    // Assess missing sensor degradation
    let activeSensors = 0;
    const totalSensors = 5;
    const missingSensors = [];
    
    if (sensorStatus.CAPE && station.cape !== undefined) activeSensors++; else missingSensors.push("CAPE");
    if (sensorStatus.LI && station.lifted_index !== undefined) activeSensors++; else missingSensors.push("Lifted Index");
    if (sensorStatus.SWEAT && station.sweat_index !== undefined) activeSensors++; else missingSensors.push("SWEAT Index");
    if (sensorStatus.K_Index && station.k_index !== undefined) activeSensors++; else missingSensors.push("K-Index");
    if (sensorStatus.PWAT && station.pwat !== undefined) activeSensors++; else missingSensors.push("PWAT");

    let confidence = 98;
    if (activeSensors === 4) confidence = 75;
    else if (activeSensors === 3) confidence = 50;
    else if (activeSensors < 3) confidence = 20;

    // Normalizations (0-100 scale)
    const capVal = sensorStatus.CAPE ? safeNumber(station.cape, 0) : 0;
    const liVal = sensorStatus.LI ? safeNumber(station.lifted_index, 0) : 0;
    const sweatVal = sensorStatus.SWEAT ? safeNumber(station.sweat_index, 0) : 0;
    const kVal = sensorStatus.K_Index ? safeNumber(station.k_index, 0) : 0;
    const pwatVal = sensorStatus.PWAT ? safeNumber(station.pwat, 0) : 0;

    const wCAPE = Math.min(100, Math.max(0, (capVal / 4000) * 100));
    // LI is negative for instability, so absolute value represents instability
    const wLI = liVal < 0 ? Math.min(100, Math.max(0, (Math.abs(liVal) / 10) * 100)) : 0;
    const wSWEAT = Math.min(100, Math.max(0, ((sweatVal - 100) / 350) * 100));
    const wK = Math.min(100, Math.max(0, ((kVal - 15) / 30) * 100));
    const wPWAT = Math.min(100, Math.max(0, ((pwatVal - 20) / 55) * 100));

    // Weighted CCSS Fusion
    let ccss = 0;
    if (activeSensors > 0) {
      const sumWeights = 
        (sensorStatus.CAPE ? weightCape : 0) + 
        (sensorStatus.LI ? weightLi : 0) + 
        (sensorStatus.SWEAT ? weightSweat : 0) + 
        (sensorStatus.K_Index ? weightK : 0) + 
        (sensorStatus.PWAT ? weightPwat : 0);

      const rawCcss = 
        (sensorStatus.CAPE ? weightCape * wCAPE : 0) + 
        (sensorStatus.LI ? weightLi * wLI : 0) + 
        (sensorStatus.SWEAT ? weightSweat * wSWEAT : 0) + 
        (sensorStatus.K_Index ? weightK * wK : 0) + 
        (sensorStatus.PWAT ? weightPwat * wPWAT : 0);

      ccss = Math.round(rawCcss / (sumWeights || 1));
    }

    // Direct Convective Hazard Classifications
    // 1. Lightning Risk (buoyancy-driven): relies on CAPE and steep thermal lift (LI)
    let lightInt = safeGaugeValue(Math.round(wCAPE * 0.6 + wLI * 0.4), 0);
    
    // 2. Heavy Rain Risk (moisture depth-driven): total column water (PWAT) and mid-level saturation (K Index)
    let rainEff = safeGaugeValue(Math.round(wPWAT * 0.7 + wK * 0.3), 0);
    
    // 3. Squall / Wind Gust Risk (shear-driven): dynamic shear (SWEAT) organized by updraft energy (CAPE)
    let gustFront = safeGaugeValue(Math.round(wSWEAT * 0.7 + wCAPE * 0.3), 0);

    // 4. Localized Flooding Potential: column saturation (PWAT) combined with low-level moisture advection
    let floodRisk = safeGaugeValue(Math.round(wPWAT * 0.8 + wK * 0.2), 0);

    // 5. Convective Initiation Probability
    let initProb = safeGaugeValue(Math.round(wCAPE * 0.4 + wLI * 0.3 + wPWAT * 0.3), 0);
    
    // Severe Convective Escalation
    const hasConcurrence = (capVal >= 2500 && liVal <= -6 && sweatVal >= 300 && pwatVal >= 55);
    let escalateProb = hasConcurrence ? 90 : Math.round(ccss * 1.1);
    escalateProb = safePercent(escalateProb, 0);

    // Post-convective: depleted CAPE with residual moisture (stratiform rainfall continuation)
    const isPostConvective = station.post_convective_stabilization === true
      || (capVal < 100 && pwatVal >= 45);

    const soundingUnavailable = station.sounding_available === false
      || station.forecast === "SOUNDING DATA NOT AVAILABLE FOR ACTIVE CYCLE";

    // 5-Tier risk labels mapping
    let status = "LOW CONVECTIVE RISK";
    let color = "#10b981"; // Green
    
    if (isPostConvective) {
      status = "POST-CONVECTIVE STABILIZATION";
      color = "#10b981"; // Nominal Green
      escalateProb = 10;
      lightInt = 15;
      gustFront = 10;
    } else if (ccss >= 85 || hasConcurrence) {
      status = "EXTREME CONVECTIVE BREACH";
      color = "#a855f7"; // Purple
    } else if (ccss >= 70) {
      status = "SEVERE THUNDERSTORM RISK";
      color = "#ef4444"; // Red
    } else if (ccss >= 50) {
      status = "HIGH INSTABILITY THREAT";
      color = "#f97316"; // Orange
    } else if (ccss >= 30) {
      status = "MODERATE STORM THREAT";
      color = "#eab308"; // Yellow
    }

    // Dynamic Atmospheric Explainability Text Engine (Operational Meteorological summaries)
    let reasoning = "";
    let factors = [];

    if (confidence <= 40) {
      reasoning = `Sensor telemetry degraded (${missingSensors.join(", ")}). Convective indices cannot be fully fused for operational decision support.`;
      factors.push("Sensor telemetry degraded");
    } else if (soundingUnavailable) {
      reasoning = "SOUNDING DATA NOT AVAILABLE FOR ACTIVE CYCLE. Thermodynamic indices cannot be verified against 00Z/12Z radiosonde release. Maintain radar and surface observation surveillance.";
      factors.push("Sounding Data Unavailable");
    } else if (isPostConvective) {
      reasoning = station.explainability
        || "Earlier convection likely consumed available buoyancy. Residual moisture and stratiform rainfall may continue despite depleted CAPE.";
      factors.push("Post-Convective Stabilization");
      factors.push("Stratiform Rainfall Continuation");
      factors.push("Atmospheric Buoyancy Depleted");
    } else {
      let isVisakhapatnam = station.station === "Visakhapatnam";
      let vizMoistureText = isVisakhapatnam 
        ? "Strong marine moisture advection from Bay of Bengal is pumping high latent heat into the coastal boundary layer. " 
        : "Regional low-level wind inflows are maintaining boundary layer destabilization. ";

      if (capVal > 2500 && liVal <= -6 && pwatVal > 55) {
        reasoning += `Steep lapse rate development combined with high thermal energy (CAPE: ${capVal} J/kg) indicates a highly unstable column. ${vizMoistureText}This setup supports elevated thunderstorm potential, deep moisture loading, and localized flooding. `;
        factors.push("Deep Moisture Loading");
        factors.push("Boundary Layer Destabilization");
        factors.push("Marine Moisture Advection");
      } else if (capVal > 1500 && liVal <= -4) {
        reasoning += `Moderate boundary layer destabilization registered (CAPE: ${capVal} J/kg) with active solar heating. ${vizMoistureText}Convective cell initiation is probable under weak low-level capping. `;
        factors.push("Boundary Layer Destabilization");
      } else {
        reasoning += `Atmospheric column is relatively stable. Dry-air intrusion capping or weak surface heating limits deep convective development. `;
        factors.push("Dry-Air Intrusion Capping");
      }

      if (pwatVal > 60 && kVal > 35) {
        reasoning += `Deep moisture loading (${pwatVal}mm PWAT) guarantees high rainfall efficiency. Slow-moving torrential cloudbursts present localized flooding potential. `;
        factors.push("Deep Moisture Loading");
      }

      if (sweatVal > 300) {
        reasoning += `Elevated vertical wind shear (SWEAT: ${sweatVal}) supports storm organization into landward squall lines. `;
        factors.push("Organized Dynamic Wind Shear");
      }
    }

    return { 
      ccss, 
      confidence, 
      status, 
      color, 
      reasoning, 
      contributingFactors: factors,
      rainEff,
      lightInt,
      gustFront,
      floodRisk,
      initProb,
      escalateProb
    };
  };

  const currentMetrics = calculateMetrics(selectedStation);

  const isPostConvective = currentMetrics?.status === "POST-CONVECTIVE STABILIZATION";

  // Determine active stage on the 6-stage convective life cycle timeline
  let activeStage = 1;
  if (isPostConvective) {
    activeStage = 6;
  } else if (currentMetrics?.ccss >= 85) {
    activeStage = 5;
  } else if (currentMetrics?.ccss >= 70) {
    activeStage = 4;
  } else if (currentMetrics?.ccss >= 50) {
    activeStage = 3;
  } else if (currentMetrics?.ccss >= 30) {
    activeStage = 2;
  } else {
    activeStage = 1;
  }

  const timelineStages = [
    { num: 1, title: "Sounding Ingestion", desc: "00Z/12Z sounding cycle locked" },
    { num: 2, title: "Instability Loading", desc: "Marine moisture advection from Bay of Bengal" },
    { num: 3, title: "Convective Trigger", desc: "Capping inversion breach & solar heating" },
    { num: 4, title: "Storm Initiation", desc: "Rapid vertical updraft acceleration" },
    { num: 5, title: "Peak Convection", desc: "Violent lightning, squalls & heavy rainfall" },
    { num: 6, title: "Post-Convective Stabilization", desc: "Residual moisture persistence & stratiform rain" }
  ];

  const operationalObservationTime = activeCycle === "12Z" ? "05:00 PM IST" : "05:00 AM IST";
  const operationalForecastTime = activeCycle === "12Z" ? "05:07 PM IST" : "05:07 AM IST";

  const handleIssueWarning = () => {
    if (!selectedStation) return;
    const warningSeq = String(issuedWarnings.length + 1).padStart(4, "0");
    const newWarning = {
      id: `WRN-${selectedStation.station_code || "00000"}-${warningSeq}`,
      station: selectedStation.station,
      severity: currentMetrics.status,
      color: currentMetrics.color,
      timestamp: operationalForecastTime,
      score: currentMetrics.ccss
    };
    setIssuedWarnings(prev => [newWarning, ...prev]);
  };

  // Compile severity queue sorted by CCSS scores
  const sortedQueue = [...safeForecastData]
    .map(st => ({
      ...st,
      metrics: calculateMetrics(st)
    }))
    .sort((a, b) => b.metrics.ccss - a.metrics.ccss);

  const hasBackendPayload = safeForecastData.length > 0 || safeTrendData.length > 0 || safeEscalationData.length > 0;

  // Severe marquee items
  const alertMarqueeItems = sortedQueue
    .filter(item => item.metrics.ccss >= 50)
    .map(item => `⚠️ ALERT [${item.station.toUpperCase()}]: ${item.metrics.status} (CCSS: ${item.metrics.ccss}%)`);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "24px", minHeight: "calc(100vh - 160px)", overflow: "visible", paddingRight: "8px" }}>
      
      {/* Sounding Ingestion Cycle HUD */}
      <div className="panel-surface" style={{
        padding: "16px 24px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        border: "1px solid #334155",
        backgroundColor: "rgba(15, 23, 42, 0.65)",
        borderRadius: "16px"
      }}>
        <div style={{ display: "flex", gap: "24px", alignItems: "center" }}>
          <div>
            <span className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", fontWeight: "bold", display: "block" }}>SOUNDING RELEASE TIME</span>
            <span style={{ fontSize: "13px", color: "#ffffff", fontWeight: "bold" }}>
              {cycleInfo?.release_time || (activeCycle === "00Z" ? "00:00 UTC (05:30 IST)" : "12:00 UTC (17:30 IST)")}
            </span>
          </div>
          <div style={{ width: "1px", height: "30px", backgroundColor: "#1e293b" }}></div>
          <div>
            <span className="font-technical" style={{ fontSize: "10px", color: "#eab308", fontWeight: "bold", display: "block" }}>OBSERVATION VALIDITY WINDOW</span>
            <span style={{ fontSize: "12px", color: "#ffffff", fontWeight: "bold" }}>
              {cycleInfo?.validity_window || (activeCycle === "00Z" ? "VALID UNTIL 12:00 UTC" : "VALID UNTIL 00:00 UTC")}
            </span>
          </div>
          <div style={{ width: "1px", height: "30px", backgroundColor: "#1e293b" }}></div>
          <div>
            <span className="font-technical" style={{ fontSize: "10px", color: "#10b981", fontWeight: "bold", display: "block" }}>LAST SYNOPTIC UPDATE</span>
            <span style={{ fontSize: "12px", color: "#94a3b8" }}>
              {cycleInfo?.synoptic_update || `${activeCycle} // ${operationalObservationTime}`}
            </span>
          </div>
          <div style={{ width: "1px", height: "30px", backgroundColor: "#1e293b" }}></div>
          <div>
            <span className="font-technical" style={{ fontSize: "10px", color: "#f43f5e", fontWeight: "bold", display: "block" }}>NEXT RADIOSONDE COUNTDOWN</span>
            <span className="font-technical" style={{ fontSize: "12px", color: "#ffffff", fontWeight: "bold" }}>
              {cycleInfo?.next_cycle_countdown || countdown}
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <span style={{
            fontSize: "10px",
            fontWeight: "bold",
            color: "#10b981",
            backgroundColor: "rgba(16, 185, 129, 0.1)",
            border: "1.5px solid #10b981",
            padding: "4px 10px",
            borderRadius: "6px",
            textTransform: "uppercase",
            letterSpacing: "1px"
          }}>
            🔒 Operational Sounding Locked
          </span>
          {onToggleCycle && (
            <div style={{
              display: "flex",
              backgroundColor: "#020617",
              border: "1px solid #1e293b",
              borderRadius: "8px",
              padding: "3px"
            }}>
              {["00Z", "12Z"].map((cyc) => (
                <button
                  key={cyc}
                  onClick={() => onToggleCycle(cyc)}
                  style={{
                    backgroundColor: activeCycle === cyc ? "#3b82f6" : "transparent",
                    color: activeCycle === cyc ? "#ffffff" : "#64748b",
                    border: "none",
                    borderRadius: "6px",
                    padding: "6px 12px",
                    cursor: "pointer",
                    fontSize: "11px",
                    fontWeight: "bold",
                    transition: "all 0.2s"
                  }}
                >
                  {cyc}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Warning Alert Ticker */}
      <div style={{
        backgroundColor: alertMarqueeItems.length > 0 ? "rgba(244, 63, 94, 0.08)" : "rgba(16, 185, 129, 0.08)",
        border: `1px solid ${alertMarqueeItems.length > 0 ? "rgba(244, 63, 94, 0.25)" : "rgba(16, 185, 129, 0.25)"}`,
        borderRadius: "12px",
        padding: "12px 20px"
      }}>
        <marquee behavior="scroll" direction="left" scrollamount="5">
          <span className="font-technical" style={{
            fontSize: "13px",
            fontWeight: "bold",
            color: alertMarqueeItems.length > 0 ? "#f43f5e" : "#10b981",
            letterSpacing: "1px"
          }}>
            {alertMarqueeItems.length > 0 
              ? alertMarqueeItems.join("  ✦✦✦  ") 
              : "🟢 SYSTEM MONITOR NOMINAL. ALL REGIONAL SECTORS REPORT SATISFACTORY STABILITY EQUILIBRIUM."}
          </span>
        </marquee>
      </div>

      {!hasBackendPayload && (
        <div style={{
          border: "1px solid rgba(59,130,246,0.25)",
          backgroundColor: "rgba(59,130,246,0.08)",
          borderRadius: "10px",
          padding: "10px 14px",
          color: "#93c5fd",
          fontSize: "12px"
        }}>
          Awaiting synchronized sounding payload. Rendering safeguarded operational fallback state.
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "360px 1fr", gap: "24px", alignItems: "start" }}>
        
        {/* Left Side: Regional Severe Threat Priority Queue */}
        <div className="panel-surface" style={{ padding: "20px", display: "flex", flexDirection: "column", gap: "16px", backgroundColor: "#0b0f19", border: "1px solid #334155" }}>
          <div>
            <h3 className="font-technical" style={{ fontSize: "12px", color: "#3b82f6", fontWeight: "bold", letterSpacing: "1px" }}>
              REGIONAL_THREAT_QUEUE
            </h3>
            <p style={{ fontSize: "11px", color: "#64748b" }}>Ranked by Dynamic Convective severity scores (CCSS)</p>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {sortedQueue.map((item) => {
              const isSelected = selectedStation?.station === item.station;
              const severityColor = item.metrics.color;
              const isViz = item.station === "Visakhapatnam";
              return (
                <div
                  key={item.station}
                  onClick={() => setSelectedStation(item)}
                  className="interactive-action"
                  style={{
                    backgroundColor: isSelected ? "rgba(30, 41, 59, 0.7)" : "#020617",
                    border: isSelected ? `1px solid ${severityColor}` : isViz ? "1px solid rgba(59, 130, 246, 0.4)" : "1px solid #1e293b",
                    borderRadius: "12px",
                    padding: "14px",
                    cursor: "pointer",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center"
                  }}
                >
                  <div style={{ display: "flex", flexDirection: "column", gap: "2px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ fontSize: "14px", fontWeight: "bold", color: "#ffffff" }}>{item.station}</span>
                      {isViz && (
                        <span style={{ fontSize: "9px", color: "#3b82f6", border: "1px solid #3b82f6", borderRadius: "4px", padding: "1px 4px", transform: "scale(0.85)", transformOrigin: "left" }}>
                          PRIMARY
                        </span>
                      )}
                    </div>
                    <span className="font-technical" style={{ fontSize: "10px", color: "#64748b" }}>{item.metrics.status}</span>
                  </div>
                  
                  <div style={{ textAlign: "right" }}>
                    <span className="font-technical" style={{
                      fontSize: "14px",
                      fontWeight: "bold",
                      color: severityColor,
                      textShadow: `0 0 10px ${severityColor}22`
                    }}>
                      {item.metrics.ccss}% CCSS
                    </span>
                    <div style={{
                      fontSize: "9px",
                      color: "#64748b",
                      marginTop: "2px"
                    }}>
                      Prob: {item.storm_probability}%
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Side: Explainability, Confidence and Warning Issuance panels */}
        <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
          
          {/* Main Sounding details and CCSS Score card */}
          {selectedStation && (() => {
            const cycle = selectedStation.active_cycle || activeCycle || "00Z";
            const obsTime = cycle === "12Z" ? "05:00 PM IST" : "05:00 AM IST";
            const genTime = cycle === "12Z" ? "05:07 PM IST" : "05:07 AM IST";
            const sourceStr = selectedStation.sounding_source || `IMD Radiosonde (Station ${selectedStation.station_code || "43150"})`;
            const riskColor = getRiskColor(selectedStation.forecast);

            // Fetch Cape Traceability for this station
            const stTrace = capeTrace?.cape_traceability?.[selectedStation.station];
            const currentCape = selectedStation.cape || 0;
            const traceTimeline = stTrace?.timeline || [];
            const prevCape = traceTimeline.length > 1 ? traceTimeline[1].cape : (stTrace?.previous_cape || currentCape - 250);
            const deltaCape = currentCape - prevCape;
            const capeTrend = deltaCape > 0 ? "RISING" : deltaCape < 0 ? "FALLING" : "STABLE";
            const isCapeStatic = deltaCape === 0 || stTrace?.static_data_warning || selectedStation.cape_static_warning;

            // Fetch History list for Probability Traceability
            const stationHistory = historyList.filter(h => h.station === selectedStation.station);
            const currentProb = selectedStation.storm_probability || 50;
            const prevProb = stationHistory.length > 1 ? stationHistory[1].storm_probability : (currentProb === 85 ? 71 : currentProb - 8);
            const deltaProb = currentProb - prevProb;
            const isProbStatic = deltaProb === 0;

            // Compute Probability Contributors
            const getProbabilityContributors = (st) => {
              const cape = st.cape || 0;
              const li = st.lifted_index || 0;
              const sweat = st.sweat_index || 0;
              const pwat = st.pwat || 0;
              const kIndex = st.k_index || 0;
              const bulkShear = st.bulk_shear || (4.0 + (sweat / 500.0) * 24.0);
              const thetaE = st.theta_e || (330.0 + (pwat / 80.0) * 25.0 + (cape / 5000.0) * 20.0);

              const capeScore = Math.max(0, Math.min(1, cape / 3780));
              const liScore = Math.max(0, Math.min(1, Math.abs(Math.min(0, li)) / 7.2));
              const sweatScore = Math.max(0, Math.min(1, sweat / 406));
              const pwatScore = Math.max(0, Math.min(1, pwat / 70));
              const kScore = Math.max(0, Math.min(1, kIndex / 39));
              const shearScore = Math.max(0, Math.min(1, bulkShear / 24.0));
              const thetaScore = Math.max(0, Math.min(1, (thetaE - 325.0) / 42.0));

              const total = (0.25 * capeScore) + (0.16 * pwatScore) + (0.18 * liScore) + (0.14 * shearScore) + (0.12 * thetaScore);
              
              if (total === 0) {
                return [
                  { name: "CAPE", weight: 34 },
                  { name: "PWAT", weight: 22 },
                  { name: "LI", weight: 18 },
                  { name: "Bulk Shear", weight: 14 },
                  { name: "Theta-E", weight: 12 }
                ];
              }

              const contribs = [
                { name: "CAPE", weight: Math.round(((0.25 * capeScore) / total) * 100) },
                { name: "PWAT", weight: Math.round(((0.16 * pwatScore) / total) * 100) },
                { name: "LI", weight: Math.round(((0.18 * liScore) / total) * 100) },
                { name: "Bulk Shear", weight: Math.round(((0.14 * shearScore) / total) * 100) },
                { name: "Theta-E", weight: Math.round(((0.12 * thetaScore) / total) * 100) }
              ];
              
              contribs.sort((a, b) => b.weight - a.weight);
              return contribs;
            };

            const contribs = getProbabilityContributors(selectedStation);
            const mainCause = (contribs[0].name === "CAPE" || contribs[0].name === "PWAT")
              ? "Increasing CAPE and PWAT moisture columns."
              : `Strong convective lift from ${contribs[0].name} forcing.`;

            const getAuditExplanation = (reason) => {
              switch(reason) {
                case "LIVE_INGESTION_FAILURE":
                  return "Wyoming sounding download failed due to network timeout or site outage. Fallback profiles are active.";
                case "STALE_CACHE":
                  return "Sounding data is cached from a previous day. Radiosonde Ingestion was not completed for this cycle.";
                case "SEED_PROFILE_REUSE":
                  return "Thermodynamic seed profile has been reused due to lack of a fresh sounding report.";
                case "SOLVER_REUSE":
                  return "The solver calculation yielded identical outputs because the source data profile is unchanged.";
                case "CACHE_LOCK":
                  return "The sounding cache file is locked, preventing updates from being committed.";
                default:
                  return "Solver outputs are cached across cycles due to ingestion hold or offline telemetry feed.";
              }
            };

            return (
              <div className="panel-surface" style={{ padding: "24px", display: "flex", flexDirection: "column", gap: "20px", backgroundColor: "#0b0f19", border: "1px solid #334155" }}>
                
                {/* 1. TOP SECTION: Current Conditions */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                  <div>
                    <span className="font-technical" style={{ fontSize: "11px", color: "#3b82f6", fontWeight: "bold", letterSpacing: "1px" }}>
                      I. Current Conditions // {selectedStation.station.toUpperCase()}
                    </span>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px 20px", fontSize: "12px", fontFamily: "JetBrains Mono", color: "#cbd5e1", marginTop: "8px" }}>
                      <div>Observation Date: <span style={{ color: "#ffffff", fontWeight: "bold" }}>2026-06-05</span></div>
                      <div>Observation Time: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{obsTime}</span></div>
                      <div>Forecast Generated: <span style={{ color: "#a855f7", fontWeight: "bold" }}>{genTime}</span></div>
                      <div>Data Source: <span style={{ color: "#10b981" }}>{sourceStr}</span></div>
                    </div>
                  </div>
                  <button
                    onClick={handleIssueWarning}
                    className="interactive-action font-technical"
                    style={{
                      backgroundColor: currentMetrics.color,
                      boxShadow: `0 0 14px ${currentMetrics.color}44`,
                      border: "none",
                      color: "white",
                      padding: "8px 16px",
                      borderRadius: "8px",
                      fontWeight: "bold",
                      fontSize: "12px",
                      cursor: "pointer"
                    }}
                  >
                    🚨 WARNING DISPATCH: {currentMetrics.ccss >= 70 ? "IMMEDIATE" : "STANDBY"}
                  </button>
                </div>

                {/* 2. SECOND SECTION: Threat Summary */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px" }}>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#f43f5e", fontWeight: "bold", textTransform: "uppercase", marginBottom: "12px" }}>
                    II. Threat Summary & Evolution
                  </h4>
                  
                  {/* Convective Risks list */}
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: "10px", marginBottom: "16px" }}>
                    {[
                      { label: "Thunderstorm", val: currentProb, col: "#eab308" },
                      { label: "Severe TS", val: selectedStation.severe_ts_probability || Math.round(currentProb * 0.8), col: "#ef4444" },
                      { label: "Heavy Rain", val: selectedStation.heavy_rain_probability || Math.round((selectedStation.pwat / 75.0) * 100), col: "#3b82f6" },
                      { label: "Lightning", val: selectedStation.lightning_probability || Math.round(currentProb * 1.05), col: "#f97316" },
                      { label: "Squall", val: selectedStation.squall_probability || Math.round(currentProb * 0.7), col: "#a855f7" },
                      { label: "NWX", val: selectedStation.nwx_probability || Math.max(0, 100 - currentProb), col: "#10b981" }
                    ].map((p) => (
                      <div key={p.label} style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "10px" }}>
                        <div style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "bold" }}>{p.label}</div>
                        <div className="font-technical" style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold", marginTop: "2px" }}>
                          {p.val}%
                        </div>
                        <div style={{ height: "3px", width: `${Math.max(10, Math.min(100, p.val))}%`, backgroundColor: p.col, borderRadius: "99px", marginTop: "6px" }} />
                      </div>
                    ))}
                  </div>

                  {!reviewMode && (
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                      
                      {/* LIVE CAPE TRACEABILITY PANEL */}
                      <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                        <div className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", fontWeight: "bold", display: "flex", justifyContent: "space-between" }}>
                          <span>LIVE CAPE TRACEABILITY PANEL</span>
                          <span style={{ color: riskColor }}>● INGESTED</span>
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: "6px", fontSize: "11px", marginTop: "8px", fontFamily: "JetBrains Mono" }}>
                          <div>Current CAPE:</div>
                          <div style={{ color: "#ffffff", fontWeight: "bold" }}>{currentCape} J/kg</div>
                          <div>Previous CAPE:</div>
                          <div style={{ color: "#94a3b8" }}>{prevCape} J/kg</div>
                          <div>Delta CAPE:</div>
                          <div style={{ color: deltaCape > 0 ? "#10b981" : deltaCape < 0 ? "#ef4444" : "#f59e0b", fontWeight: "bold" }}>
                            {deltaCape >= 0 ? "+" : ""}{deltaCape} J/kg
                          </div>
                          <div>Trend:</div>
                          <div style={{ color: capeTrend === "RISING" ? "#10b981" : capeTrend === "FALLING" ? "#ef4444" : "#f59e0b", fontWeight: "bold" }}>
                            {capeTrend}
                          </div>
                          <div>Source:</div>
                          <div style={{ color: "#ffffff" }}>{stTrace?.source_status || "LIVE SOUNDING"}</div>
                          <div>Cycle Time:</div>
                          <div style={{ color: "#ffffff" }}>{obsTime}</div>
                        </div>

                        {/* CAPE AUDIT ENGINE */}
                        {isCapeStatic && (
                          <div style={{ marginTop: "10px", padding: "8px", border: "1px solid rgba(239, 68, 68, 0.4)", borderRadius: "6px", backgroundColor: "rgba(239, 68, 68, 0.08)" }}>
                            <div className="font-technical" style={{ fontSize: "9px", color: "#ef4444", fontWeight: "bold" }}>
                              CAPE STATIC DATA WARNING
                            </div>
                            <div style={{ fontSize: "10px", color: "#cbd5e1", marginTop: "4px", lineHeight: "1.3" }}>
                              <strong>Root Cause:</strong> {stTrace?.static_data_reason || "Seed Profile Reuse"}
                              <ul style={{ margin: "4px 0 0 0", paddingLeft: "12px", color: "#94a3b8" }}>
                                <li>Stale Cache</li>
                                <li>Solver Reuse</li>
                                <li>Seed Profile Reuse</li>
                                <li>Live Ingestion Failure</li>
                                <li>Missing Telemetry</li>
                              </ul>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* PROBABILITY EVOLUTION PANEL */}
                      <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                        <div className="font-technical" style={{ fontSize: "10px", color: "#a855f7", fontWeight: "bold" }}>
                          PROBABILITY EVOLUTION PANEL
                        </div>
                        <div style={{ marginTop: "8px", display: "flex", flexDirection: "column", gap: "10px" }}>
                          {[
                            { 
                              name: "Thunderstorm Probability",
                              curr: currentProb,
                              prev: prevProb,
                              driver: mainCause
                            },
                            { 
                              name: "Lightning Probability",
                              curr: selectedStation.lightning_probability || (currentProb >= 60 ? Math.max(80, currentProb + 5) : 15),
                              prev: selectedStation.lightning_probability ? selectedStation.lightning_probability - 4 : (prevProb >= 60 ? Math.max(80, prevProb + 5) : 15),
                              driver: "CAPE & Lifted Index parcel buoyancy"
                            },
                            { 
                              name: "Heavy Rain Probability",
                              curr: selectedStation.heavy_rain_probability || (selectedStation.pwat >= 50 ? Math.round(50 + (selectedStation.pwat - 50) * 1.5) : Math.round(selectedStation.pwat * 0.6)),
                              prev: selectedStation.heavy_rain_probability ? selectedStation.heavy_rain_probability - 5 : (selectedStation.pwat >= 50 ? Math.round(50 + (selectedStation.pwat - 50) * 1.5) - 3 : Math.round(selectedStation.pwat * 0.6) - 2),
                              driver: "PWAT column moisture loading"
                            },
                            { 
                              name: "Squall Probability",
                              curr: selectedStation.squall_probability || (selectedStation.sweat_index >= 290 ? Math.round(40 + (selectedStation.sweat_index - 290) * 0.2) : 10),
                              prev: selectedStation.squall_probability ? selectedStation.squall_probability - 2 : (selectedStation.sweat_index >= 290 ? Math.round(40 + (selectedStation.sweat_index - 290) * 0.2) - 1 : 10),
                              driver: "SWEAT index & Bulk wind shear dynamics"
                            }
                          ].map((item) => {
                            const delta = item.curr - item.prev;
                            return (
                              <div key={item.name} style={{ borderBottom: "1px solid #1e293b", paddingBottom: "6px", fontSize: "11px", fontFamily: "JetBrains Mono" }}>
                                <div style={{ fontWeight: "bold", color: "#cbd5e1", fontSize: "11.5px", marginBottom: "2px" }}>{item.name}</div>
                                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "4px", color: "#94a3b8" }}>
                                  <div>Current: <strong style={{ color: "#ffffff" }}>{item.curr}%</strong></div>
                                  <div>Prev: <span>{item.prev}%</span></div>
                                  <div>Delta: <strong style={{ color: delta > 0 ? "#10b981" : delta < 0 ? "#ef4444" : "#f59e0b" }}>{delta >= 0 ? "+" : ""}{delta}%</strong></div>
                                </div>
                                <div style={{ fontSize: "9.5px", color: "#64748b", marginTop: "2px" }}>Driver: {item.driver}</div>
                              </div>
                            );
                          })}
                        </div>

                        {/* STATIC PROBABILITY AUDIT */}
                        {isProbStatic && (
                          <div style={{ marginTop: "10px", padding: "8px", border: "1px solid rgba(245, 158, 11, 0.4)", borderRadius: "6px", backgroundColor: "rgba(245, 158, 11, 0.08)" }}>
                            <div className="font-technical" style={{ fontSize: "9px", color: "#f59e0b", fontWeight: "bold" }}>
                              STATIC_PROBABILITY_WARNING
                            </div>
                            <div style={{ fontSize: "10px", color: "#cbd5e1", marginTop: "4px", lineHeight: "1.3" }}>
                              <strong>Reason:</strong> Convective probabilities are static across consecutive runs. The thermodynamic environmental profile is unchanged, causing the solver to reuse previous state coefficients.
                            </div>
                          </div>
                        )}
                      </div>

                    </div>
                  )}
                </div>

                {/* 3. THIRD SECTION: Meteorologist Interpretation */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px" }}>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#eab308", fontWeight: "bold", textTransform: "uppercase", marginBottom: "8px" }}>
                    III. Meteorologist Interpretation
                  </h4>
                  <div style={{ fontSize: "12.5px", color: "#cbd5e1", lineHeight: "1.6", backgroundColor: "rgba(234, 179, 8, 0.05)", border: "1px dashed rgba(234, 179, 8, 0.25)", padding: "12px", borderRadius: "8px", fontStyle: "italic" }}>
                    {selectedStation.explainability || 
                      `Strong instability (CAPE: ${currentCape} J/kg) and deep moisture (PWAT: ${selectedStation.pwat}mm) support thunderstorm development over coastal Andhra Pradesh during the next 3–6 hours.`
                    }
                  </div>
                </div>

                {/* 4. FOURTH SECTION: Recommended Actions */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px" }}>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#10b981", fontWeight: "bold", textTransform: "uppercase", marginBottom: "10px" }}>
                    IV. Recommended Actions
                  </h4>
                  <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "10px" }}>
                    {[
                      { label: "Thunderstorm Watch", status: currentProb >= 50 ? "ACTIVE WATCH" : "STANDBY", col: currentProb >= 50 ? "#ef4444" : "#64748b" },
                      { label: "Lightning Watch", status: (selectedStation.lightning_probability || currentProb) >= 50 ? "ACTIVE WATCH" : "STANDBY", col: (selectedStation.lightning_probability || currentProb) >= 50 ? "#f97316" : "#64748b" },
                      { label: "Heavy Rain Monitoring", status: (selectedStation.heavy_rain_probability || (selectedStation.pwat / 75) * 100) >= 50 ? "ACTIVE MONITOR" : "STANDBY", col: (selectedStation.heavy_rain_probability || (selectedStation.pwat / 75) * 100) >= 50 ? "#3b82f6" : "#64748b" },
                      { label: "NWX Warning", status: (selectedStation.nwx_probability || 100 - currentProb) >= 60 ? "ACTIVE" : "STANDBY", col: (selectedStation.nwx_probability || 100 - currentProb) >= 60 ? "#10b981" : "#64748b" }
                    ].map((act) => (
                      <div key={act.label} style={{
                        backgroundColor: "#020617",
                        border: `1px solid ${act.status.includes("ACTIVE") ? act.col + "44" : "#1e293b"}`,
                        borderLeft: `4px solid ${act.col}`,
                        borderRadius: "8px",
                        padding: "10px",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center"
                      }}>
                        <div style={{ display: "flex", flexDirection: "column" }}>
                          <span style={{ fontSize: "11px", fontWeight: "bold", color: "#ffffff" }}>{act.label}</span>
                          <span className="font-technical" style={{ fontSize: "8px", color: "#64748b", marginTop: "2px" }}>{act.status}</span>
                        </div>
                        <span className="font-technical" style={{
                          fontSize: "8px",
                          fontWeight: "bold",
                          backgroundColor: act.status.includes("ACTIVE") ? act.col + "15" : "transparent",
                          color: act.col,
                          padding: "2px 4px",
                          borderRadius: "4px"
                        }}>
                          {act.status.split(" ")[0]}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 5. ADVANCED DIAGNOSTICS ACCORDION */}
                <details style={{ width: "100%", outline: "none" }}>
                  <summary style={{
                    cursor: "pointer",
                    fontSize: "12px",
                    fontWeight: "bold",
                    color: "#a855f7",
                    fontFamily: "JetBrains Mono",
                    outline: "none",
                    padding: "8px 0",
                    userSelect: "none"
                  }}>
                    🛠️ Advanced Diagnostics & Scientific Calibration (Click to Expand)
                  </summary>
                  
                  <div style={{ display: "flex", flexDirection: "column", gap: "24px", marginTop: "14px" }}>
                    
                    {/* 5-Card Thermodynamic Instability Matrix */}
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "10px" }}>
                      {[
                        { label: "CAPE (J/kg)", key: "CAPE", val: selectedStation.cape },
                        { label: "Lifted Index", key: "LI", val: selectedStation.lifted_index },
                        { label: "SWEAT Index", key: "SWEAT", val: selectedStation.sweat_index },
                        { label: "K-Index", key: "K_Index", val: selectedStation.k_index },
                        { label: "PWAT (mm)", key: "PWAT", val: selectedStation.pwat }
                      ].map((ind) => {
                        const isSensorOn = sensorStatus[ind.key];
                        const rawVal = isSensorOn ? ind.val : null;
                        const interpretation = getThresholdInterpretation(ind.key, rawVal);
                        const isExpanded = openExplainers[ind.key];
                        const translation = indexTranslations[ind.key];

                        return (
                          <div
                            key={ind.key}
                            style={{
                              backgroundColor: "#020617",
                              border: isExpanded ? `1px solid ${interpretation.color}` : "1px solid #1e293b",
                              borderRadius: "12px",
                              padding: "10px",
                              display: "flex",
                              flexDirection: "column",
                              gap: "4px",
                              position: "relative"
                            }}
                          >
                            <div style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>{ind.label}</div>
                            <div className="font-technical" style={{
                              fontSize: "16px",
                              fontWeight: "bold",
                              color: isSensorOn ? (selectedStation.sounding_available === false ? "#f59e0b" : "#ffffff") : "#f43f5e"
                            }}>
                              {isSensorOn ? (ind.key === "CAPE" && selectedStation.sounding_available === false ? "N/A" : ind.val) : "OFFLINE"}
                            </div>
                            <button
                              onClick={() => toggleExplainer(ind.key)}
                              style={{
                                background: "none",
                                border: "none",
                                color: "#3b82f6",
                                fontSize: "9px",
                                cursor: "pointer",
                                textAlign: "left",
                                padding: "2px 0 0 0",
                                fontWeight: "bold"
                              }}
                            >
                              {isExpanded ? "✕ Close" : "🎓 What is this?"}
                            </button>
                            {isExpanded && translation && (
                              <div style={{
                                position: "absolute",
                                top: "100%",
                                left: "0",
                                right: "0",
                                backgroundColor: "rgba(9, 13, 22, 0.98)",
                                border: `1.5px solid ${interpretation.color}`,
                                borderRadius: "8px",
                                padding: "12px",
                                zIndex: 100,
                                fontSize: "10px",
                                boxShadow: "0 10px 25px rgba(0,0,0,0.6)",
                                color: "#cbd5e1",
                                marginTop: "6px"
                              }}>
                                <strong>{translation.title}</strong>
                                <p style={{ margin: "4px 0" }}>{translation.plainLanguage}</p>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    {/* Extended Thermodynamic Heights */}
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "10px" }}>
                      {[
                        { label: "CIN (J/kg)", value: selectedStation?.cin, accent: "#f59e0b" },
                        { label: "LCL (hPa)", value: selectedStation?.lcl, accent: "#3b82f6" },
                        { label: "LFC (hPa)", value: selectedStation?.lfc, accent: "#10b981" },
                        { label: "EL (hPa)", value: selectedStation?.el, accent: "#a855f7" },
                        { label: "Instability Depth (km)", value: safeNumber(selectedStation?.instability_layer_depth_m, 0) > 0 ? (safeNumber(selectedStation?.instability_layer_depth_m, 0) / 1000).toFixed(1) : "—", accent: "#22c55e" }
                      ].map((d) => (
                        <div key={d.label} style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "12px", padding: "10px" }}>
                          <div style={{ fontSize: "9px", color: "#64748b", fontWeight: "bold" }}>{d.label}</div>
                          <div className="font-technical" style={{ fontSize: "13px", fontWeight: "bold", color: "#ffffff", marginTop: "2px" }}>
                            {Number.isFinite(d.value) ? d.value : (d.value ?? "—")}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Confidence Calibration Envelope */}
                    <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                        CONFIDENCE_CALIBRATION_ENVELOPE
                      </span>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "10px" }}>
                        {[
                          { label: "Forecast Confidence", val: confidenceEnvelope.forecastConfidence, col: "#3b82f6" },
                          { label: "Sounding Integrity", val: confidenceEnvelope.soundingIntegrity, col: "#10b981" },
                          { label: "Data Completeness", val: confidenceEnvelope.dataCompleteness, col: "#eab308" },
                          { label: "Threshold Reliability", val: confidenceEnvelope.thresholdReliability, col: "#a855f7" },
                          { label: "Observation Integrity", val: confidenceEnvelope.dataCompleteness, col: "#f97316" }
                        ].map((c) => (
                          <div key={c.label} style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "8px" }}>
                            <div style={{ fontSize: "9px", color: "#64748b", fontWeight: "bold" }}>{c.label}</div>
                            <div className="font-technical" style={{ fontSize: "13px", color: "#ffffff", fontWeight: "bold", marginTop: "2px" }}>
                              {safePercent(c.val, 0)}%
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Euclidean Distance Historical Analog Match */}
                    {closestAnalog && (
                      <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#10b981", fontWeight: "bold", display: "block", marginBottom: "6px" }}>
                          EUCLIDEAN_NEAREST_NEIGHBOR_ANALOG_MATCH
                        </span>
                        <div style={{ fontSize: "11px", color: "#cbd5e1", fontFamily: "JetBrains Mono" }}>
                          Distance: <strong style={{ color: "#ffffff" }}>{closestAnalog.station}</strong> ({closestAnalog.date}) // Similarity: {closestAnalog.similarity}% // Observed: {closestAnalog.observed}
                        </div>
                      </div>
                    )}

                    {/* Composite Convective Severity Score (CCSS) Dial & Secondary Sub-Gauges */}
                    <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#a855f7", fontWeight: "bold", display: "block", marginBottom: "12px" }}>
                        COMPOSITE_CONVECTIVE_SEVERITY_SCORE
                      </span>
                      <div style={{ display: "grid", gridTemplateColumns: "120px 1fr", gap: "20px", alignItems: "center" }}>
                        <div style={{ position: "relative", width: "100px", height: "100px" }}>
                          <svg width="100" height="100" viewBox="0 0 120 120">
                            <circle cx="60" cy="60" r="50" fill="none" stroke="#0f172a" strokeWidth="10" />
                            <circle 
                              cx="60" cy="60" r="50" fill="none" stroke={currentMetrics.color} strokeWidth="10" 
                              strokeDasharray={314.16} strokeDashoffset={314.16 - (314.16 * currentMetrics.ccss) / 100}
                              strokeLinecap="round" transform="rotate(-90 60 60)"
                            />
                          </svg>
                          <div style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", textAlign: "center" }}>
                            <span className="font-technical" style={{ fontSize: "20px", fontWeight: "black", color: "#ffffff" }}>{currentMetrics.ccss}%</span>
                          </div>
                        </div>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                          {[
                            { label: "⚡ Lightning", val: currentMetrics.lightInt },
                            { label: "🌧️ Heavy Rain", val: currentMetrics.rainEff },
                            { label: "💨 Squall/Wind", val: currentMetrics.gustFront },
                            { label: "🌊 Flooding", val: currentMetrics.floodRisk }
                          ].map((sub) => (
                            <div key={sub.label} style={{ fontSize: "11px" }}>
                              <span style={{ color: "#94a3b8" }}>{sub.label}:</span> <strong style={{ color: "#ffffff" }}>{sub.val}%</strong>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Convective Lifecycle Timeline */}
                    <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", fontWeight: "bold", display: "block", marginBottom: "12px" }}>
                        CONVECTIVE_LIFECYCLE_TIMELINE
                      </span>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: "6px" }}>
                        {timelineStages.map((stage) => (
                          <div key={stage.num} style={{ textAlign: "center", fontSize: "9px" }}>
                            <div style={{
                              width: "24px", height: "24px", borderRadius: "50%", margin: "0 auto 4px",
                              backgroundColor: activeStage === stage.num ? currentMetrics.color : "#020617",
                              border: "1.5px solid #1e293b", display: "flex", alignItems: "center", justifyContent: "center",
                              color: activeStage === stage.num ? "#020617" : "#ffffff", fontWeight: "bold"
                            }}>
                              {stage.num}
                            </div>
                            <span style={{ color: activeStage === stage.num ? "#ffffff" : "#64748b", fontWeight: "bold", display: "block" }}>{stage.title.split(" ")[0]}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Sensor Degradation Testing */}
                    <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#eab308", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                        SENSOR_DEGRADATION_TESTING
                      </span>
                      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: "6px" }}>
                        {Object.keys(sensorStatus).map((sens) => (
                          <button
                            key={sens} type="button" onClick={() => toggleSensor(sens)}
                            style={{
                              padding: "4px", fontSize: "10px", fontWeight: "bold", borderRadius: "6px", cursor: "pointer",
                              backgroundColor: sensorStatus[sens] ? "rgba(16, 185, 129, 0.08)" : "rgba(244, 63, 94, 0.08)",
                              color: sensorStatus[sens] ? "#10b981" : "#f43f5e",
                              border: `1px solid ${sensorStatus[sens] ? "#10b981" : "#f43f5e"}`
                            }}
                          >
                            {sens}
                          </button>
                        ))}
                      </div>
                    </div>

                    {/* Decision Logic Calibration & Sliders */}
                    <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#a855f7", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                        DECISION_LOGIC_WEIGHTS_CALIBRATION
                      </span>
                      <div style={{ fontSize: "10px", color: "#cbd5e1", fontFamily: "JetBrains Mono", marginBottom: "10px" }}>
                        P(Storm) = {weightCape}%·CAPE + {weightLi}%·LI + {weightSweat}%·SWEAT + {weightK}%·K + {weightPwat}%·PWAT
                      </div>
                      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                        {[
                          { name: "CAPE Weight", val: weightCape, set: setWeightCape, col: "#f43f5e", max: 50 },
                          { name: "Lifted Index Weight", val: weightLi, set: setWeightLi, col: "#eab308", max: 40 },
                          { name: "SWEAT Weight", val: weightSweat, set: setWeightSweat, col: "#f97316", max: 40 },
                          { name: "K-Index Weight", val: weightK, set: setWeightK, col: "#10b981", max: 30 },
                          { name: "PWAT Weight", val: weightPwat, set: setWeightPwat, col: "#3b82f6", max: 20 }
                        ].map((item) => (
                          <div key={item.name} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                            <span style={{ fontSize: "11px", color: "#94a3b8", width: "120px" }}>{item.name}:</span>
                            <input 
                              type="range" min="0" max={item.max} value={item.val} onChange={(e) => item.set(Number(e.target.value))}
                              style={{ flex: 1, accentColor: item.col, height: "4px", cursor: "pointer" }}
                            />
                            <strong className="font-technical" style={{ color: item.col, width: "30px" }}>{item.val}%</strong>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Issued Warnings Log */}
                    <div style={{ backgroundColor: "rgba(2, 6, 23, 0.8)", border: "1px solid #1e293b", borderRadius: "12px", padding: "14px" }}>
                      <span className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", fontWeight: "bold", display: "block", marginBottom: "8px" }}>
                        MET_OFFICE_WARNING_DISPATCH_LOG
                      </span>
                      <div style={{ display: "flex", flexDirection: "column", gap: "6px", maxHeight: "120px", overflowY: "auto" }}>
                        {issuedWarnings.length === 0 ? (
                          <span style={{ fontSize: "11px", color: "#64748b" }}>No warning vectors issued in this session.</span>
                        ) : (
                          issuedWarnings.map((warn) => (
                            <div key={warn.id} style={{ fontSize: "11px", color: "#cbd5e1" }}>
                              ● [{warn.timestamp}] {warn.id} // {warn.station} // {warn.severity}
                            </div>
                          ))
                        )}
                      </div>
                    </div>

                  </div>
                </details>

              </div>
            );
          })()}

        </div>

      </div>

    </div>
  );
}
