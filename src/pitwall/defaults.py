"""Illustrative tunable model inputs. These are not telemetry or calibrated data."""
from .models import Circuit, Compound, Driver, RaceConfig, TyreCompound


def default_config() -> RaceConfig:
    return RaceConfig(50, Circuit("Illustrative circuit", 90, 20), Driver("Reference driver"), (
        TyreCompound(Compound.SOFT, 0, .16, 15),
        TyreCompound(Compound.MEDIUM, .5, .09, 25),
        TyreCompound(Compound.HARD, 1, .045, 35),
    ), 3)
