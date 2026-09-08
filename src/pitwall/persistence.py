"""Strict versioned JSON. Loading data never runs arbitrary code."""
from dataclasses import asdict, dataclass
from enum import Enum
import json
from pathlib import Path
import tempfile
import os
from .conditions import Conditions
from .events import RaceEvent, EventType, EventQueue, Weather
from .models import Circuit, Compound, Driver, PitStopPlan, RaceConfig, Strategy, TyreCompound

MAX_FILE_BYTES = 1_048_576


@dataclass(frozen=True)
class Scenario:
    config: RaceConfig
    conditions: Conditions
    strategies: tuple[Strategy, ...]

    def __post_init__(self):
        if not isinstance(self.config, RaceConfig) or not isinstance(self.conditions, Conditions):
            raise ValueError("Scenario requires race configuration and conditions")
        if not isinstance(self.strategies, tuple) or not 1 <= len(self.strategies) <= 20 or not all(isinstance(s, Strategy) for s in self.strategies):
            raise ValueError("Scenario requires 1..20 strategies")
        if len({s.name.strip().casefold() for s in self.strategies}) != len(self.strategies):
            raise ValueError("Scenario strategy names must be unique")
        for strategy in self.strategies:
            strategy.validate_for(self.config)
        if len(self.conditions.events) > 500:
            raise ValueError("Scenario allows at most 500 events")
        EventQueue(self.conditions.events, self.config.laps)
        if self.conditions.variation >= self.config.circuit.base_lap_time:
            raise ValueError("Variation amplitude must be below base lap time")


def to_data(scenario: Scenario) -> dict:
    return {"schema_version": 1, **asdict(scenario)}


def enum_json(value):
    if isinstance(value, Enum):
        return value.value
    raise TypeError(f"Cannot encode {type(value).__name__}")


def fields(data, expected):
    if not isinstance(data, dict) or set(data) != set(expected):
        raise ValueError(f"Expected fields: {', '.join(expected)}")
    return dict(data)


def array(data, name):
    if not isinstance(data, list):
        raise ValueError(f"{name} must be a JSON array")
    return data


def from_data(data: dict) -> Scenario:
    try:
        top = fields(data, ("schema_version", "config", "conditions", "strategies"))
        if type(top["schema_version"]) is not int or top["schema_version"] != 1:
            raise ValueError("Unsupported schema version; expected 1")
        race = fields(top["config"], ("laps", "circuit", "driver", "tyres", "initial_fuel_penalty"))
        circuit = Circuit(**fields(race["circuit"], ("name", "base_lap_time", "pit_lane_loss")))
        driver = Driver(**fields(race["driver"], ("name", "pace_delta")))
        tyres = []
        for tyre in array(race["tyres"], "Tyres"):
            t = fields(tyre, ("name", "base_pace_delta", "degradation_rate", "recommended_life"))
            t["name"] = Compound(t["name"])
            tyres.append(TyreCompound(**t))
        config = RaceConfig(race["laps"], circuit, driver, tuple(tyres), race["initial_fuel_penalty"])
        cond = fields(top["conditions"], ("initial_weather", "events", "damp_penalty", "wet_penalty", "safety_car_penalty", "safety_car_pit_factor", "seed", "variation"))
        cond["initial_weather"] = Weather(cond["initial_weather"])
        events = []
        for event in array(cond["events"], "Events"):
            e = fields(event, ("lap", "kind", "weather"))
            events.append(RaceEvent(e["lap"], EventType(e["kind"]), Weather(e["weather"]) if e["weather"] is not None else None))
        cond["events"] = tuple(events)
        strategies = []
        for strategy in array(top["strategies"], "Strategies"):
            s = fields(strategy, ("name", "starting_compound", "planned_stops"))
            stops = []
            for stop in array(s["planned_stops"], "Planned stops"):
                p = fields(stop, ("lap", "compound", "stationary_time"))
                stops.append(PitStopPlan(p["lap"], Compound(p["compound"]), p["stationary_time"]))
            strategies.append(Strategy(s["name"], Compound(s["starting_compound"]), tuple(stops)))
        return Scenario(config, Conditions(**cond), tuple(strategies))
    except (TypeError, KeyError, AttributeError) as exc:
        raise ValueError(f"Malformed scenario: {exc}") from exc


def reject_constant(value):
    raise ValueError(f"Non-finite JSON value {value} is not allowed")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def load_scenario(path: Path) -> Scenario:
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_FILE_BYTES + 1)
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("Scenario file exceeds 1 MiB")
    try:
        return from_data(json.loads(raw.decode('utf-8-sig'), parse_constant=reject_constant, object_pairs_hook=unique_keys))
    except (UnicodeError, RecursionError) as exc:
        raise ValueError("Scenario is not valid supported UTF-8 JSON") from exc


def save_scenario(path: Path, scenario: Scenario) -> None:
    # Round-trip validation verifies the serialized contract before touching destination.
    text = json.dumps(to_data(scenario), default=enum_json, allow_nan=False, indent=2)
    from_data(json.loads(text))
    if len(text.encode('utf-8')) > MAX_FILE_BYTES:
        raise ValueError("Scenario file exceeds 1 MiB")
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
