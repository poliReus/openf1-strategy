import { StrategyResponse } from "../types";

interface Props {
  driver: StrategyResponse;
}

export default function DriverCard({ driver }: Props) {
  return (
    <div className="p-4 rounded-2xl shadow-md bg-white flex flex-col">
      <h2 className="text-xl font-bold mb-2">
        Driver #{driver.driver_number} (Lap {driver.lap})
      </h2>
      <ul className="space-y-1">
        {driver.options.map((opt) => (
          <li key={opt.id} className="p-2 border rounded-md">
            <span className="font-mono">{opt.id}</span> →{" "}
            {opt.compounds.join("-")} | Pit:{" "}
            {opt.pit_laps.join(", ")} | Time: {opt.exp_total_time}s
            <br />
            <span className="text-sm text-gray-600">{opt.notes}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
