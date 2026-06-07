import { useEffect, useState, useRef } from "react";
import axios from "axios";

// Import layout components
import Header from "./components/layout/Header";
import Sidebar from "./components/layout/Sidebar";

// Import modules
import RadarConsole from "./components/modules/RadarConsole";
import PredictorEngine from "./components/modules/PredictorEngine";
import AnalyticsDeck from "./components/modules/AnalyticsDeck";
import ResearchHub from "./components/modules/ResearchHub";
import HealthConsole from "./components/modules/HealthConsole";
import Phase3OpsModule from "./components/modules/Phase3OpsModule";
import IMDReviewSummaryDeck from "./components/modules/IMDReviewSummaryDeck";
import { validateForecastPayload } from "./utils/atmosphericUtils";
import ErrorBoundary from "./components/layout/ErrorBoundary";

import Login from "./pages/Login";
import Signup from "./pages/Signup";

// ==========================================
// HIGH-FIDELITY ATMOSPHERIC FALLBACK DATA
// ==========================================
const fallbackForecastData = [
  { station: "Visakhapatnam", station_code: "43150", cape: 2850, lifted_index: -7.5, sweat_index: 340, k_index: 38, pwat: 68, forecast: "SEVERE THUNDERSTORM RISK", storm_probability: 85 },
  { station: "Chennai", station_code: "43279", cape: 1650, lifted_index: -4.2, sweat_index: 220, k_index: 30, pwat: 52, forecast: "MODERATE THUNDERSTORM RISK", storm_probability: 48 },
  { station: "Kolkata", station_code: "42809", cape: 3100, lifted_index: -8.8, sweat_index: 390, k_index: 42, pwat: 75, forecast: "SEVERE THUNDERSTORM RISK", storm_probability: 92 },
  { station: "Hyderabad", station_code: "43128", cape: 950, lifted_index: -2.1, sweat_index: 180, k_index: 27, pwat: 40, forecast: "LOW THUNDERSTORM RISK", storm_probability: 25 },
  { station: "Machilipatnam", station_code: "43185", cape: 2200, lifted_index: -5.2, sweat_index: 280, k_index: 34, pwat: 55, forecast: "HIGH THUNDERSTORM RISK", storm_probability: 68 }
];

const fallbackHistoryData = [
  { station: "Visakhapatnam", cape: 2400, storm_probability: 75 },
  { station: "Chennai", cape: 1500, storm_probability: 42 },
  { station: "Kolkata", cape: 2900, storm_probability: 88 },
  { station: "Hyderabad", cape: 800, storm_probability: 20 },
  { station: "Machilipatnam", cape: 2200, storm_probability: 68 }
];

const fallbackTrendData = [
  { station: "Visakhapatnam", trend: "INTENSIFYING", cape_change: "+450 J/kg", instability_shift: "RAPID DECREASE IN LI" },
  { station: "Chennai", trend: "WEAKENING", cape_change: "-210 J/kg", instability_shift: "STABILIZING LAPSE RATE" },
  { station: "Kolkata", trend: "INTENSIFYING", cape_change: "+620 J/kg", instability_shift: "EXPLOSIVE DESTRUCTION OF CAP" },
  { station: "Machilipatnam", trend: "STABLE", cape_change: "+15 J/kg", instability_shift: "NO SIGNIFICANT CHANGE" },
  { station: "Hyderabad", trend: "STABLE", cape_change: "-5 J/kg", instability_shift: "AMBIENT SYSTEM EQUILIBRIUM" }
];

const fallbackEscalationData = [
  { station: "Visakhapatnam", escalation: "ATMOSPHERIC INVERSION BREACHED", risk_level: "EXTREME", cape: 3200, lifted_index: -8.2, pwat: 72 },
  { station: "Kolkata", escalation: "DEEP MOISTURE CONVECTION INITIATED", risk_level: "SEVERE", cape: 3100, lifted_index: -8.8, pwat: 75 }
];

const stationLocations = {
  Visakhapatnam: [17.6868, 83.2185],
  Chennai: [13.0827, 80.2707],
  Kolkata: [22.5726, 88.3639],
  Hyderabad: [17.3850, 78.4867],
  Machilipatnam: [16.1800, 81.1300]
};

const getOperationalCycleTime = (cycle) => (cycle === "12Z" ? "05:00 PM IST" : "05:00 AM IST");

function App() {
  // Navigation Section Router
  const [activeSection, setActiveSection] = useState("RADAR");

  // Global IMD Review Mode State
  const [reviewMode, setReviewMode] = useState(() => localStorage.getItem("imd_review_mode") === "true");

  const handleToggleReviewMode = () => {
    const newMode = !reviewMode;
    setReviewMode(newMode);
    localStorage.setItem("imd_review_mode", String(newMode));
  };

  // Secure Authentication States
  const [token, setToken] = useState(localStorage.getItem("stormsense_token") || null);
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("stormsense_user")) || null);
  const [authMode, setAuthMode] = useState("LOGIN"); // LOGIN or SIGNUP

  // Operational HUD Diagnostics States
  const [apiLatency, setApiLatency] = useState(42);
  const [dbStatus, setDbStatus] = useState("ONLINE");
  const [wsStatus, setWsStatus] = useState("DISCONNECTED");
  const [wsFrequency, setWsFrequency] = useState(0);

  // Weather Observation States
  const [forecastData, setForecastData] = useState(fallbackForecastData);
  const [historyData, setHistoryData] = useState(fallbackHistoryData);
  const [trendData, setTrendData] = useState(fallbackTrendData);
  const [escalationData, setEscalationData] = useState(fallbackEscalationData);
  const [loadingWeather, setLoadingWeather] = useState(false);
  const [lastUpdated, setLastUpdated] = useState("");

  // Ingestion Sounding Cycle States
  const [activeCycle, setActiveCycle] = useState("00Z");
  const [cycleInfo, setCycleInfo] = useState({
    active_cycle: "00Z",
    last_updated: "",
    validity: "VALID // NEXT INGEST AT 12:00Z",
    data_source: "IMD Visakhapatnam Sounding Station 43150",
    operational_status: "STABLE OBSERVATION CYCLE"
  });

  // Active Case Study Replay Override State
  const [activeCaseStudy, setActiveCaseStudy] = useState(null);
  const activeCaseStudyRef = useRef(null);

  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const reconnectDelayRef = useRef(2000); // Start reconnect with 2s delay
  const wsCandidatePortsRef = useRef([8000, 8002, 8001, 8004]);
  const wsCandidateIndexRef = useRef(0);
  const fetchAbortRef = useRef(null);
  const [activeBackendPort, setActiveBackendPort] = useState(8000);

  // Sync ref with state to prevent websocket closures reading stale states
  useEffect(() => {
    activeCaseStudyRef.current = activeCaseStudy;
  }, [activeCaseStudy]);

  // ==========================================
  // FETCH ACTIVE SOUNDING CYCLE METADATA
  // ==========================================
  const fetchCycleInfo = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:${activeBackendPort}/cwc/cycle`);
      setCycleInfo(response.data);
      setActiveCycle(response.data.active_cycle);
      return response.data;
    } catch (e) {
      console.warn("App Console: Could not fetch active ingestion sounding cycle from backend.");
      return null;
    }
  };

  const formatOperationalSyncLabel = (info, sourceLabel) => {
    const cycle = info?.active_cycle || activeCycle || "00Z";
    return `${cycle} // ${getOperationalCycleTime(cycle)} // ${sourceLabel}`;
  };

  const handleToggleCycle = async (newCycle) => {
    if (!token) return;
    try {
      const config = { headers: { Authorization: `Bearer ${token}` } };
      await axios.post(`http://127.0.0.1:${activeBackendPort}/cwc/cycle`, { cycle: newCycle }, config);
      await fetchCycleInfo();
      if (!activeCaseStudy) {
        await fetchWeatherData();
      }
    } catch (e) {
      console.error("Error toggling sounding cycle:", e);
    }
  };

  // ==========================================
  // HISTORICAL CASE STUDY INTERFACE OVERRIDE
  // ==========================================
  const handleSelectCaseStudy = (caseStudy) => {
    setActiveCaseStudy(caseStudy);
    if (caseStudy) {
      // Perform a clean deep drop-in replacement of default forecast registries
      const overriddenForecast = fallbackForecastData.map(st => {
        if (st.station === "Visakhapatnam") {
          return {
            ...st,
            cape: caseStudy.data.Visakhapatnam.cape,
            lifted_index: caseStudy.data.Visakhapatnam.lifted_index,
            sweat_index: caseStudy.data.Visakhapatnam.sweat_index,
            k_index: caseStudy.data.Visakhapatnam.k_index,
            pwat: caseStudy.data.Visakhapatnam.pwat,
            forecast: caseStudy.data.Visakhapatnam.forecast,
            storm_probability: caseStudy.data.Visakhapatnam.storm_probability
          };
        }
        if (st.station === "Machilipatnam") {
          return {
            ...st,
            cape: caseStudy.data.Machilipatnam.cape,
            lifted_index: caseStudy.data.Machilipatnam.lifted_index,
            sweat_index: caseStudy.data.Machilipatnam.sweat_index,
            k_index: caseStudy.data.Machilipatnam.k_index,
            pwat: caseStudy.data.Machilipatnam.pwat,
            forecast: caseStudy.data.Machilipatnam.forecast,
            storm_probability: caseStudy.data.Machilipatnam.storm_probability
          };
        }
        return st;
      });

      const overriddenTrends = fallbackTrendData.map(t => {
        if (t.station === "Visakhapatnam") {
          return {
            ...t,
            trend: "INTENSIFYING",
            cape_change: `+${Math.round(caseStudy.data.Visakhapatnam.cape - 1800)} J/kg`,
            instability_shift: "EXPLOSIVE MOISTURE DESTRUCTION OF CAP"
          };
        }
        if (t.station === "Machilipatnam") {
          return {
            ...t,
            trend: "INTENSIFYING",
            cape_change: `+${Math.round(caseStudy.data.Machilipatnam.cape - 1400)} J/kg`,
            instability_shift: "RAPID DECREASE IN LI / BOUNDARY HEATING"
          };
        }
        return t;
      });

      const overriddenEscalations = [
        {
          station: "Visakhapatnam",
          escalation: caseStudy.data.Visakhapatnam.forecast,
          risk_level: caseStudy.data.Visakhapatnam.storm_probability >= 85 ? "EXTREME" : "SEVERE",
          cape: caseStudy.data.Visakhapatnam.cape,
          lifted_index: caseStudy.data.Visakhapatnam.lifted_index,
          pwat: caseStudy.data.Visakhapatnam.pwat
        }
      ];

      setForecastData(overriddenForecast);
      setTrendData(overriddenTrends);
      setEscalationData(overriddenEscalations);
      setLastUpdated(`Replay: ${caseStudy.name} (Locked)`);
    } else {
      // Resume live ingestion sounding
      fetchWeatherData();
    }
  };

  // ==========================================
  // FETCH WEATHER TELEMETRY (RESILIENT API LOGIC)
  // ==========================================
  const fetchWeatherData = async () => {
    if (activeCaseStudyRef.current) return; // Prevent overwriting case study details
    
    const startTime = Date.now();
    try {
      setLoadingWeather(true);

      if (fetchAbortRef.current) {
        fetchAbortRef.current.abort();
      }
      fetchAbortRef.current = new AbortController();
      const requestCfg = { signal: fetchAbortRef.current.signal };
      
      const forecastResponse = await axios.get(`http://127.0.0.1:${activeBackendPort}/forecast`, requestCfg);
      const historyResponse = await axios.get(`http://127.0.0.1:${activeBackendPort}/history`, requestCfg);
      const trendResponse = await axios.get(`http://127.0.0.1:${activeBackendPort}/trend-analysis`, requestCfg);
      const escalationResponse = await axios.get(`http://127.0.0.1:${activeBackendPort}/storm-escalation`, requestCfg);

      const safeForecast = validateForecastPayload(forecastResponse.data);
      const safeHistory = Array.isArray(historyResponse.data) ? historyResponse.data : [];
      const safeTrend = Array.isArray(trendResponse.data) ? trendResponse.data : [];
      const safeEscalation = Array.isArray(escalationResponse.data) ? escalationResponse.data : [];

      setForecastData(safeForecast.length > 0 ? safeForecast : fallbackForecastData);
      setHistoryData(safeHistory.length > 0 ? safeHistory : fallbackHistoryData);
      setTrendData(safeTrend.length > 0 ? safeTrend : fallbackTrendData);
      setEscalationData(safeEscalation.length > 0 ? safeEscalation : fallbackEscalationData);
      
      const latestCycleInfo = await fetchCycleInfo();
      setLastUpdated(formatOperationalSyncLabel(latestCycleInfo, "API SYNC"));
      setDbStatus("ONLINE");
      setApiLatency(Date.now() - startTime);
    } catch (error) {
      if (axios.isCancel?.(error) || error?.name === "CanceledError" || error?.name === "AbortError") {
        return;
      }
      console.warn("App Console: API backend is offline, utilizing local meteorological mock telemetry registry.");
      setLastUpdated(formatOperationalSyncLabel(cycleInfo, "CACHE / MOCK TELEMETRY"));
      setDbStatus("OFFLINE");
      setApiLatency(0);
    } finally {
      setLoadingWeather(false);
    }
  };

  // ==========================================
  // WEBSOCKET TELEMETRY STREAM & EXPONENTIAL BACKOFF RECOVERY
  // ==========================================
  const connectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }

    console.log("WebSocket: Attempting atmospheric feed handshake...");
    const candidatePorts = wsCandidatePortsRef.current || [8000];
    const port = candidatePorts[wsCandidateIndexRef.current] ?? 8000;
    const socket = new WebSocket(`ws://127.0.0.1:${port}/stream/atmospheric`);
    wsRef.current = socket;

    let messageCount = 0;
    let hasOpened = false;
    let frequencyTimer = setInterval(() => {
      setWsFrequency(messageCount);
      messageCount = 0;
    }, 1000);

    socket.onopen = () => {
      console.log("WebSocket: Handshake accepted. Live streaming active.");
      hasOpened = true;
      setWsStatus("LIVE");
      setActiveBackendPort(port);
      reconnectDelayRef.current = 2000; // Reset reconnection delay
    };

    socket.onmessage = (event) => {
      messageCount++;
      if (activeCaseStudyRef.current) return; // Prevent overwriting case study details
      
      try {
        const payload = JSON.parse(event.data);
        if (payload?.forecasts && Array.isArray(payload.forecasts) && payload.forecasts.length > 0) {
          setForecastData(validateForecastPayload(payload.forecasts));
        }
        if (payload?.trends && Array.isArray(payload.trends) && payload.trends.length > 0) {
          setTrendData(payload.trends);
        }
        if (payload?.escalations && Array.isArray(payload.escalations)) {
          setEscalationData(payload.escalations);
        }
        if (payload?.cycle_info) {
          setCycleInfo(payload.cycle_info);
          if (payload.cycle_info.active_cycle) {
            setActiveCycle(payload.cycle_info.active_cycle);
          }
        }
        setLastUpdated(formatOperationalSyncLabel(payload?.cycle_info, "WEBSOCKET LIVE"));
      } catch (e) {
        console.error("WebSocket payload parsing exception:", e);
      }
    };

    socket.onclose = (event) => {
      console.warn("WebSocket: Atmospheric feed disconnected. Clean close:", event.wasClean);
      setWsStatus("OFFLINE FALLBACK");
      clearInterval(frequencyTimer);
      // If the socket never opened, try alternate backend ports before exponential backoff.
      const ports = wsCandidatePortsRef.current || [8000];
      if (!hasOpened && wsCandidateIndexRef.current < ports.length - 1) {
        wsCandidateIndexRef.current += 1;
        reconnectDelayRef.current = 2000;
        triggerReconnect();
        return;
      }
      // After a successful open (or after exhausting candidates), stick to the best known port.
      if (hasOpened) wsCandidateIndexRef.current = Math.min(wsCandidateIndexRef.current, ports.length - 1);
      triggerReconnect();
    };

    socket.onerror = (err) => {
      console.error("WebSocket socket error encountered:", err);
      socket.close();
    };
  };

  const triggerReconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    setWsStatus("RECONNECTING");
    console.log(`WebSocket: Retry schedule queued in ${reconnectDelayRef.current}ms`);
    reconnectTimeoutRef.current = setTimeout(() => {
      connectWebSocket();
      // Double the delay for next retry up to a max of 30 seconds
      reconnectDelayRef.current = Math.min(30000, reconnectDelayRef.current * 2);
    }, reconnectDelayRef.current);
  };

  // Start polling and websocket streaming hooks
  useEffect(() => {
    if (token) {
      fetchWeatherData();
      connectWebSocket();
      fetchCycleInfo();

      // Secondary fallback polling loop (5 mins) if WS fails
      const weatherInterval = setInterval(fetchWeatherData, 300000);

      return () => {
        clearInterval(weatherInterval);
        if (fetchAbortRef.current) fetchAbortRef.current.abort();
        if (wsRef.current) wsRef.current.close();
        if (reconnectTimeoutRef.current) clearTimeout(reconnectTimeoutRef.current);
      };
    }
  }, [token]);

  // Weather calculations matching standardized 5-Tier convective risk warning system
  const getRiskColor = (forecast) => {
    const fUpper = forecast ? forecast.toUpperCase() : "";
    if (fUpper.includes("EXTREME")) return "#a855f7";  // Extreme (Purple)
    if (fUpper.includes("SEVERE")) return "#ef4444";   // Severe (Red)
    if (fUpper.includes("HIGH")) return "#f97316";     // High (Orange)
    if (fUpper.includes("MODERATE")) return "#eab308"; // Moderate (Yellow)
    return "#10b981";                                  // Low (Green)
  };

  const getAIScoreColor = (score) => {
    if (score >= 85) return "#a855f7"; // Extreme (Purple)
    if (score >= 70) return "#ef4444"; // Severe (Red)
    if (score >= 50) return "#f97316"; // High (Orange)
    if (score >= 30) return "#eab308"; // Moderate (Yellow)
    return "#10b981";                  // Low (Green)
  };

  // Compute number of severe warnings active (threshold is 60% probability or severe forecast status)
  const criticalCount = forecastData.filter(s => s.storm_probability >= 60 || s.forecast?.includes("SEVERE") || s.forecast?.includes("HIGH")).length;

  const handleLoginSuccess = (token, user) => {
    localStorage.setItem("stormsense_token", token);
    localStorage.setItem("stormsense_user", JSON.stringify(user));
    setToken(token);
    setUser(user);
  };

  const handleLogout = () => {
    localStorage.removeItem("stormsense_token");
    localStorage.removeItem("stormsense_user");
    setToken(null);
    setUser(null);
    setActiveCaseStudy(null);
  };

  // ==========================================
  // SECURE AUTHENTICATION SCREEN ROUTING
  // ==========================================
  if (!token) {
    if (authMode === "SIGNUP") {
      return (
        <Signup
          onToggleMode={() => setAuthMode("LOGIN")}
          backendStatus={dbStatus}
        />
      );
    }
    return (
      <Login
        onLoginSuccess={handleLoginSuccess}
        onToggleMode={() => setAuthMode("SIGNUP")}
        backendStatus={dbStatus}
      />
    );
  }

  return (
    <div style={{ backgroundColor: "#0f172a", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      
      {/* Sticky Blurred Header with HUD */}
      <Header
        apiLatency={apiLatency}
        dbStatus={dbStatus}
        wsStatus={wsStatus}
        wsFrequency={wsFrequency}
        criticalCount={criticalCount}
        user={user}
        onLogout={handleLogout}
        reviewMode={reviewMode}
        onToggleReviewMode={handleToggleReviewMode}
      />

      {/* Main Console Workspace: Sidebar navigation + Active module layout */}
      <div style={{ flex: 1, display: "flex" }}>
        
        {/* Navigation Sidebar */}
        <Sidebar
          activeSection={activeSection}
          setActiveSection={setActiveSection}
        />

        {/* Console Panel Component Viewport */}
        <main style={{ flex: 1, width: "100%", maxWidth: "none", padding: "24px", position: "relative", minWidth: 0 }}>
          
          {/* Case Study Status Alert Banner */}
          {activeCaseStudy && (
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              backgroundColor: "rgba(168, 85, 247, 0.15)",
              border: "1px solid rgba(168, 85, 247, 0.4)",
              borderRadius: "8px",
              padding: "8px 16px",
              marginBottom: "16px",
              fontSize: "12px",
              color: "#a855f7",
              fontFamily: "JetBrains Mono"
            }}>
              <span>🚨 <strong>OPERATIONAL REPLAY RUNNING:</strong> {activeCaseStudy.name} event loaded. Soundings & radar profiles represent historical storm state.</span>
              <button 
                onClick={() => handleSelectCaseStudy(null)}
                style={{
                  backgroundColor: "#a855f7",
                  border: "none",
                  borderRadius: "4px",
                  color: "#ffffff",
                  padding: "4px 10px",
                  cursor: "pointer",
                  fontSize: "11px",
                  fontWeight: "bold"
                }}
              >
                Resume Live Ingestion
              </button>
            </div>
          )}

          {reviewMode && activeSection !== "RESEARCH" && activeSection !== "HEALTH" ? (
            <ErrorBoundary>
              <IMDReviewSummaryDeck />
            </ErrorBoundary>
          ) : (
            <>
              {activeSection === "RADAR" && (
                <ErrorBoundary>
                  <RadarConsole
                    forecastData={forecastData}
                    stationLocations={stationLocations}
                    getRiskColor={getRiskColor}
                    getAIScoreColor={getAIScoreColor}
                    loadingWeather={loadingWeather}
                    lastUpdated={lastUpdated}
                    activeCaseStudy={activeCaseStudy}
                    reviewMode={reviewMode}
                  />
                </ErrorBoundary>
              )}

              {activeSection === "PREDICTOR" && (
                <ErrorBoundary>
                  <PredictorEngine
                    forecastData={forecastData}
                    trendData={trendData}
                    escalationData={escalationData}
                    getRiskColor={getRiskColor}
                    getAIScoreColor={getAIScoreColor}
                    token={token}
                    user={user}
                    activeCycle={activeCycle}
                    cycleInfo={cycleInfo}
                    onToggleCycle={handleToggleCycle}
                    reviewMode={reviewMode}
                  />
                </ErrorBoundary>
              )}

              {activeSection === "ANALYTICS" && (
                <ErrorBoundary>
                  <AnalyticsDeck
                    forecastData={forecastData}
                    trendData={trendData}
                    historyData={historyData}
                    activeCaseStudy={activeCaseStudy}
                    onSelectCaseStudy={handleSelectCaseStudy}
                    activeCycle={activeCycle}
                    reviewMode={reviewMode}
                  />
                </ErrorBoundary>
              )}

              {activeSection === "RESEARCH" && (
                <ErrorBoundary>
                  <ResearchHub activeCycle={activeCycle} activeCaseStudy={activeCaseStudy} forecastData={forecastData} reviewMode={reviewMode} />
                </ErrorBoundary>
              )}

              {activeSection === "HEALTH" && (
                <ErrorBoundary>
                  <HealthConsole />
                </ErrorBoundary>
              )}

              {[
                "ATM_INTEL",
                "WATCHDESK",
                "THERMO_LAB",
                "CLIMO_RESEARCH",
                "AI_LAB",
                "RADSAT_FUSION",
                "VERIFY_CENTER",
                "ANALOG_ARCHIVE",
                "BULLETIN",
                "ANDHRA_MONITOR",
              ].includes(activeSection) && (
                <ErrorBoundary>
                  <Phase3OpsModule
                    moduleId={activeSection}
                    forecastData={forecastData}
                    trendData={trendData}
                    reviewMode={reviewMode}
                  />
                </ErrorBoundary>
              )}
            </>
          )}

        </main>
      </div>

    </div>
  );
}

export default App;
