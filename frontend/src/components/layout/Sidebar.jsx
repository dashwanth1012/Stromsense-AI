import React from "react";
import {
  BrainCircuit,
  ShieldAlert,
  FlaskConical,
  BookOpenCheck,
  Bot,
  SatelliteDish,
  BadgeCheck,
  Archive,
  FileText,
  Waves
} from "lucide-react";

export default function Sidebar({ activeSection, setActiveSection }) {
  const menuItems = [
    {
      id: "RADAR",
      label: "Live Doppler Radar",
      icon: (
        <svg style={{ width: "20px", height: "20px" }} fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      id: "PREDICTOR",
      label: "AI Prediction Engine",
      icon: (
        <svg style={{ width: "20px", height: "20px" }} fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 21l8.904-4.452M18 10.5a6 6 0 11-12 0 6 6 0 0112 0z" />
        </svg>
      )
    },
    {
      id: "ANALYTICS",
      label: "Convective Analytics",
      icon: (
        <svg style={{ width: "20px", height: "20px" }} fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v16.5M12 9.75h9.75M12 14.25h9.75M12 5.25h9.75M3.75 21h16.5" />
        </svg>
      )
    },
    {
      id: "RESEARCH",
      label: "Research & Insights",
      icon: (
        <svg style={{ width: "20px", height: "20px" }} fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
        </svg>
      )
    },
    {
      id: "HEALTH",
      label: "Health & Migrations",
      icon: (
        <svg style={{ width: "20px", height: "20px" }} fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.152c-3.196 0-6.1-1.249-8.25-3.286zm0 13.036h.008v.008H12v-.008z" />
        </svg>
      )
    },
    { id: "ATM_INTEL", label: "Atmospheric Intelligence Center", icon: <BrainCircuit size={18} strokeWidth={2} /> },
    { id: "WATCHDESK", label: "Severe Weather Watchdesk", icon: <ShieldAlert size={18} strokeWidth={2} /> },
    { id: "THERMO_LAB", label: "Thermodynamic Lab", icon: <FlaskConical size={18} strokeWidth={2} /> },
    { id: "CLIMO_RESEARCH", label: "Climatology & Research Center", icon: <BookOpenCheck size={18} strokeWidth={2} /> },
    { id: "AI_LAB", label: "Thunderstorm Forecast Simulator", icon: <Bot size={18} strokeWidth={2} /> },
    { id: "RADSAT_FUSION", label: "Live Operational Nowcast Center", icon: <SatelliteDish size={18} strokeWidth={2} /> },
    { id: "VERIFY_CENTER", label: "Forecast Verification", icon: <BadgeCheck size={18} strokeWidth={2} /> },
    { id: "ANALOG_ARCHIVE", label: "Historical Thunderstorm Archive", icon: <Archive size={18} strokeWidth={2} /> },
    { id: "BULLETIN", label: "Auto IMD Bulletin Generator", icon: <FileText size={18} strokeWidth={2} /> },
    { id: "ANDHRA_MONITOR", label: "Coastal Thunderstorm Monitoring Center", icon: <Waves size={18} strokeWidth={2} /> },
  ];

  return (
    <div style={{
      width: "280px",
      minWidth: "280px",
      backgroundColor: "#0b0f19",
      borderRight: "1px solid #1e293b",
      display: "flex",
      flexDirection: "column",
      padding: "18px 14px",
      height: "calc(100vh - 80px)",
      gap: "6px",
      overflowY: "auto",
      overflowX: "hidden"
    }}>
      <span className="font-technical" style={{
        fontSize: "11px",
        color: "#64748b",
        fontWeight: "bold",
        letterSpacing: "2px",
        paddingLeft: "12px",
        marginBottom: "12px",
        textTransform: "uppercase"
      }}>
        Command Deck Consoles
      </span>

      {menuItems.map((item) => {
        const isActive = activeSection === item.id;
        return (
          <button
            key={item.id}
            onClick={() => setActiveSection(item.id)}
            className="interactive-action"
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              width: "100%",
              padding: "11px 14px",
              borderRadius: "10px",
              border: isActive ? "1px solid rgba(244, 63, 94, 0.4)" : "1px solid transparent",
              backgroundColor: isActive ? "rgba(244, 63, 94, 0.08)" : "transparent",
              color: isActive ? "#ffffff" : "#94a3b8",
              fontWeight: isActive ? 700 : 600,
              fontSize: "13px",
              lineHeight: "1.25",
              cursor: "pointer",
              textAlign: "left",
              outline: "none",
              boxShadow: isActive ? "0 0 15px rgba(244, 63, 94, 0.1)" : "none",
              transition: "all 0.2s ease-in-out"
            }}
            onMouseEnter={(e) => {
              if (!isActive) {
                e.currentTarget.style.color = "#ffffff";
                e.currentTarget.style.backgroundColor = "rgba(30, 41, 59, 0.3)";
              }
            }}
            onMouseLeave={(e) => {
              if (!isActive) {
                e.currentTarget.style.color = "#94a3b8";
                e.currentTarget.style.backgroundColor = "transparent";
              }
            }}
          >
            <span style={{
              color: isActive ? "#f43f5e" : "#64748b",
              display: "flex",
              alignItems: "center",
              minWidth: "20px",
              justifyContent: "center"
            }}>
              {item.icon}
            </span>
            <span style={{ minWidth: 0 }}>{item.label}</span>
          </button>
        );
      })}

      {/* Footer system core info panel */}
      <div style={{
        marginTop: "auto",
        padding: "16px",
        backgroundColor: "#020617",
        borderRadius: "12px",
        border: "1px solid #1e293b",
        display: "flex",
        flexDirection: "column",
        gap: "4px"
      }}>
        <span className="font-technical" style={{ fontSize: "10px", color: "#64748b", fontWeight: "bold" }}>CONSOLE_STATUS</span>
        <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
          <span style={{
            width: "6px",
            height: "6px",
            borderRadius: "50%",
            backgroundColor: "#10b981",
            boxShadow: "0 0 6px #10b981"
          }}></span>
          <span className="font-technical" style={{ fontSize: "11px", color: "#10b981", fontWeight: "bold" }}>SYSTEM_HEALTH_OK</span>
        </div>
      </div>
    </div>
  );
}
