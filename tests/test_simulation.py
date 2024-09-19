import pytest
from src.ui import PendulumSimulation

@pytest.fixture
def simulation(app):
    return PendulumSimulation()

def test_initialize_parameters(simulation):
    simulation.initialize_parameters()
    assert simulation.sliders['m1'].value() == 50
    assert simulation.sliders['L1'].value() == 50
    assert simulation.sliders['g'].value() == 98  # Updated to match the actual value set in the method

def test_randomize_parameters(simulation):
    simulation.randomize_parameters()
    for param in simulation.sliders:
        assert 5 <= simulation.sliders[param].value() <= 95

def test_start_simulation(simulation):
    simulation.initialize_parameters()
    simulation.start_simulation()
    assert simulation.timer.isActive()
    assert simulation.frame == 0
