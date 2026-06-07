const trimTrailingSlash = (value = "") => String(value).trim().replace(/\/+$/, "");

const runtimeOrigin = () => {
  if (typeof window === "undefined") return "";
  return window.location.origin;
};

const devApiOrigin = () => {
  if (typeof window === "undefined") return "";
  return `${window.location.protocol}//${window.location.hostname}:8000`;
};

const envApiUrl = trimTrailingSlash(import.meta.env.VITE_API_URL || "");
const envWsUrl = trimTrailingSlash(import.meta.env.VITE_WS_URL || "");

export const APP_ENV = import.meta.env.VITE_APP_ENV || import.meta.env.MODE || "production";
export const API_BASE_URL = envApiUrl || (import.meta.env.DEV ? devApiOrigin() : runtimeOrigin());

const inferWsUrl = () => {
  if (envWsUrl) return envWsUrl;
  const source = API_BASE_URL || runtimeOrigin();
  if (!source) return "";
  if (source.startsWith("https://")) return source.replace(/^https:\/\//, "wss://");
  if (source.startsWith("http://")) return source.replace(/^http:\/\//, "ws://");
  return source;
};

export const WS_BASE_URL = trimTrailingSlash(inferWsUrl());

export const buildApiUrl = (path = "") => {
  const normalizedPath = String(path).startsWith("/") ? String(path) : `/${path}`;
  return `${trimTrailingSlash(API_BASE_URL)}${normalizedPath}`;
};

export const buildWsUrl = (path = "") => {
  const normalizedPath = String(path).startsWith("/") ? String(path) : `/${path}`;
  return `${trimTrailingSlash(WS_BASE_URL)}${normalizedPath}`;
};

export const ENVIRONMENT_STATUS = {
  appEnv: APP_ENV,
  apiConfigured: Boolean(API_BASE_URL),
  wsConfigured: Boolean(WS_BASE_URL),
};
