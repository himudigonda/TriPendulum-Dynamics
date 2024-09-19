import pytest
from src.ui import PendulumSimulation

@pytest.fixture
def simulation(app):
    return PendulumSimulation()

def test_ui_initialization(simulation):
    assert simulation.windowTitle() == "Three-Point Pendulum Simulation"
    assert simulation.centralWidget() is not None

def test_update_plots(simulation):
    simulation.initialize_parameters()
    simulation.start_simulation()
    simulation.update_plots()
    assert simulation.frame == 1
