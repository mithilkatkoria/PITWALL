"""Pure explainable formulas; all penalties are measured in seconds."""
from .models import RaceConfig, TyreCompound, integer, number


def degradation(tyre: TyreCompound, age: int) -> float:
    integer(age, "Tyre age")
    loss = tyre.degradation_rate * age
    number(loss, "Degradation loss")
    return loss


def fuel_effect(config: RaceConfig, lap: int) -> float:
    integer(lap, "Lap number", 1, config.laps)
    if config.laps == 1:
        return 0.0
    return config.initial_fuel_penalty * ((config.laps - lap) / (config.laps - 1))


def lap_time(config: RaceConfig, tyre: TyreCompound, age: int,
             lap: int, pit_loss: float = 0.0) -> tuple[float, float, float]:
    number(pit_loss, "Pit loss")
    wear = degradation(tyre, age)
    fuel = fuel_effect(config, lap)
    total = (config.circuit.base_lap_time + config.driver.pace_delta
             + tyre.base_pace_delta + wear + fuel + pit_loss)
    number(total, "Calculated lap time", positive=True)
    return total, wear, fuel
