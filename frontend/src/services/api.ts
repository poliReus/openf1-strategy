import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
console.log("API BASE URL = ", import.meta.env.VITE_API_URL);


export async function fetchSessionOptions() {
  const res = await axios.get(`${API_BASE}/session/options`);
  return res.data;
}

export async function fetchDriverOptions(driverNumber: number) {
  const res = await axios.get(`${API_BASE}/drivers/${driverNumber}/options`);
  return res.data;
}
