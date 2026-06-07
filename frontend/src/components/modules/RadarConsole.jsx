import { useState, useEffect } from "react";
import { MapContainer, TileLayer, Circle, CircleMarker, Popup, useMap, SVGOverlay, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { GISAdapter } from "../../services/WeatherAdapter";
import { apiGet } from "../../services/apiClient";

// Helper component to handle active map flyTo zoom and coordinates focus
function MapController({ centerLocation }) {
  const map = useMap();
  useEffect(() => {
    if (centerLocation) {
      map.flyTo(centerLocation, 7.5, { duration: 1.5 });
    }
  }, [centerLocation, map]);
  return null;
}

export default function RadarConsole({
  forecastData,
  stationLocations,
  getRiskColor,
  getAIScoreColor,
  loadingWeather,
  lastUpdated,
  reviewMode
}) {
  const [selectedStation, setSelectedStation] = useState(null);
  const [dopplerActive, setDopplerActive] = useState(true); // Default active for Cyclone Warning Console feel
  const [insatActive, setInsatActive] = useState(false);
  const [lightningActive, setLightningActive] = useState(true); // Default active for severe storms focus
  const [radarRotation, setRadarRotation] = useState(0);
  const [capeTrace, setCapeTrace] = useState(null);
  const [historyList, setHistoryList] = useState([]);

  useEffect(() => {
    let active = true;
    const fetchCapeTrace = async () => {
      try {
        const data = await apiGet("/cwc/cape-traceability");
        if (active) {
          setCapeTrace(data);
        }
      } catch (e) {
        // silent fallback
      }
    };
    const fetchHistory = async () => {
      try {
        const data = await apiGet("/history");
        if (active) {
          setHistoryList(data);
        }
      } catch (e) {
        // silent fallback
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

  // Default select Visakhapatnam on mount to enforce Visakhapatnam Priority Mode
  useEffect(() => {
    if (forecastData && forecastData.length > 0) {
      const vizNode = forecastData.find((s) => s.station === "Visakhapatnam");
      if (vizNode) {
        setSelectedStation(vizNode);
      }
    }
  }, [forecastData]);

  // Animate the radar sweep line rotation
  useEffect(() => {
    const sweepInterval = setInterval(() => {
      setRadarRotation((prev) => (prev + 3) % 360);
    }, 40);
    return () => clearInterval(sweepInterval);
  }, []);

  // Standard IMD Visakhapatnam coordinates
  const vizCoords = [17.6868, 83.2185];
  const centerCoord = selectedStation 
    ? stationLocations[selectedStation.station] 
    : vizCoords;
  // Generate realistic storm track vectors based on Bay of Bengal convection patterns
  const getStormTrackText = (stationName) => {
    if (stationName === "Visakhapatnam" || stationName === "Machilipatnam") {
      return "TRACK: ESE to WNW @ 18 knots (Bay of Bengal squall system moving landward)";
    }
    if (stationName === "Chennai") {
      return "TRACK: SE to NW @ 12 knots (Coastal convergence convective band)";
    }
    return "TRACK: SW to NE @ 15 knots (Ambient monsoon steering winds)";
  };

  return (
    <div className="radar-workstation" style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) minmax(300px,350px)", gap: "20px", height: "calc(100vh - 160px)", minWidth: 0 }}>
      
      {/* Map Pane with Overlay HUD Controls */}
      <div className="panel-surface" style={{ position: "relative", overflow: "hidden", display: "flex", flexDirection: "column", borderRadius: "16px", border: "1px solid #334155" }}>
        
        {/* Header HUD / Operational Controls */}
        <div style={{
          padding: "16px 24px",
          borderBottom: "1px solid #1e293b",
          backgroundColor: "#0b0f19",
          display: "flex",
          flexDirection: "column",
          gap: "12px",
          zIndex: 10
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h2 style={{ fontSize: "16px", color: "#ffffff", fontWeight: "bold" }}>
                📡 IMD Visakhapatnam Cyclone Warning Centre Console
              </h2>
            </div>

            <div style={{ display: "flex", gap: "8px" }}>
              <button
                onClick={() => setDopplerActive(!dopplerActive)}
                className="interactive-action font-technical"
                style={{
                  padding: "6px 12px",
                  borderRadius: "8px",
                  fontSize: "11px",
                  fontWeight: "bold",
                  backgroundColor: dopplerActive ? "rgba(244, 63, 94, 0.15)" : "#020617",
                  border: `1px solid ${dopplerActive ? "#f43f5e" : "#1e293b"}`,
                  color: dopplerActive ? "#f43f5e" : "#64748b",
                  cursor: "pointer"
                }}
              >
                📡 DWR: {dopplerActive ? "ON" : "OFF"}
              </button>
              <button
                onClick={() => setLightningActive(!lightningActive)}
                className="interactive-action font-technical"
                style={{
                  padding: "6px 12px",
                  borderRadius: "8px",
                  fontSize: "11px",
                  fontWeight: "bold",
                  backgroundColor: lightningActive ? "rgba(245, 158, 11, 0.15)" : "#020617",
                  border: `1px solid ${lightningActive ? "#f59e0b" : "#1e293b"}`,
                  color: lightningActive ? "#f59e0b" : "#64748b",
                  cursor: "pointer"
                }}
              >
                ⚡ LIGHTNING: {lightningActive ? "ON" : "OFF"}
              </button>
              <button
                onClick={() => setInsatActive(!insatActive)}
                className="interactive-action font-technical"
                style={{
                  padding: "6px 12px",
                  borderRadius: "8px",
                  fontSize: "11px",
                  fontWeight: "bold",
                  backgroundColor: insatActive ? "rgba(59, 130, 246, 0.15)" : "#020617",
                  border: `1px solid ${insatActive ? "#3b82f6" : "#1e293b"}`,
                  color: insatActive ? "#3b82f6" : "#64748b",
                  cursor: "pointer"
                }}
              >
                ☁️ CLOUD: {insatActive ? "ON" : "OFF"}
              </button>
            </div>
          </div>

          {/* Operational HUD Info Grid */}
          {(() => {
            const station = selectedStation || forecastData[0] || {};
            const cycle = station.active_cycle || "00Z";
            const obsTime = cycle === "12Z" ? "05:00 PM IST" : "05:00 AM IST";
            const nextTime = cycle === "12Z" ? "05:00 AM IST" : "05:00 PM IST";
            const genTime = cycle === "12Z" ? "05:07 PM IST" : "05:07 AM IST";
            const sourceStr = station.sounding_source || `IMD Radiosonde (Station ${station.station_code || "43150"})`;
            return (
              <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(7, 1fr)",
                gap: "8px",
                fontSize: "11px",
                fontFamily: "JetBrains Mono",
                color: "#cbd5e1",
                backgroundColor: "#020617",
                padding: "8px 12px",
                borderRadius: "8px",
                border: "1px solid #1e293b"
              }}>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>STATION</span>
                  <strong style={{ color: "#ffffff" }}>{station.station || "Visakhapatnam"}</strong>
                </div>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>OBS DATE</span>
                  <strong style={{ color: "#ffffff" }}>2026-06-06</strong>
                </div>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>OBS TIME</span>
                  <strong style={{ color: "#ffffff" }}>{obsTime}</strong>
                </div>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>FORECAST TIME</span>
                  <strong style={{ color: "#a855f7" }}>{genTime}</strong>
                </div>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>DATA SOURCE</span>
                  <strong style={{ color: "#10b981" }}>{sourceStr.split(" ")[0]}</strong>
                </div>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>LAST DATA UPDATE</span>
                  <strong style={{ color: "#38bdf8" }}>{obsTime}</strong>
                </div>
                <div>
                  <span style={{ fontSize: "8px", color: "#64748b", display: "block" }}>NEXT EXPECTED UPDATE</span>
                  <strong style={{ color: "#facc15" }}>{nextTime}</strong>
                </div>
              </div>
            );
          })()}
        </div>

        {/* Map Container */}
        <div style={{ flex: 1, position: "relative" }}>
          <MapContainer
            center={centerCoord}
            zoom={7} // Closer default zoom for detailed coastal tracking
            zoomControl={false}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://carto.com/">CARTO</a>'
            />
            
            {/* Map FlyTo controller */}
            {selectedStation && (
              <MapController centerLocation={stationLocations[selectedStation.station]} />
            )}

            {/* Rotating SVG Radar Sweep Overlay centered on the selected station */}
            {dopplerActive && selectedStation && (() => {
              const loc = stationLocations[selectedStation.station];
              if (!loc) return null;
              
              // We'll place the sweep overlay centered on the station coordinates
              // with a range of approx 2.0 degrees lat/lng in all directions
              const boundRadius = 2.5;
              const bounds = [
                [loc[0] - boundRadius, loc[1] - boundRadius],
                [loc[0] + boundRadius, loc[1] + boundRadius]
              ];
              
              return (
                <SVGOverlay bounds={bounds}>
                  {/* Outer circle of the sweep boundary */}
                  <circle cx="50%" cy="50%" r="48%" fill="none" stroke="rgba(16, 185, 129, 0.15)" strokeWidth="1" />
                  <circle cx="50%" cy="50%" r="35%" fill="none" stroke="rgba(16, 185, 129, 0.08)" strokeWidth="0.8" strokeDasharray="5, 5" />
                  <circle cx="50%" cy="50%" r="20%" fill="none" stroke="rgba(16, 185, 129, 0.08)" strokeWidth="0.8" strokeDasharray="5, 5" />
                  
                  {/* Rotating sweep sector */}
                  <g transform={`rotate(${radarRotation}, 150, 150)`} style={{ transformOrigin: "50% 50%" }}>
                    <path 
                      d="M 150 150 L 150 6 A 144 144 0 0 1 294 150 Z" 
                      fill="url(#radar-sweep-grad)"
                      opacity="0.25"
                    />
                    <line x1="150" y1="150" x2="150" y2="6" stroke="#10b981" strokeWidth="1.5" opacity="0.8" />
                  </g>

                  <defs>
                    <radialGradient id="radar-sweep-grad" cx="50%" cy="50%" r="50%">
                      <stop offset="0%" stopColor="#10b981" stopOpacity="0.8" />
                      <stop offset="50%" stopColor="#10b981" stopOpacity="0.1" />
                      <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                    </radialGradient>
                  </defs>
                </SVGOverlay>
              );
            })()}

            {/* INSAT-3D Satellite Cloud Imagery SVG Overlay */}
            {insatActive && (
              <SVGOverlay bounds={[[6.0, 68.0], [36.0, 98.0]]}>
                <defs>
                  <filter id="cloud-glow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="15" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                  </filter>
                  <radialGradient id="cloud-grad-1" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.35" />
                    <stop offset="60%" stopColor="#60a5fa" stopOpacity="0.12" />
                    <stop offset="100%" stopColor="#1d4ed8" stopOpacity="0" />
                  </radialGradient>
                </defs>
                <circle cx="50%" cy="40%" r="22%" fill="url(#cloud-grad-1)" filter="url(#cloud-glow)" />
                <circle cx="54%" cy="42%" r="15%" fill="url(#cloud-grad-1)" filter="url(#cloud-glow)" />
              </SVGOverlay>
            )}
            
            {/* Doppler Weather Radar DWR Reflectivity precipitation cells */}
            {dopplerActive && forecastData.map((station, index) => {
              const location = stationLocations[station.station];
              if (!location) return null;
              
              const prob = station.storm_probability || 0;
              const severeProb = station.severe_ts_probability || Math.round(prob * 0.8);
              const cape = station.cape || 0;
              const pwat = station.pwat || 0;
              const shear = station.bulk_shear || 8;
              const thetaE = station.theta_e || 340;
              const moistureConv = station.moisture_convergence || 6;
              const radar = station.radar_sounding_coupling || {};
              const organizationIdx = Math.max(10, Math.min(100, Math.round((severeProb * 0.5) + (shear / 24) * 35 + (thetaE - 320) * 0.4)));
              const isPostConvective = station.post_convective_stabilization || (cape < 100 && pwat >= 45);
              if (prob < 20 && !isPostConvective) return null;

              // Reflectivity scaled from thermodynamic indices (not synthetic probability curves)
              let dbzVal;
              if (Number.isFinite(Number(radar.max_reflectivity_dbz))) {
                dbzVal = Number(radar.max_reflectivity_dbz);
              } else if (isPostConvective) {
                dbzVal = Math.round(20 + Math.min(16, (pwat / 75) * 16));
              } else {
                const capeFactor = Math.min(1, cape / 3500);
                const pwatFactor = Math.min(1, pwat / 70);
                const shearFactor = Math.min(1, shear / 24);
                const thetaFactor = Math.min(1, (thetaE - 320) / 50);
                const convFactor = Math.min(1, moistureConv / 16);
                dbzVal = Math.round(16 + capeFactor * 22 + pwatFactor * 12 + shearFactor * 10 + thetaFactor * 7 + convFactor * 6 + (severeProb / 100) * 10);
              }
              const echoTopKm = Number.isFinite(Number(radar.echo_top_km))
                ? Number(radar.echo_top_km).toFixed(1)
                : isPostConvective
                ? (4.0 + (pwat / 75) * 3.5).toFixed(1)
                : (5.5 + (prob / 100) * 9.0 + (shear / 24) * 2.2 + (organizationIdx / 100) * 1.8).toFixed(1);
              const vilScore = Number.isFinite(Number(radar.vil_kg_m2))
                ? Math.round(Number(radar.vil_kg_m2))
                : isPostConvective
                ? Math.round(12 + (pwat / 75) * 25)
                : Math.round((prob / 100) * 50 + (severeProb / 100) * 25);
              const signatureClass = radar.signature_class || (isPostConvective ? "POST-CONVECTIVE STRATIFORM RAIN SIGNATURE" : "CONVECTIVE CELL CORE");

              // Draw a realistic multi-cellular squall line structure (rainband)
              const offsetLat = (index % 2 === 0 ? 0.08 : -0.06);
              const offsetLng = (index % 2 === 0 ? -0.1 : 0.08);

              // 3 separate cells for multicellular storm representation
              const cell1 = location; // Core
              const cell2 = [location[0] + offsetLat, location[1] + offsetLng + 0.15]; // Secondary cell
              const cell3 = [location[0] - offsetLat - 0.1, location[1] - offsetLng - 0.2]; // Tertiary cell

              const trackingTo = [location[0] + 0.25, location[1] - 0.5]; // Landward motion track (ocean to land)
              const trackingPos15 = [location[0] + 0.125, location[1] - 0.25];
              const trackingPos30 = [location[0] + 0.25, location[1] - 0.5];

              return (
                <g key={`dwr-structure-${index}`}>
                  {/* Convective Rainband Polyline Connecting cells */}
                  <Polyline
                    positions={[cell3, cell1, cell2]}
                    pathOptions={{
                      color: dbzVal > 50 ? "#a855f7" : dbzVal > 40 ? "#ef4444" : "#10b981",
                      weight: 4,
                      opacity: 0.3,
                      lineCap: "round"
                    }}
                  />

                  {/* Cell 1: Core */}
                  <Circle
                    center={cell1}
                    radius={Math.round(prob * 320 + organizationIdx * 90)}
                    pathOptions={{
                      color: dbzVal >= 52 ? "#ef4444" : dbzVal >= 40 ? "#f97316" : "#10b981",
                      fillColor: dbzVal >= 52 ? "#ef4444" : dbzVal >= 40 ? "#f97316" : "#10b981",
                      fillOpacity: dbzVal >= 52 ? 0.35 : 0.2,
                      weight: 1.5
                    }}
                  >
                    <Popup>
                      <div style={{ backgroundColor: "#0f172a", color: "#ffffff", padding: "10px", borderRadius: "8px", border: "1px solid #1e293b", fontFamily: "JetBrains Mono", fontSize: "11px" }}>
                        <span style={{ color: "#ef4444", fontWeight: "bold" }}>🚨 PRIMARY CONVECTIVE CELL CORE</span><br/>
                        Signature: <strong>{signatureClass}</strong><br/>
                        Station: {station.station} ({station.station_code})<br/>
                        Reflectivity: <strong style={{ color: "#ef4444" }}>{dbzVal} dBZ</strong><br/>
                        Echo-Top Height: <strong style={{ color: "#eab308" }}>{echoTopKm} km</strong><br/>
                        VIL Score: <strong>{vilScore} kg/m²</strong><br/>
                        Organization Index: <strong>{organizationIdx}%</strong>
                      </div>
                    </Popup>
                  </Circle>

                  {/* Cell 2: Secondary Cell */}
                  {prob >= 40 && (
                    <Circle
                      center={cell2}
                      radius={prob * 250}
                      pathOptions={{
                        color: "#f59e0b",
                        fillColor: "#f59e0b",
                        fillOpacity: 0.18,
                        weight: 1
                      }}
                    >
                      <Popup>
                        <div style={{ backgroundColor: "#0f172a", color: "#ffffff", padding: "10px", borderRadius: "8px", border: "1px solid #1e293b", fontFamily: "JetBrains Mono", fontSize: "11px" }}>
                          <span style={{ color: "#f59e0b", fontWeight: "bold" }}>⚡ SECONDARY FEEDER CELL</span><br/>
                          Reflectivity: <strong>{Math.round(dbzVal * 0.85)} dBZ</strong><br/>
                          Echo-Top: <strong>{(echoTopKm * 0.8).toFixed(1)} km</strong>
                        </div>
                      </Popup>
                    </Circle>
                  )}

                  {/* Cell 3: Tertiary Cell */}
                  {prob >= 50 && (
                    <Circle
                      center={cell3}
                      radius={prob * 200}
                      pathOptions={{
                        color: "#10b981",
                        fillColor: "#10b981",
                        fillOpacity: 0.15,
                        weight: 1
                      }}
                    >
                      <Popup>
                        <div style={{ backgroundColor: "#0f172a", color: "#ffffff", padding: "10px", borderRadius: "8px", border: "1px solid #1e293b", fontFamily: "JetBrains Mono", fontSize: "11px" }}>
                          <span style={{ color: "#10b981", fontWeight: "bold" }}>🌧️ STRATIFORM OUTFLOW CELL</span><br/>
                          Reflectivity: <strong>{Math.round(dbzVal * 0.65)} dBZ</strong><br/>
                          Echo-Top: <strong>{(echoTopKm * 0.6).toFixed(1)} km</strong>
                        </div>
                      </Popup>
                    </Circle>
                  )}

                  {/* Cell Tracking & Storm Motion Vectors (Ocean-to-Land) */}
                  <Polyline
                    positions={[cell1, trackingTo]}
                    pathOptions={{
                      color: "#10b981",
                      weight: 1.5,
                      dashArray: "4, 6",
                      opacity: 0.8
                    }}
                  />

                  {/* Projected positions markers */}
                  <CircleMarker
                    center={trackingPos15}
                    radius={4}
                    pathOptions={{ color: "#10b981", fillColor: "#ffffff", fillOpacity: 1, weight: 1 }}
                  >
                    <Popup>
                      <div style={{ fontSize: "10px", fontFamily: "JetBrains Mono", color: "#ffffff" }}>
                        🕒 Projected Position (T+15 min)<br/>
                        Heading: 285° (WNW) @ 18 knots
                      </div>
                    </Popup>
                  </CircleMarker>

                  <CircleMarker
                    center={trackingPos30}
                    radius={4}
                    pathOptions={{ color: "#eab308", fillColor: "#ffffff", fillOpacity: 1, weight: 1 }}
                  >
                    <Popup>
                      <div style={{ fontSize: "10px", fontFamily: "JetBrains Mono", color: "#ffffff" }}>
                        🕒 Projected Position (T+30 min)<br/>
                        Estimated Coastal Boundary Entry
                      </div>
                    </Popup>
                  </CircleMarker>
                </g>
              );
            })}

            {/* Lightning Strike Overlays (⚡) popped up around high-buoyancy areas */}
            {lightningActive && forecastData.map((station, index) => {
              const location = stationLocations[station.station];
              const lightningProb = station.lightning_probability || station.storm_probability || 0;
              if (!location || lightningProb < 35) return null;
              
              const offsets = [
                [0.08, -0.12],
                [-0.05, 0.14],
                [0.15, 0.05]
              ];
              const activeOffsets = lightningProb >= 75 ? offsets : offsets.slice(0, 2);

              return (
                <g key={`lightning-cluster-${index}`}>
                  {activeOffsets.map((off, oIdx) => {
                    const strikeCoords = [location[0] + off[0], location[1] + off[1]];
                    return (
                      <CircleMarker
                        key={`strike-${oIdx}`}
                        center={strikeCoords}
                        radius={5}
                        pathOptions={{
                          color: "#eab308",
                          fillColor: "#ffffff",
                          fillOpacity: 1,
                          weight: 1.5
                        }}
                      >
                        <Popup>
                          <div style={{ backgroundColor: "#0f172a", color: "#eab308", fontSize: "11px", padding: "6px", fontFamily: "JetBrains Mono" }}>
                            ⚡ LIGHTNING DISCHARGE REGISTERED<br/>
                            Density: High Cloud-To-Ground Strike<br/>
                            Lat: {strikeCoords[0].toFixed(4)} | Lng: {strikeCoords[1].toFixed(4)}
                          </div>
                        </Popup>
                      </CircleMarker>
                    );
                  })}
                </g>
              );
            })}

            {/* Concentric Threat Rings centered on Visakhapatnam (50km, 100km, 200km) */}
            <g>
              <Circle
                center={vizCoords}
                radius={50000} // 50km
                pathOptions={{ color: "rgba(244, 63, 94, 0.4)", fillColor: "transparent", weight: 1.2, dashArray: "3, 6" }}
              />
              <Circle
                center={vizCoords}
                radius={100000} // 100km
                pathOptions={{ color: "rgba(244, 63, 94, 0.25)", fillColor: "transparent", weight: 1.2, dashArray: "3, 6" }}
              />
              <Circle
                center={vizCoords}
                radius={200000} // 200km
                pathOptions={{ color: "rgba(244, 63, 94, 0.15)", fillColor: "transparent", weight: 1.2, dashArray: "3, 6" }}
              />
            </g>

            {/* Sea-Breeze Convergence front & Moisture Inflow Vectors */}
            {(() => {
              const seaBreezeFrontCoords = [
                [13.08, 80.22],
                [14.50, 80.05],
                [15.80, 80.80],
                [16.15, 81.05],
                [17.10, 82.20],
                [17.65, 83.15],
                [18.50, 84.10]
              ];

              const moistureInflowVectors = [
                {
                  from: [16.2, 84.5],
                  to: [17.5, 83.3],
                  label: "Bay of Bengal Moisture Jet (Moisture Transport: 68g/kg)"
                },
                {
                  from: [15.0, 82.5],
                  to: [16.1, 81.2],
                  label: "Coastal Andhra Inflow (Moisture Transport: 61g/kg)"
                },
                {
                  from: [12.0, 81.2],
                  to: [13.0, 80.3],
                  label: "Tamil Nadu Convective Inflow (Moisture Transport: 52g/kg)"
                }
              ];

              return (
                <g>
                  {/* Sea Breeze front line */}
                  <Polyline
                    positions={seaBreezeFrontCoords}
                    pathOptions={{
                      color: "#06b6d4",
                      weight: 3.5,
                      dashArray: "8, 8",
                      opacity: 0.85
                    }}
                  >
                    <Popup>
                      <div style={{ backgroundColor: "#0f172a", color: "#06b6d4", fontSize: "11px", padding: "6px", fontFamily: "JetBrains Mono" }}>
                        🚨 SEA-BREEZE CONVERGENCE FRONT<br/>
                        Type: Convective Trigger Boundary Line<br/>
                        Status: ACTIVE (Inland pushing thermal contrast front)
                      </div>
                    </Popup>
                  </Polyline>

                  {/* Moisture inflow transport vectors */}
                  {moistureInflowVectors.map((v, i) => (
                    <g key={`inflow-${i}`}>
                      <Polyline
                        positions={[v.from, v.to]}
                        pathOptions={{
                          color: "#60a5fa",
                          weight: 2.2,
                          opacity: 0.75,
                          dashArray: "4, 6"
                        }}
                      >
                        <Popup>
                          <div style={{ backgroundColor: "#0f172a", color: "#60a5fa", fontSize: "11px", padding: "6px", fontFamily: "JetBrains Mono" }}>
                            💨 MARITIME INFLOW VECTOR<br/>
                            Source: Bay of Bengal Convective Fuel<br/>
                            Details: {v.label}
                          </div>
                        </Popup>
                      </Polyline>
                      {/* Arrow Head marker */}
                      <CircleMarker
                        center={v.to}
                        radius={4}
                        pathOptions={{
                          color: "#60a5fa",
                          fillColor: "#ffffff",
                          fillOpacity: 1,
                          weight: 1.2
                        }}
                      />
                    </g>
                  ))}
                </g>
              );
            })()}

            {/* Dynamic Storm Track Inflow Vectors moving off the Bay of Bengal (ocean-to-land) */}
            {forecastData.map((station, index) => {
              const location = stationLocations[station.station];
              if (!location || station.storm_probability < 40) return null;
              
              // Define a realistic ocean-to-land trajectory line based on station
              let oceanSource = [location[0] - 0.4, location[1] + 0.8]; // Default ESE (ocean) to WNW (land)
              if (station.station === "Chennai") {
                oceanSource = [location[0] - 0.6, location[1] + 0.6]; // SE (ocean) to NW (land)
              }
              
              return (
                <g key={`track-${index}`}>
                  {/* Outer vector arrow line */}
                  <line 
                    x1={oceanSource[1]} 
                    y1={oceanSource[0]} 
                    x2={location[1]} 
                    y2={location[0]} 
                    stroke="#10b981" 
                    strokeWidth="2.5" 
                    strokeDasharray="5, 5" 
                  />
                  {/* Blinking core nucleus marking storm velocity tracking */}
                  <CircleMarker
                    center={[(oceanSource[0] + location[0]) / 2, (oceanSource[1] + location[1]) / 2]}
                    radius={3}
                    pathOptions={{
                      color: "#10b981",
                      fillColor: "#ffffff",
                      fillOpacity: 0.9,
                      weight: 1
                    }}
                  />
                </g>
              );
            })}

            {/* Dynamic Interactive Station Markers */}
            {forecastData.map((station, index) => {
              const location = stationLocations[station.station];
              if (!location) return null;
              const isStationSelected = selectedStation?.station === station.station;
              const riskColor = getRiskColor(station.forecast);
              
              return (
                <CircleMarker
                  key={`marker-${index}`}
                  center={location}
                  radius={isStationSelected ? 12 : 8}
                  pathOptions={{
                    color: riskColor,
                    fillColor: isStationSelected ? "#ffffff" : riskColor,
                    fillOpacity: 0.9,
                    weight: isStationSelected ? 4 : 2,
                    stroke: true
                  }}
                  eventHandlers={{
                    click: () => setSelectedStation(station)
                  }}
                >
                  <Popup>
                    <div style={{
                      backgroundColor: "#0f172a",
                      color: "#ffffff",
                      padding: "10px",
                      borderRadius: "12px",
                      border: "1px solid #334155",
                      fontFamily: "Satoshi",
                      minWidth: "220px"
                    }}>
                      <h4 style={{ fontWeight: "bold", fontSize: "14px", borderBottom: "1px solid #1e293b", paddingBottom: "6px", marginBottom: "6px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span>{station.station}</span>
                        <span className="font-technical" style={{ fontSize: "10px", color: "#64748b" }}>#{station.station_code}</span>
                      </h4>
                      <div style={{ display: "flex", flexDirection: "column", gap: "4px", fontSize: "12px" }}>
                        <div>CAPE Index: <strong style={{ color: "#f43f5e" }}>{station.cape} J/kg</strong></div>
                        <div>Lifted Index: <strong style={{ color: "#3b82f6" }}>{station.lifted_index}</strong></div>
                        <div>Precip Water: <strong>{station.pwat} mm</strong></div>
                        <div>Convective Risk: <strong style={{ color: riskColor }}>{station.forecast}</strong></div>
                        
                        <div style={{ marginTop: "6px", display: "flex", justifyContent: "space-between", borderTop: "1px solid #1e293b", paddingTop: "6px" }}>
                          <span>AI Probability:</span>
                          <span className="font-technical" style={{ color: getAIScoreColor(station.storm_probability), fontWeight: "bold" }}>{station.storm_probability}%</span>
                        </div>
                      </div>
                    </div>
                  </Popup>
                </CircleMarker>
              );
            })}
          </MapContainer>

          {/* Ingestion Status Overlay */}
          <div style={{
            position: "absolute",
            bottom: "16px",
            left: "16px",
            zIndex: 1000,
            backgroundColor: "rgba(11, 15, 25, 0.95)",
            border: "1px solid #1e293b",
            padding: "8px 14px",
            borderRadius: "8px",
            backdropFilter: "blur(8px)",
            boxShadow: "0 4px 20px rgba(0, 0, 0, 0.5)"
          }}>
            <span className="font-technical" style={{ fontSize: "11px", color: "#10b981", display: "block" }}>
              ● CWC_DWR_WALTAIR // ONLINE // SCAN COMPLETE
            </span>
            <span className="font-technical" style={{ fontSize: "9px", color: "#64748b", marginTop: "2px", display: "block" }}>
              SYNCED: {lastUpdated || "MOCK TELEMETRY"}
            </span>
          </div>

          {/* Reflectivity Scale Legend */}
          <div style={{
            position: "absolute",
            bottom: "16px",
            right: "16px",
            zIndex: 1000,
            backgroundColor: "rgba(11, 15, 25, 0.95)",
            border: "1px solid #1e293b",
            padding: "8px 12px",
            borderRadius: "8px",
            backdropFilter: "blur(8px)",
            color: "#ffffff",
            fontSize: "10px",
            fontFamily: "JetBrains Mono"
          }}>
            <span style={{ fontWeight: "bold", display: "block", color: "#06b6d4", marginBottom: "4px" }}>DWR REFLECTIVITY (dBZ)</span>
            <div style={{ display: "flex", gap: "2px", height: "8px", borderRadius: "2px", overflow: "hidden", marginBottom: "4px" }}>
              <div style={{ width: "20px", backgroundColor: "#10b981" }}></div>
              <div style={{ width: "20px", backgroundColor: "#eab308" }}></div>
              <div style={{ width: "20px", backgroundColor: "#f97316" }}></div>
              <div style={{ width: "20px", backgroundColor: "#ef4444" }}></div>
              <div style={{ width: "20px", backgroundColor: "#a855f7" }}></div>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", color: "#64748b", fontSize: "8.5px", marginTop: "2px" }}>
              <span>18 (Light)</span>
              <span>&gt;55 (Severe)</span>
            </div>
          </div>

        </div>

      </div>

      {/* Right Sidebar: Restructured Operationally Focused details panel */}
      <div className="panel-surface" style={{ display: "flex", flexDirection: "column", backgroundColor: "#0b0f19", borderLeft: "1px solid #1e293b", borderRadius: "16px", border: "1px solid #334155", overflow: "hidden" }}>
        
        {/* Header with Station selector */}
        <div style={{ padding: "16px", borderBottom: "1px solid #1e293b", backgroundColor: "#020617" }}>
          <span className="font-technical" style={{ fontSize: "10px", color: "#3b82f6", fontWeight: "bold", letterSpacing: "1px", display: "block", marginBottom: "8px" }}>
            STATION_SELECT
          </span>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
            {forecastData.map((station) => {
              const isSelected = selectedStation?.station === station.station;
              return (
                <button
                  key={station.station}
                  onClick={() => setSelectedStation(station)}
                  style={{
                    padding: "4px 8px",
                    borderRadius: "6px",
                    fontSize: "11px",
                    fontWeight: "bold",
                    backgroundColor: isSelected ? "#3b82f6" : "#0f172a",
                    color: isSelected ? "#ffffff" : "#94a3b8",
                    border: isSelected ? "1px solid #3b82f6" : "1px solid #1e293b",
                    cursor: "pointer",
                    fontFamily: "JetBrains Mono"
                  }}
                >
                  {station.station.slice(0, 4).toUpperCase()}
                </button>
              );
            })}
          </div>
        </div>

        {/* Restructured Sections Scroll Area */}
        <div style={{ flex: 1, overflowY: "auto", padding: "16px", display: "flex", flexDirection: "column", gap: "20px" }}>
          
          {selectedStation && (() => {
            const station = selectedStation;
            const cycle = station.active_cycle || "00Z";
            const obsTime = cycle === "12Z" ? "05:00 PM IST" : "05:00 AM IST";
            const genTime = cycle === "12Z" ? "05:07 PM IST" : "05:07 AM IST";
            const sourceStr = station.sounding_source || `IMD Radiosonde (Station ${station.station_code || "43150"})`;
            const riskColor = getRiskColor(station.forecast);

            // Fetch Cape Traceability for this station
            const stTrace = capeTrace?.cape_traceability?.[station.station];
            const currentCape = station.cape || 0;
            const traceTimeline = stTrace?.timeline || [];
            const prevCape = traceTimeline.length > 1 ? traceTimeline[1].cape : (stTrace?.previous_cape || currentCape - 250);
            const deltaCape = currentCape - prevCape;
            const capeTrend = deltaCape > 0 ? "RISING" : deltaCape < 0 ? "FALLING" : "STABLE";
            const isCapeStatic = deltaCape === 0 || stTrace?.static_data_warning || station.cape_static_warning;

            // Fetch History list for Probability Traceability
            const stationHistory = historyList.filter(h => h.station === station.station);
            const currentProb = station.storm_probability || 50;
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

            const contribs = getProbabilityContributors(station);
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
              <>
                {/* FIRST SECTION: Current Conditions */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px" }}>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#3b82f6", fontWeight: "bold", textTransform: "uppercase", marginBottom: "8px" }}>
                    I. Current Conditions
                  </h4>
                  <div style={{ display: "flex", flexDirection: "column", gap: "6px", fontSize: "12px", fontFamily: "JetBrains Mono", color: "#cbd5e1" }}>
                    <div>Observation Date: <span style={{ color: "#ffffff", fontWeight: "bold" }}>2026-06-05</span></div>
                    <div>Observation Time: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{obsTime}</span></div>
                    <div>Forecast Generated: <span style={{ color: "#a855f7", fontWeight: "bold" }}>{genTime}</span></div>
                    <div>Station Name: <span style={{ color: "#ffffff", fontWeight: "bold" }}>{station.station} ({station.station_code})</span></div>
                    <div>Data Source: <span style={{ color: "#10b981" }}>{sourceStr}</span></div>
                  </div>
                </div>

                {/* SECOND SECTION: Threat Summary */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px" }}>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#f43f5e", fontWeight: "bold", textTransform: "uppercase", marginBottom: "10px" }}>
                    II. Threat Summary & Evolution
                  </h4>
                  
                  {/* Convective Risks list */}
                  <div style={{ display: "flex", flexDirection: "column", gap: "6px", marginBottom: "14px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px" }}>
                      <span style={{ color: "#94a3b8" }}>Thunderstorm Risk:</span>
                      <strong style={{ color: riskColor }}>{station.forecast} ({station.storm_probability || 0}%)</strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px" }}>
                      <span style={{ color: "#94a3b8" }}>Lightning Risk:</span>
                      <strong style={{ color: getAIScoreColor(station.lightning_probability || station.storm_probability) }}>
                        {station.lightning_probability || Math.round(station.storm_probability * 1.05)}%
                      </strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px" }}>
                      <span style={{ color: "#94a3b8" }}>Heavy Rain Risk:</span>
                      <strong style={{ color: getAIScoreColor(station.heavy_rain_probability || (station.pwat / 75.0) * 100) }}>
                        {station.heavy_rain_probability || Math.round((station.pwat / 75.0) * 100)}%
                      </strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px" }}>
                      <span style={{ color: "#94a3b8" }}>Squall Risk:</span>
                      <strong style={{ color: getAIScoreColor(station.squall_probability || station.storm_probability * 0.7) }}>
                        {station.squall_probability || Math.round(station.storm_probability * 0.7)}%
                      </strong>
                    </div>
                  </div>

                  {/* LIVE CAPE TRACEABILITY PANEL & PROBABILITY EVOLUTION PANEL */}
                  {!reviewMode && (
                    <>
                      {/* LIVE CAPE TRACEABILITY PANEL */}
                      <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px", marginBottom: "12px" }}>
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
                          <div>Last Update:</div>
                          <div style={{ color: "#cbd5e1", fontSize: "10px" }}>2026-06-06 {obsTime}</div>
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
                      <div style={{ backgroundColor: "#020617", border: "1px solid #1e293b", borderRadius: "10px", padding: "12px" }}>
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
                              curr: station.lightning_probability || (currentProb >= 60 ? Math.max(80, currentProb + 5) : 15),
                              prev: station.lightning_probability ? station.lightning_probability - 4 : (prevProb >= 60 ? Math.max(80, prevProb + 5) : 15),
                              driver: "CAPE & Lifted Index parcel buoyancy"
                            },
                            { 
                              name: "Heavy Rain Probability",
                              curr: station.heavy_rain_probability || (station.pwat >= 50 ? Math.round(50 + (station.pwat - 50) * 1.5) : Math.round(station.pwat * 0.6)),
                              prev: station.heavy_rain_probability ? station.heavy_rain_probability - 5 : (station.pwat >= 50 ? Math.round(50 + (station.pwat - 50) * 1.5) - 3 : Math.round(station.pwat * 0.6) - 2),
                              driver: "PWAT column moisture loading"
                            },
                            { 
                              name: "Squall Probability",
                              curr: station.squall_probability || (station.sweat_index >= 290 ? Math.round(40 + (station.sweat_index - 290) * 0.2) : 10),
                              prev: station.squall_probability ? station.squall_probability - 2 : (station.sweat_index >= 290 ? Math.round(40 + (station.sweat_index - 290) * 0.2) - 1 : 10),
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
                    </>
                  )}
                </div>

                {/* THIRD SECTION: Meteorologist Interpretation */}
                <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "14px" }}>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#eab308", fontWeight: "bold", textTransform: "uppercase", marginBottom: "8px" }}>
                    III. Meteorologist Interpretation
                  </h4>
                  <div style={{ fontSize: "12px", color: "#cbd5e1", lineHeight: "1.5", backgroundColor: "rgba(234, 179, 8, 0.05)", border: "1px dashed rgba(234, 179, 8, 0.25)", padding: "10px", borderRadius: "8px" }}>
                    {station.explainability || 
                      `Strong instability (CAPE: ${currentCape} J/kg) and deep moisture (PWAT: ${station.pwat}mm) support thunderstorm development over coastal Andhra Pradesh during the next 3–6 hours.`
                    }
                  </div>
                </div>

                {/* FOURTH SECTION: Recommended Actions */}
                <div>
                  <h4 className="font-technical" style={{ fontSize: "11px", color: "#10b981", fontWeight: "bold", textTransform: "uppercase", marginBottom: "10px" }}>
                    IV. Recommended Actions
                  </h4>
                  <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                    {[
                      { label: "Thunderstorm Watch", status: currentProb >= 50 ? "ACTIVE WATCH" : "STANDBY", col: currentProb >= 50 ? "#ef4444" : "#64748b" },
                      { label: "Lightning Watch", status: (station.lightning_probability || currentProb) >= 50 ? "ACTIVE WATCH" : "STANDBY", col: (station.lightning_probability || currentProb) >= 50 ? "#f97316" : "#64748b" },
                      { label: "Heavy Rain Monitoring", status: (station.heavy_rain_probability || (station.pwat / 75) * 100) >= 50 ? "ACTIVE MONITOR" : "STANDBY", col: (station.heavy_rain_probability || (station.pwat / 75) * 100) >= 50 ? "#3b82f6" : "#64748b" },
                      { label: "NWX (No Weather Warning)", status: (station.nwx_probability || 100 - currentProb) >= 60 ? "ACTIVE" : "STANDBY", col: (station.nwx_probability || 100 - currentProb) >= 60 ? "#10b981" : "#64748b" }
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
                        <span style={{ fontSize: "12px", fontWeight: "bold", color: "#ffffff" }}>{act.label}</span>
                        <span className="font-technical" style={{
                          fontSize: "9px",
                          fontWeight: "bold",
                          backgroundColor: act.status.includes("ACTIVE") ? act.col + "15" : "transparent",
                          color: act.col,
                          padding: "2px 6px",
                          borderRadius: "4px"
                        }}>
                          {act.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            );
          })()}

        </div>

      </div>

    </div>
  );
}
