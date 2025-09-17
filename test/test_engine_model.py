from engine.model import score_options


def test_score_basic():
    state = {"last_lap": 10, "laps_times": [90.0, 89.5, 91.2], "compound": "M"}
    options = score_options(state, total_laps=60)
    assert len(options) >= 2
    for o in options:
        assert "exp_total_time" in o
        assert isinstance(o["exp_total_time"], float)
