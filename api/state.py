from typing import Dict
from api.models import StrategyResponse

# Cache: driver_number → StrategyResponse
latest_options: Dict[int, StrategyResponse] = {}


def update_driver_options(driver_number: int, response: StrategyResponse):
    latest_options[driver_number] = response


def get_driver_options(driver_number: int) -> StrategyResponse | None:
    return latest_options.get(driver_number)


def get_all_options() -> Dict[int, StrategyResponse]:
    return latest_options
