export interface StrategyOption {
  id: string;
  pit_laps: number[];
  compounds: string[];
  exp_total_time: number;
  notes: string;
}

export interface StrategyResponse {
  timestamp: string;
  session_key: number;
  driver_number: number;
  lap: number;
  options: StrategyOption[];
}
