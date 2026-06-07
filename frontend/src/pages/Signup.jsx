import { useState } from "react";
import { apiPost } from "../services/apiClient";

export default function Signup({ onToggleMode, backendStatus }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("MET_CHIEF");
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    if (!name || !email || !password) {
      setError("Please fill in all operational credential fields.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      // Connect to FastAPI auth signup endpoint
      const response = await apiPost("/auth/signup", {
        name,
        email,
        password,
        role
      });

      setSuccess(response.message || "Operator account registered successfully!");
      setName("");
      setEmail("");
      setPassword("");
      
      // Auto toggle to Login after 2 seconds
      setTimeout(() => {
        onToggleMode();
      }, 2000);

    } catch (err) {
      console.error("Signup Exception:", err);
      const errMsg = err.response?.data?.detail || err.operationalMessage || "Connection refused: Meteorological server is offline.";
      setError(errMsg);
    } finally {
      setLoading(false);
    }
  };

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
        background: "radial-gradient(circle, rgba(16, 185, 129, 0.03) 0%, transparent 70%)",
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
            backgroundColor: "rgba(16, 185, 129, 0.1)",
            border: "1px solid rgba(16, 185, 129, 0.2)",
            fontSize: "24px",
            marginBottom: "12px",
            boxShadow: "0 0 15px rgba(16, 185, 129, 0.2)"
          }}>
            🛰️
          </div>
          <h1 style={{ fontSize: "20px", fontWeight: "900", color: "#ffffff", letterSpacing: "1px" }}>
            StormSense AI
          </h1>
          <p className="font-technical" style={{ fontSize: "10px", color: "#10b981", textTransform: "uppercase", marginTop: "4px", letterSpacing: "2px" }}>
            Operator Registration Portal
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

        {success && (
          <div style={{
            backgroundColor: "rgba(16, 185, 129, 0.1)",
            border: "1px solid rgba(16, 185, 129, 0.3)",
            borderRadius: "8px",
            padding: "10px 14px",
            fontSize: "12px",
            color: "#10b981",
            marginBottom: "20px",
            textAlign: "center",
            fontWeight: "bold"
          }}>
            {success} Redirecting to login terminal...
          </div>
        )}

        <form onSubmit={handleSignupSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label className="font-technical" style={{ fontSize: "10px", color: "#94a3b8", fontWeight: "bold", textTransform: "uppercase" }}>
              Full Name / Operator Signature
            </label>
            <input
              type="text"
              placeholder="e.g. Dr. A. K. Sharma"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={loading || success}
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
              Operational Username / Email
            </label>
            <input
              type="email"
              placeholder="operator@stormsense.gov.in"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading || success}
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
              disabled={loading || success}
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
              Operational Command Role
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              disabled={loading || success}
              style={{
                backgroundColor: "#020617",
                border: "1px solid #1e293b",
                borderRadius: "8px",
                padding: "10px 14px",
                color: "#10b981",
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
            disabled={loading || success}
            className="interactive-action"
            style={{
              backgroundColor: "#10b981",
              boxShadow: "0 0 15px rgba(16, 185, 129, 0.4)",
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
            {loading ? "INITIALIZING SECURE REGISTRY..." : "✦ REGISTER OPERATOR ID"}
          </button>
        </form>

        <div style={{ height: "1px", backgroundColor: "#1e293b", margin: "24px 0" }}></div>

        <div style={{ textAlign: "center", fontSize: "11px", color: "#64748b" }}>
          Already registered?{" "}
          <span
            onClick={onToggleMode}
            style={{ color: "#10b981", cursor: "pointer", textDecoration: "underline" }}
          >
            Authorize Operator ID
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
