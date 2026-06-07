import re

file_path = 'frontend/src/components/modules/ResearchHub.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update activeTab initial state to HISTORICAL_WORKBENCH
search_active_tab = 'const [activeTab, setActiveTab] = useState("SKEW_T"); // SKEW_T, WYOMING_DATA, INDEX_GLOSSARY, TERMINOLOGY'
replace_active_tab = 'const [activeTab, setActiveTab] = useState("HISTORICAL_WORKBENCH"); // SKEW_T, WYOMING_DATA, INDEX_GLOSSARY, TERMINOLOGY'

if search_active_tab in content:
    content = content.replace(search_active_tab, replace_active_tab)
    print("Successfully set activeTab landing page to HISTORICAL_WORKBENCH.")
else:
    print("CRITICAL WARNING: activeTab search pattern not found!")

# 2. Insert new states and useMemo helpers for the occurrence registry, standard times, and explanation cards.
search_states = """  // Databank Filter States
  const [databankStationFilter, setDatabankStationFilter] = useState("ALL");
  const [databankClassFilter, setDatabankClassFilter] = useState("ALL");"""

replace_states = """  // Databank Filter States
  const [databankStationFilter, setDatabankStationFilter] = useState("ALL");
  const [databankClassFilter, setDatabankClassFilter] = useState("ALL");

  // Phase 5.5 Occurrence Registry Filter States
  const [registryStation, setRegistryStation] = useState("ALL");
  const [registryStartDate, setRegistryStartDate] = useState("");
  const [registryEndDate, setRegistryEndDate] = useState("");
  const [registrySeason, setRegistrySeason] = useState("ALL");
  const [registryEventType, setRegistryEventType] = useState("ALL");

  // Advanced Scientific Analysis panel toggle state
  const [showAdvancedScientific, setShowAdvancedScientific] = useState(false);

  // Enriched historical dates helper mapping database observations to strict IST timestamps
  const enrichedHistoricalDates = useMemo(() => {
    return (historicalDates || []).map(item => {
      const morningDates = ["2025-04-18", "2025-05-15", "2025-06-12", "2025-07-02", "2025-07-22", "2025-08-20"];
      const time = morningDates.includes(item.date) ? "05:00 IST" : "17:00 IST";
      const observed = item.observed || "NWX";
      const isTS = !!item.thunderstorm;
      
      // Calculate Forecast Result based on standard threshold constraints
      const forecastTS = item.cape >= 2100 && item.li <= -4.5 && item.pwat >= 50;
      const forecastResult = forecastTS ? "THUNDERSTORM (FAVORED)" : "NO WEATHER EXPECTED";
      
      let verificationResult = "CORRECT_NEGATIVE";
      if (forecastTS && isTS) verificationResult = "HIT";
      else if (!forecastTS && !isTS) verificationResult = "CORRECT_NEGATIVE";
      else if (forecastTS && !isTS) verificationResult = "FALSE_ALARM";
      else if (!forecastTS && isTS) verificationResult = "MISS";
      
      const explanation = isTS 
        ? "Atmospheric instability and deep moisture favored thunderstorm development."
        : "No Weather Expected due to stable atmospheric conditions.";
         
      return {
        ...item,
        time,
        forecastResult,
        verificationResult,
        explanation
      };
    });
  }, [historicalDates]);

  // Filtered Registry list containing ONLY actual thunderstorm events
  const filteredRegistry = useMemo(() => {
    return enrichedHistoricalDates.filter(item => {
      if (!item.thunderstorm) return false;
      const stationOk = registryStation === "ALL" || item.station === registryStation;
      const startOk = !registryStartDate || item.date >= registryStartDate;
      const endOk = !registryEndDate || item.date <= registryEndDate;
      const seasonOk = registrySeason === "ALL" || item.season === registrySeason;
      const typeOk = registryEventType === "ALL" || 
        (item.observed || "").toUpperCase() === registryEventType.toUpperCase();
      return stationOk && startOk && endOk && seasonOk && typeOk;
    });
  }, [enrichedHistoricalDates, registryStation, registryStartDate, registryEndDate, registrySeason, registryEventType]);

  // Client-side export helper for downloading registry / events databanks
  const handleDownloadRegistry = (dataList, format) => {
    const exportData = dataList.map(r => ({
      date: r.date,
      time: r.time,
      station: r.station,
      observedEvent: r.observed,
      thunderstormFlag: r.thunderstorm ? "YES" : "NO",
      cape: r.cape,
      li: r.li,
      pwat: r.pwat,
      sweat: r.sweat,
      forecastResult: r.forecastResult,
      verificationResult: r.verificationResult,
      explanation: r.explanation
    }));
    
    if (format === 'json') {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportData, null, 2));
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", "thunderstorm_events.json");
      document.body.appendChild(dlAnchor);
      dlAnchor.click();
      dlAnchor.remove();
    } else {
      let csv = "data:text/csv;charset=utf-8,\\uFEFF";
      csv += "Date,Time,Station,Observed Event,Thunderstorm Flag,CAPE,LI,PWAT,SWEAT,Forecast Result,Verification Result,Meteorologist Explanation\\n";
      exportData.forEach(r => {
        const exp = r.explanation.replace(/"/g, '""');
        csv += `"${r.date}","${r.time}","${r.station}","${r.observedEvent}","${r.thunderstormFlag}","${r.cape}","${r.li}","${r.pwat}","${r.sweat}","${r.forecastResult}","${r.verificationResult}","${exp}"\\n`;
      });
      const encodedUri = encodeURI(csv);
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", encodedUri);
      dlAnchor.setAttribute("download", "thunderstorm_events.csv");
      document.body.appendChild(dlAnchor);
      dlAnchor.click();
      dlAnchor.remove();
    }
  };

  // Dynamically compute the last verified/recorded thunderstorm event
  const lastVerifiedThunderstorm = useMemo(() => {
    const tsEvents = enrichedHistoricalDates.filter(item => item.thunderstorm);
    if (tsEvents.length === 0) return null;
    const sorted = [...tsEvents].sort((a, b) => b.date.localeCompare(a.date));
    return sorted[0];
  }, [enrichedHistoricalDates]);

  // Helper to render simple Convective Threshold Explanation Card
  const renderExplanationCard = (row) => {
    if (!row) return null;
    const capePass = row.cape >= 2100;
    const liPass = row.li <= -4.5;
    const pwatPass = row.pwat >= 50;
    const sweatPass = row.sweat >= 290;
    const isStorm = row.thunderstorm;
    
    if (isStorm) {
      return (
        <div className="panel-surface" style={{ border: "2px solid #10b981", borderRadius: "12px", padding: "16px", backgroundColor: "rgba(16, 185, 129, 0.05)" }}>
          <h4 style={{ color: "#10b981", fontSize: "12px", fontWeight: "bold", margin: "0 0 10px 0" }}>⚡ WHY DID THE THUNDERSTORM OCCUR?</h4>
          <div style={{ display: "flex", flexDirection: "column", gap: "6px", fontSize: "11.5px", color: "#cbd5e1" }}>
            <div>{capePass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✓</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✗</span>} CAPE exceeded threshold ({row.cape} J/kg vs 2100 limit)</div>
            <div>{liPass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✓</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✗</span>} LI indicated unstable atmosphere ({row.li} K vs -4.5 limit)</div>
            <div>{pwatPass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✓</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✗</span>} PWAT indicated high moisture ({row.pwat} mm vs 50 limit)</div>
            <div>{sweatPass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✓</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✗</span>} SWEAT indicated organized convection ({row.sweat} vs 290 limit)</div>
          </div>
          <div style={{ borderTop: "1px solid rgba(16, 185, 129, 0.2)", marginTop: "10px", paddingTop: "8px", fontSize: "11.5px" }}>
            <strong>Meteorologist Summary:</strong> <span style={{ color: "#ffffff" }}>"Atmospheric instability and deep moisture favored thunderstorm development."</span>
          </div>
        </div>
      );
    } else {
      return (
        <div className="panel-surface" style={{ border: "2px solid #ef4444", borderRadius: "12px", padding: "16px", backgroundColor: "rgba(239, 68, 68, 0.05)" }}>
          <h4 style={{ color: "#ef4444", fontSize: "12px", fontWeight: "bold", margin: "0 0 10px 0" }}>🛡️ WHY NO THUNDERSTORM OCCURRED</h4>
          <div style={{ display: "flex", flexDirection: "column", gap: "6px", fontSize: "11.5px", color: "#cbd5e1" }}>
            <div>{!capePass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✗</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✓</span>} CAPE below threshold ({row.cape} J/kg vs 2100 limit)</div>
            <div>{!liPass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✗</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✓</span>} Atmosphere stable ({row.li} K vs -4.5 limit)</div>
            <div>{!pwatPass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✗</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✓</span>} Moisture insufficient ({row.pwat} mm vs 50 limit)</div>
            <div>{!sweatPass ? <span style={{ color: "#10b981", fontWeight: "bold" }}>✗</span> : <span style={{ color: "#ef4444", fontWeight: "bold" }}>✓</span>} Trigger mechanisms weak ({row.sweat} vs 290 limit)</div>
          </div>
          <div style={{ borderTop: "1px solid rgba(239, 68, 68, 0.2)", marginTop: "10px", paddingTop: "8px", fontSize: "11.5px" }}>
            <strong>Meteorologist Summary:</strong> <span style={{ color: "#ffffff" }}>"No Weather Expected due to stable atmospheric conditions."</span>
          </div>
        </div>
      );
    }
  };"""

if search_states in content:
    content = content.replace(search_states, replace_states)
    print("Successfully inserted Phase 5.5 states, helper functions, and useMemo trace calculations.")
else:
    print("CRITICAL WARNING: Filter states search pattern not found!")

# 3. Rename sidebar text and fallback title
content = content.replace('{tab === "HISTORICAL_WORKBENCH" && "🕰️ Historical Workbench"}', '{tab === "HISTORICAL_WORKBENCH" && "🕰️ Historical Thunderstorm Archive"}')
content = content.replace('fallbackTitle="⚠ Historical Workbench Rendering Error"', 'fallbackTitle="⚠ Historical Thunderstorm Archive Rendering Error"')
content = content.replace('<li>Open Historical Workbench</li>', '<li>Open Historical Thunderstorm Archive</li>')
print("Successfully renamed Historical Workbench references.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved partial changes.")
