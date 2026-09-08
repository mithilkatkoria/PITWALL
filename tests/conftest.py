import pytest
from pitwall.models import Circuit, Compound, Driver, RaceConfig, TyreCompound


@pytest.fixture
def config():
    return RaceConfig(5, Circuit("Manual example", 90, 20), Driver("Reference"), (
        TyreCompound(Compound.SOFT, 0, 0.2, 10),
        TyreCompound(Compound.MEDIUM, 0.5, 0.1, 20),
        TyreCompound(Compound.HARD, 1, 0.05, 30),
    ), 2)
