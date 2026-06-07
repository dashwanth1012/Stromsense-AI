import { useState, useEffect } from "react";
import { apiPost } from "../services/apiClient";

export default function Login({ onLoginSuccess, onToggleMode, backendStatus }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("MET_CHIEF");
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [booting, setBooting] = useState(false);
  const [bootProgress, setBootProgress] = useState(0);
  const [bootLog, setBootLog] = useState([]);

  // Telemetry loading logs
  const bootMessages = [
    { text: "Initializing Atmospheric Intelligence Command Grid...", time: 300 },
    { text: "Establishing secure JWS session protocol...", time: 800 },
    { text: "Connecting to CWC Visakhapatnam telemetry socket...", time: 1400 },
    { text: "Syncing Station ID 43150 / 43185 sounding feeds...", time: 2000 },
    { text: "Caching Bay of Bengal convective thermodynamic grids...", time: 2600 },
    { text: "Deploying machine-learning thunderstorm probability models...", time: 3200 },
    { text: "Status NOMINAL: Operational Command Console Ready.", time: 3800 }
  ];

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Provide operational email and password authorization.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // Connect to FastAPI auth login endpoint
      const response = await apiPost("/auth/login", {
        email,
        password
      });

      const { token, user } = response;

      // Validate matching role
      if (user.role !== role) {
        setError(`Operational Authorization Mismatch: User role is registered as ${user.role}, not ${role}.`);
        setLoading(false);
        return;
      }

      // Launch Boot Sequence
      triggerBootSequence(token, user);
    } catch (err) {
      console.error("Auth Exception:", err);
      const errMsg = err.response?.data?.detail || err.operationalMessage || "Connection refused: Meteorological server is offline.";
      setError(errMsg);
      setLoading(false);
    }
  };

  const handleGuestAccess = () => {
    setError("");
    setLoading(true);
    
    // Simulate Met Chief Profile for demo quick evaluation
    const guestUser = {
      id: 999,
      name: "CWC Evaluation Guest",
      email: "guest@stormsense.gov.in",
      role: role
    };
    const guestToken = "GUEST_SESSION_TOKEN_STORMSENSE";
    
    triggerBootSequence(guestToken, guestUser);
  };

  const triggerBootSequence = (token, user) => {
    setBooting(true);
    setBootProgress(0);
    setBootLog([]);

    // Iterate boot progress & console logs
    let currentProgress = 0;
    const progressInterval = setInterval(() => {
      currentProgress += 2.5;
      setBootProgress(Math.min(100, Math.round(currentProgress)));
      if (currentProgress >= 100) {
        clearInterval(progressInterval);
        setTimeout(() => {
          onLoginSuccess(token, user);
        }, 300);
      }
    }, 100);

    bootMessages.forEach((msg) => {
      setTimeout(() => {
        setBootLog((prev) => [...prev, `✦ [${new Date().toLocaleTimeString()}] ${msg.text}`]);
      }, msg.time);
    });
  };

  if (booting) {
    return (
      <div style={{
        minHeight: "100vh",
        backgroundColor: "#020617",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "24px",
        fontFamily: "JetBrains Mono"
      }}>
        <div className="glass-panel" style={{
          width: "100%",
          maxWidth: "640px",
          padding: "32px",
          border: "1px solid #334155",
          boxShadow: "0 0 40px rgba(59, 130, 246, 0.15)",
          display: "flex",
          flexDirection: "column",
          gap: "20px"
        }}>
          <div>
            <h3 style={{ fontSize: "12px", color: "#3b82f6", fontWeight: "bold", letterSpacing: "1.5px" }}>
              INITIALIZING_MET_CONSOLE_WATCH
            </h3>
            <h2 style={{ fontSize: "18px", color: "#ffffff", fontWeight: "bold", marginTop: "4px" }}>
              CWC Visakhapatnam Command Center
            </h2>
          </div>

          {/* Progress bar */}
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "#94a3b8" }}>
              <span>Loading telemetry libraries...</span>
              <span>{bootProgress}%</span>
            </div>
            <div style={{ height: "6px", backgroundColor: "#0f172a", borderRadius: "3px", overflow: "hidden", border: "1px solid #1e293b" }}>
              <div style={{
                width: `${bootProgress}%`,
                height: "100%",
                backgroundColor: "#3b82f6",
                boxShadow: "0 0 10px #3b82f6",
                transition: "width 0.1s linear"
              }}></div>
            </div>
          </div>

          {/* Terminal log panel */}
          <div style={{
            height: "220px",
            backgroundColor: "#020617",
            border: "1px solid #1e293b",
            borderRadius: "10px",
            padding: "16px",
            overflowY: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "6px",
            fontSize: "11px",
            color: "#10b981",
            lineHeight: "1.5",
            boxShadow: "inset 0 0 10px rgba(0,0,0,0.8)"
          }}>
            {bootLog.map((log, idx) => (
              <div key={idx} style={{
                color: log.includes("NOMINAL") ? "#3b82f6" : log.includes("Initializing") ? "#eab308" : "#10b981"
              }}>{log}</div>
            ))}
          </div>

          <span style={{ fontSize: "9px", color: "#64748b", textAlign: "center" }}>
            SECURE ACCESS ENFORCED // INGESTION SYNC ACTIVE
          </span>
        </div>
      </div>
    );
  }

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "#0f172a",
      backgroundImage: "radial-gradient(circle at 50% 20%, #1e1e38 0%, #0f172a 70%)",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      padding: "24px",
      position: "relative"
    }}>
      
      {/* Decorative Neon Ring */}
      <div style={{
        position: "absolute",
        width: "500px",
        height: "500px",
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(59, 130, 246, 0.05) 0%, transparent 70%)",
        top: "20%",
        zIndex: 0
      }}></div>

      <div className="glass-panel" style={{
        width: "100%",
        maxWidth: "450px",
        padding: "36px",
        border: "1px solid #334155",
        boxShadow: "0 20px 50px rgba(0, 0, 0, 0.5)",
        zIndex: 1
      }}>
        
        {/* Console Header logo */}
        <div style={{ textAlign: "center", marginBottom: "28px" }}>
          <div style={{
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
            width: "50px",
            height: "50px",
            borderRadius: "14px",
            backgroundColor: "rgba(59, 130, 246, 0.1)",
            border: "1px solid rgba(59, 130, 246, 0.2)",
            fontSize: "24px",
            marginBottom: "12px",
            boxShadow: "0 0 15px rgba(59, 130, 246, 0.2)"
          }}>
            🌩️
          </div>
          <h1 style={{ fontSize: "20px", fontWeight: "900", color: "#ffffff", letterSpacing: "1px" }}>
            StormSense AI
          </h1>
          <p className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", textTransform: "uppercase", marginTop: "4px", letterSpacing: "2px" }}>
            Atmospheric Operations Command Portal
          </p>
        </div>

        {error && (
          <div style={{
            backgroundColor: "rgba(244, 63, 94, 0.1)",
            border: "1px solid rgba(244, 63, 94, 0.3)",
            borderRadius: "8px",
            padding: "10px 14px",
            fontSize: "12px",
            color: "#f43f5e",
            marginBottom: "20px",
            textAlign: "center"
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleLoginSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label className="font-technical" style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "bold", textTransform: "uppercase" }}>
              Operational Username / Email
            </label>
            <input
              type="email"
              placeholder="operator@stormsense.gov.in"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              style={{
                backgroundColor: "#020617",
                border: "1px solid #1e293b",
                borderRadius: "8px",
                padding: "10px 14px",
                color: "#ffffff",
                fontSize: "13px",
                outline: "none",
                transition: "border 0.2s"
              }}
            />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label className="font-technical" style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "bold", textTransform: "uppercase" }}>
              Operational Passphrase
            </label>
            <input
              type="password"
              placeholder="••••••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              style={{
                backgroundColor: "#020617",
                border: "1px solid #1e293b",
                borderRadius: "8px",
                padding: "10px 14px",
                color: "#ffffff",
                fontSize: "13px",
                outline: "none",
                transition: "border 0.2s"
              }}
            />
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label className="font-technical" style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "bold", textTransform: "uppercase" }}>
              Active Command Role
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              disabled={loading}
              style={{
                backgroundColor: "#020617",
                border: "1px solid #1e293b",
                borderRadius: "8px",
                padding: "10px 14px",
                color: "#3b82f6",
                fontSize: "13px",
                fontWeight: "bold",
                outline: "none",
                cursor: "pointer"
              }}
            >
              <option value="MET_CHIEF">MET_CHIEF (Chief Commander)</option>
              <option value="FORECAST_ANALYST">FORECAST_ANALYST (Atmospheric analysis)</option>
              <option value="RADAR_OPERATOR">RADAR_OPERATOR (DWR surveillance)</option>
              <option value="TRAINEE_MET">TRAINEE_MET (Meteorological education)</option>
              <option value="RESEARCH_OBSERVER">RESEARCH_OBSERVER (Historical analytics)</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="interactive-action"
            style={{
              backgroundColor: "#3b82f6",
              boxShadow: "0 0 15px rgba(59, 130, 246, 0.4)",
              border: "none",
              color: "white",
              padding: "12px",
              borderRadius: "8px",
              fontWeight: "bold",
              fontSize: "13px",
              cursor: "pointer",
              marginTop: "8px"
            }}
          >
            {loading ? "AUTHENTICATING SECURE PIN..." : "✦ AUTHORIZE COMMAND SESSION"}
          </button>
        </form>

        <div style={{ height: "1px", backgroundColor: "#1e293b", margin: "24px 0" }}></div>

        {/* Guest Demo Access */}
        <button
          onClick={handleGuestAccess}
          disabled={loading}
          className="interactive-action font-technical"
          style={{
            width: "100%",
            backgroundColor: "rgba(16, 185, 129, 0.08)",
            border: "1px solid rgba(16, 185, 129, 0.25)",
            color: "#10b981",
            padding: "10px",
            borderRadius: "8px",
            fontWeight: "bold",
            fontSize: "12px",
            cursor: "pointer",
            marginBottom: "12px"
          }}
        >
          🚀 QUICK EVALUATION: GUEST DEMO ACCESS
        </button>

        <div style={{ textAlign: "center", fontSize: "11px", color: "#64748b" }}>
          New team member?{" "}
          <span
            onClick={onToggleMode}
            style={{ color: "#3b82f6", cursor: "pointer", textDecoration: "underline" }}
          >
            Register Operator ID
          </span>
        </div>

      </div>

      {/* Footer system health */}
      <div style={{
        marginTop: "20px",
        fontSize: "10px",
        color: "#64748b",
        display: "flex",
        gap: "16px",
        fontFamily: "JetBrains Mono"
      }}>
        <span>DB STATUS: <strong style={{ color: backendStatus === "ONLINE" ? "#10b981" : "#f43f5e" }}>{backendStatus}</strong></span>
        <span>SECURE NODE: <strong>WALTAIR_CWC_43150</strong></span>
      </div>

    </div>
  );
}
