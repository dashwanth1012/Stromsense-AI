import { buildWsUrl } from "../config/environment";

export const createAtmosphericSocket = () => new WebSocket(buildWsUrl("/stream/atmospheric"));

export const getAtmosphericSocketUrl = () => buildWsUrl("/stream/atmospheric");
