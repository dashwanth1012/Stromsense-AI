import { API_BASE_URL, buildApiUrl } from "../config/environment";

const TOKEN_KEY = "stormsense_token";

export const getStoredToken = () => {
  try {
    return localStorage.getItem(TOKEN_KEY) || "";
  } catch {
    return "";
  }
};

const shouldAttachToken = (token) => token && token !== "GUEST_SESSION_TOKEN_STORMSENSE";

const parseResponseBody = async (response) => {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
};

const createApiError = (message, response, data) => {
  const error = new Error(message);
  error.isStormSenseApiError = true;
  error.response = response ? { status: response.status, data } : null;
  error.operationalMessage = data?.detail || data?.message || message;
  return error;
};

const requestWithTimeout = async (url, options, timeoutMs) => {
  if (options.signal || !timeoutMs) {
    return fetch(url, options);
  }
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timeoutId);
  }
};

export const apiRequest = async (config, options = {}) => {
  const retries = Number(options.retries ?? 0);
  let lastError;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      const method = (config.method || "GET").toUpperCase();
      const token = getStoredToken();
      const headers = { ...(config.headers || {}) };
      const isFormData = config.data instanceof FormData;

      if (shouldAttachToken(token)) {
        headers.Authorization = `Bearer ${token}`;
      }
      if (config.data !== undefined && !isFormData && !headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
      }

      const response = await requestWithTimeout(buildApiUrl(config.url), {
        method,
        headers,
        body: method === "GET" || method === "HEAD"
          ? undefined
          : isFormData
            ? config.data
            : JSON.stringify(config.data ?? {}),
        signal: config.signal,
      }, config.timeout ?? 30000);

      const data = await parseResponseBody(response);
      if (!response.ok) {
        throw createApiError(`StormSense API returned HTTP ${response.status}`, response, data);
      }
      return { data, status: response.status, headers: response.headers };
    } catch (error) {
      lastError = error;
      const status = error.response?.status;
      const canRetry = !status || status >= 500 || status === 429;
      if (!canRetry || attempt >= retries || isApiCancel(error)) break;
      await new Promise((resolve) => setTimeout(resolve, 400 * (attempt + 1)));
    }
  }

  if (lastError?.isStormSenseApiError) throw lastError;
  throw createApiError(lastError?.message || "StormSense API request failed.", null, null);
};

export const apiGet = async (path, config = {}, options = { retries: 1 }) => {
  const response = await apiRequest({ method: "GET", url: path, ...config }, options);
  return response.data;
};

export const apiPost = async (path, data = {}, config = {}, options = {}) => {
  const response = await apiRequest({ method: "POST", url: path, data, ...config }, options);
  return response.data;
};

export const apiUpload = async (path, formData, config = {}) => {
  const headers = { ...(config.headers || {}) };
  delete headers["Content-Type"];
  const response = await apiRequest({
    method: "POST",
    url: path,
    data: formData,
    timeout: 60000,
    ...config,
    headers,
  });
  return response.data;
};

export const isApiCancel = (error) => (
  error?.name === "AbortError" ||
  error?.name === "CanceledError" ||
  error?.message?.toLowerCase?.().includes("aborted")
);

const apiClient = {
  baseURL: API_BASE_URL,
  request: apiRequest,
  get: async (url, config = {}) => apiRequest({ method: "GET", url, ...config }),
  post: async (url, data = {}, config = {}) => apiRequest({ method: "POST", url, data, ...config }),
};

export { buildApiUrl };
export default apiClient;
