import { useEffect, useState } from "react";
import { fetchSessionOptions } from "../services/api";
import DriverCard from "../components/DriverCard";
import { StrategyResponse } from "../types";

export default function Home() {
  const [drivers, setDrivers] = useState<Record<string, StrategyResponse>>({});

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchSessionOptions();
        setDrivers(data);
      } catch (err) {
        console.error("Failed to fetch session options", err);
      }
    }
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {Object.values(drivers).map((driver) => (
        <DriverCard key={driver.driver_number} driver={driver} />
      ))}
    </div>
  );
}
