from unittest.mock import Mock
import pytest
from greenrun import grid

def page(rows):
    return Mock(json=Mock(return_value={"response": {"data": rows}}), raise_for_status=Mock())

def test_fetch_fuel_mix_groups_by_hour_and_pages(monkeypatch):
    monkeypatch.setattr(grid, "API_KEY", "test")
    monkeypatch.setattr(grid, "PAGE_SIZE", 2)

    pages = [
        page([{"period": "2026-10-29T00", "fueltype": "COL", "value": "300"},
              {"period": "2026-10-29T00", "fueltype": "WND", "value": None}]),
        page([{"period": "2026-10-29T01", "fueltype": "COL", "value": "250"}]),
    ]
    get = Mock(side_effect=pages)
    monkeypatch.setattr(grid.requests, "get", get)

    assert grid.fetch_fuel_mix("MISO", "2026-10-29T00", "2026-10-29T01") == {
        "2026-10-29T00": {"COL": 300.0},
        "2026-10-29T01": {"COL": 250.0},
    }

    assert get.call_args_list[0].kwargs["params"]["facets[respondent][]"] == "MISO"
    assert get.call_args_list[1].kwargs["params"]["offset"] == 2

def test_fetch_fuel_mix_raises_on_http_error(monkeypatch):
    monkeypatch.setattr(grid, "API_KEY", "test")
    failing = page([])
    failing.raise_for_status.side_effect = grid.requests.HTTPError("403")
    monkeypatch.setattr(grid.requests, "get", Mock(return_value=failing))
    with pytest.raises(grid.requests.HTTPError):
        grid.fetch_fuel_mix("MISO", "2026-10-29T00", "2026-10-29T01")
