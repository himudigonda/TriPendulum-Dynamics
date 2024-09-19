# tests/test_ui.py
import pytest
from src.ui import PendulumSimulation  # Add this import statement

@pytest.fixture
def simulation(app):
    return PendulumSimulation()

def test_window_title(simulation):
    """
    Test to ensure the window title of the simulation is correct.

    Args:
        simulation: An instance of the PendulumSimulation class.

    Asserts:
        The window title is "Three-Point Pendulum Simulation".
        The central widget of the simulation is not None.
    """
    assert simulation.windowTitle() == "Three-Point Pendulum Simulation"
    assert simulation.centralWidget() is not None

def test_update_plots(simulation):
    """
    Test to ensure the plots are updated correctly during the simulation.

    Args:
        simulation: An instance of the PendulumSimulation class.

    Asserts:
        The frame count is incremented to 1 after updating plots.
    """
    simulation.initialize_parameters()
    simulation.start_simulation()
    simulation.update_plots()
    assert simulation.frame == 1
