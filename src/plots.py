import pyqtgraph as pg
from PySide6.QtGui import QColor

def setup_pendulum_plot():
    pendulum_plot = pg.PlotWidget()
    pendulum_plot.setAspectLocked()
    pendulum_plot.setBackground('k')  # Black background for simulation
    pendulum_plot.hideAxis('left')    # Hide axis for "black room" effect
    pendulum_plot.hideAxis('bottom')
    pendulum_curve = pendulum_plot.plot(pen=pg.mkPen('w', width=4))
    pendulum_points = []

    for i in range(3):
        point = pg.ScatterPlotItem(size=15, brush=pg.mkBrush(QColor(255, 165, 0)))
        pendulum_plot.addItem(point)
        pendulum_points.append(point)

    # Trace curves
    trace_curves = []
    for color in ['r', 'g', 'b']:
        trace_curve = pendulum_plot.plot(pen=pg.mkPen(color, width=2))
        trace_curves.append(trace_curve)

    return pendulum_plot, pendulum_curve, pendulum_points, trace_curves

def setup_energy_plot():
    """
    Set up the energy plot for the simulation.

    This function creates a plot widget for displaying the kinetic, potential,
    and total energy of the pendulum system over time.

    Returns:
        tuple: A tuple containing the energy plot widget and the curves for kinetic,
               potential, and total energy.
    """
    energy_plot = pg.PlotWidget()
    energy_plot.addLegend()
    energy_plot.setTitle("Energy vs Time")
    energy_plot.setLabel('left', 'Energy (J)')
    energy_plot.setLabel('bottom', 'Time (s)')
    kinetic_curve = energy_plot.plot(pen='r', name='Kinetic')
    potential_curve = energy_plot.plot(pen='g', name='Potential')
    total_curve = energy_plot.plot(pen='b', name='Total')

    return energy_plot, kinetic_curve, potential_curve, total_curve

def setup_velocity_plot():
    """
    Set up the velocity plot for the simulation.

    This function creates a plot widget for displaying the angular velocities
    of the pendulum system over time.

    Returns:
        tuple: A tuple containing the velocity plot widget and the curves for the
               angular velocities of the three pendulums.
    """
    velocity_plot = pg.PlotWidget()
    velocity_plot.addLegend()
    velocity_plot.setTitle("Angular Velocity vs Time")
    velocity_plot.setLabel('left', 'Angular Velocity (rad/s)')
    velocity_plot.setLabel('bottom', 'Time (s)')
    omega1_curve = velocity_plot.plot(pen='r', name='Omega1')
    omega2_curve = velocity_plot.plot(pen='g', name='Omega2')
    omega3_curve = velocity_plot.plot(pen='b', name='Omega3')

    return velocity_plot, omega1_curve, omega2_curve, omega3_curve
