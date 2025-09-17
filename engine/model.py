from engine.config import PIT_LOSS, DEG, STINT


def guess_start_compound(driver_history) -> str:
    # if we ever added compound in telemetry, pick last known; else default M
    return driver_history.get("compound", "M")


def current_elapsed_time(driver_history) -> float:
    # sum known lap times; ignore None
    return sum(
        [
            lt
            for lt in driver_history.get("laps_times", [])
            if isinstance(lt, (int, float))
        ]
    )


def remaining_race_laps(total_laps: int, current_lap: int) -> int:
    return max(0, total_laps - current_lap)


def plan_one_stop(current_lap: int, start_compound: str, total_laps: int):
    # One-stop: pit around current_lap + typical stint length
    first_stint_left = STINT.get(start_compound, 22)
    pit = min(total_laps - 1, max(current_lap + 1, current_lap + first_stint_left))
    # Simple compounds: start -> H (safer)
    return {
        "id": f"1-stop-{pit}",
        "pit_laps": [pit],
        "compounds": [start_compound, "H"],
        "notes": "baseline",
    }


def plan_two_stop(current_lap: int, start_compound: str, total_laps: int):
    # Two-stop: split remaining into ~3 stints
    rem = remaining_race_laps(total_laps, current_lap)
    leg = max(10, rem // 3)
    pit1 = min(total_laps - 1, current_lap + leg)
    pit2 = min(total_laps - 1, pit1 + leg)
    comps = [start_compound, "M", "H"]
    return {
        "id": f"2-stop-{pit1}-{pit2}",
        "pit_laps": [pit1, pit2],
        "compounds": comps,
        "notes": "balanced clean-air",
    }


def estimate_total_time(
    elapsed: float,
    options: list[dict],
    current_lap: int,
    total_laps: int,
    compound_deg: dict,
):
    # naive projection: deg * laps + pit losses
    results = []
    rem = remaining_race_laps(total_laps, current_lap)
    for opt in options:
        n_pits = len(opt["pit_laps"])
        proj_deg = 0.0
        # split remaining laps roughly across segments (#stints = pits+1)
        segments = n_pits + 1
        seg_len = max(1, rem // segments) if segments else rem
        # sum degradation per segment using compounds in option (cycle if missing)
        comps = opt["compounds"] or ["M"]
        for i in range(segments):
            c = comps[min(i, len(comps) - 1)]
            proj_deg += compound_deg.get(c, 0.06) * seg_len
        exp_total = elapsed + proj_deg + PIT_LOSS * n_pits
        results.append({**opt, "exp_total_time": round(exp_total, 3)})
    # sort by exp_total_time asc
    results.sort(key=lambda x: x["exp_total_time"])
    return results


def score_options(driver_state: dict, total_laps: int):
    current_lap = driver_state.get("last_lap", 1)
    start_comp = guess_start_compound(driver_state)
    elapsed = current_elapsed_time(driver_state)

    opt1 = plan_one_stop(current_lap, start_comp, total_laps)
    opt2 = plan_two_stop(current_lap, start_comp, total_laps)
    options = [opt1, opt2]
    options = estimate_total_time(elapsed, options, current_lap, total_laps, DEG)
    return options
