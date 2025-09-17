from typing import List
from pydantic import BaseModel


class StrategyOption(BaseModel):
    id: str
    pit_laps: List[int]
    compounds: List[str]
    exp_total_time: float
    notes: str


class StrategyResponse(BaseModel):
    timestamp: str
    session_key: int
    driver_number: int
    lap: int
    options: List[StrategyOption]
