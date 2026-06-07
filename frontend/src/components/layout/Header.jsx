import { useEffect, useState } from "react";

const formatIstClock = () =>
  `${new Intl.DateTimeFormat("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true,
    timeZone: "Asia/Kolkata"
  }).format(new Date())} IST`;

export default function Header({
  apiLatency = 42,
  dbStatus = "ONLINE",
  wsStatus = "CONNECTED",
  criticalCount = 0,
  wsFrequency = 12,
  user = null,
  onLogout = null,
  reviewMode = false,
  onToggleReviewMode = null
}) {
  const [timeStr, setTimeStr] = useState(formatIstClock());
  const isWsLive = wsStatus === "CONNECTED" || wsStatus === "LIVE";

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeStr(formatIstClock());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header style={{
      position: "sticky",
      top: 0,
      height: "80px",
      zIndex: 100,
      backgroundColor: "rgba(15, 23, 42, 0.9)",
      backdropFilter: "blur(12px)",
      borderBottom: "1px solid #1e293b",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 30px"
    }}>
      {/* Left Area: Title & Brand */}
      <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
        <div style={{
          background: "linear-gradient(135deg, #f43f5e, #be123c)",
          padding: "8px 14px",
          borderRadius: "8px",
          color: "white",
          fontWeight: 800,
          fontSize: "18px",
          letterSpacing: "2px",
          boxShadow: "0 0 15px rgba(244, 63, 94, 0.4)",
          display: "flex",
          alignItems: "center",
          gap: "8px"
        }}>
          ⚡ STORMSENSE AI
        </div>
        <div style={{ height: "24px", width: "1px", backgroundColor: "#334155" }}></div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span style={{ fontSize: "10px", fontWeight: "bold", letterSpacing: "0.15em", color: "#64748b" }}>
            ATMOSPHERIC COMMAND & CONTROL
          </span>
          <span className="font-technical" style={{ fontSize: "11px", color: "#3b82f6", fontWeight: "bold" }}>
            v5.0.0-OPERATIONAL
          </span>
        </div>
      </div>

      {/* Center Area: Floating Diagnostics HUD */}
      <div className="glass-panel" style={{
        display: "flex",
        alignItems: "center",
        gap: "24px",
        padding: "8px 24px",
        borderRadius: "16px",
        border: "1px solid #1e293b",
        backgroundColor: "rgba(9, 13, 22, 0.6)"
      }}>
        {/* API Latency */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>PING:</span>
          <span className="font-technical" style={{ fontSize: "12px", color: "#3b82f6", fontWeight: "bold" }}>
            {apiLatency}ms
          </span>
        </div>
        <div style={{ width: "1px", height: "14px", backgroundColor: "#1e293b" }}></div>

        {/* Database Status */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>DB:</span>
          <span style={{ display: "inline-flex", alignItems: "center", gap: "4px" }}>
            <span style={{
              width: "6px",
              height: "6px",
              borderRadius: "50%",
              backgroundColor: dbStatus === "ONLINE" ? "#10b981" : "#f43f5e",
              boxShadow: dbStatus === "ONLINE" ? "0 0 6px #10b981" : "0 0 6px #f43f5e"
            }}></span>
            <span className="font-technical" style={{ fontSize: "11px", color: dbStatus === "ONLINE" ? "#10b981" : "#f43f5e", fontWeight: "bold" }}>
              {dbStatus}
            </span>
          </span>
        </div>
        <div style={{ width: "1px", height: "14px", backgroundColor: "#1e293b" }}></div>

        {/* WebSocket Stream Ingest */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>INGEST:</span>
          <span className="font-technical" style={{ fontSize: "11px", color: "#e2e8f0", fontWeight: "bold" }}>
            {isWsLive ? `WS / ${wsFrequency} Hz` : wsStatus === "RECONNECTING" ? "WS RECONNECTING" : "POLLING / 5m"}
          </span>
          <span style={{
            width: "6px",
            height: "6px",
            borderRadius: "50%",
            backgroundColor: isWsLive ? "#3b82f6" : "#f59e0b",
            boxShadow: isWsLive ? "0 0 6px #3b82f6" : "0 0 6px #f59e0b",
            animation: "status-pulse 1.5s infinite"
          }}></span>
        </div>
        <div style={{ width: "1px", height: "14px", backgroundColor: "#1e293b" }}></div>

        {/* Convective Hazards */}
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>SECTOR ALERTS:</span>
          <span className="font-technical" style={{
            fontSize: "12px",
            color: criticalCount > 0 ? "#f43f5e" : "#10b981",
            fontWeight: "bold",
            backgroundColor: criticalCount > 0 ? "rgba(244, 63, 94, 0.15)" : "rgba(16, 185, 129, 0.15)",
            padding: "2px 8px",
            borderRadius: "6px",
            border: `1px solid ${criticalCount > 0 ? "rgba(244, 63, 94, 0.3)" : "rgba(16, 185, 129, 0.3)"}`
          }}>
            {criticalCount} ACTIVE
          </span>
        </div>
      </div>

      {/* Right Area: Time HUD & Operator Profile */}
      <div style={{ display: "flex", alignItems: "center", gap: "20px" }}>
        
        {/* IMD Review Mode Toggle */}
        <button
          onClick={() => onToggleReviewMode?.()}
          style={{
            background: reviewMode ? "rgba(168, 85, 247, 0.15)" : "rgba(30, 41, 59, 0.5)",
            border: `1px solid ${reviewMode ? "#a855f7" : "#334155"}`,
            color: reviewMode ? "#c084fc" : "#94a3b8",
            fontSize: "10px",
            fontWeight: "bold",
            padding: "6px 12px",
            borderRadius: "6px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            boxShadow: reviewMode ? "0 0 10px rgba(168, 85, 247, 0.2)" : "none",
            transition: "all 0.2s"
          }}
        >
          <span>📋</span>
          <span>IMD REVIEW MODE: {reviewMode ? "ON" : "OFF"}</span>
        </button>

        {/* Clock */}
        <div className="font-technical" style={{
          fontSize: "14px",
          color: "#94a3b8",
          letterSpacing: "1px",
          backgroundColor: "#020617",
          padding: "6px 14px",
          borderRadius: "8px",
          border: "1px solid #1e293b"
        }}>
          ⏱️ {timeStr}
        </div>

        <div style={{ height: "24px", width: "1px", backgroundColor: "#334155" }}></div>

        {/* Operator Profile */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end" }}>
            <span style={{ fontSize: "13px", fontWeight: "bold", color: "#f1f5f9" }}>{user ? user.name : "SYS_OP // NEON"}</span>
            <span className="font-technical" style={{ fontSize: "10px", color: "#10b981", fontWeight: "bold" }}>{user ? user.role : "MET_CHIEF"}</span>
          </div>
          {onLogout && (
            <button
              onClick={onLogout}
              style={{
                background: "rgba(244, 63, 94, 0.08)",
                border: "1px solid rgba(244, 63, 94, 0.3)",
                color: "#f43f5e",
                fontSize: "10px",
                padding: "4px 8px",
                borderRadius: "6px",
                cursor: "pointer",
                fontWeight: "bold",
                marginLeft: "4px",
                transition: "all 0.2s"
              }}
            >
              LOGOUT
            </button>
          )}
          <div style={{
            width: "36px",
            height: "36px",
            borderRadius: "10px",
            border: "1px solid #334155",
            background: "linear-gradient(135deg, #1e293b, #0f172a)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: "bold",
            fontSize: "12px",
            color: "#f43f5e",
            boxShadow: "0 0 10px rgba(244, 63, 94, 0.15)"
          }}>
            {user ? user.name.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2) : "MC"}
          </div>
        </div>
      </div>
    </header>
  );
}
