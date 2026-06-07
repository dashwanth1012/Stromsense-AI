/**
 * Meteorological Adapter Matrix for future GIS & Radar Integrations
 * Establishes ready-to-use hooks for connecting Doppler, INSAT satellite,
 * and external NOAA archives.
 */
export const GISAdapter = {
  /**
   * Fetches INSAT-3D Satellite Cloud Imagery Interface URL or tile specifications.
   * Prepared for WMS (Web Map Service) tile layers mapping INSAT-3D IR feeds.
   * @param {Array} boundingBox [minLat, minLng, maxLat, maxLng]
   */
  fetchINSATCloudOverlay: async (boundingBox) => {
    // Current stub generates a mock url demonstrating live satellite feed readiness
    const dateStr = new Date().toISOString().slice(0, 13).replace('T', '-');
    return `https://satellite.imd.gov.in/img/3D_L1B_STD_IR1_${dateStr}.png`;
  },
  
  /**
   * Fetches Doppler Weather Radar (DWR) precipitation overlay tiles.
   * Prepared for real Doppler precipitation overlays (reflectivity dBZ maps).
   * @param {string} stationCode Station ID (e.g. 43150)
   */
  fetchDopplerRadarOverlay: async (stationCode) => {
    return {
      source: `https://radar.imd.gov.in/dwr_reflectivity/${stationCode}`,
      format: "geojson-tile",
      opacity: 0.65,
      scale: "dBZ_standard"
    };
  },

  /**
   * Fetches real meteorological upper-air soundings from NOAA / IMD archives.
   * Currently triggers a detailed warning showing how mock telemetry remains active as a fallback.
   * @param {string} stationId Station ID
   */
  fetchRealSoundings: async (stationId) => {
    console.warn(`GISAdapter: NOAA/IMD Real-Time Sounding feed requested for station: ${stationId}. Direct channel idle. Mock telemetry active.`);
    return null;
  }
};
