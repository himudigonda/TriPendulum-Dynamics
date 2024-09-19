import numpy as np
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel, QPushButton, QProgressBar)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPalette, QBrush, QLinearGradient
import pyqtgraph as pg
import random

from .simulation import PendulumSimulator
from .plots import setup_pendulum_plot, setup_energy_plot, setup_velocity_plot
from .utils import create_dark_palette

class PendulumSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Three-Point Pendulum Simulation')
        self.setPalette(create_dark_palette())
        self.showMaximized()

        main_layout = QHBoxLayout()

        control_layout = self.setup_control_panel()
        plot_layout = self.setup_plots()

        control_widget = QWidget()
        control_widget.setLayout(control_layout)
        control_widget.setFixedWidth(400)

        plot_widget = QWidget()
        plot_widget.setLayout(plot_layout)

        main_layout.addWidget(control_widget)
        main_layout.addWidget(plot_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.initialize_parameters()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)

        self.trace_data = [[], [], []]
        self.trace_duration = 10
        self.simulation_speed = 1.0

        self.simulator = PendulumSimulator()

    def setup_control_panel(self):
        control_layout = QVBoxLayout()
        self.sliders = {}

        slider_font = QFont("Roboto", 12, QFont.Bold)
        label_font = QFont("Roboto", 12)

        for param in ['m1', 'm2', 'm3', 'L1', 'L2', 'L3', 'b', 'g', 'theta1', 'theta2', 'theta3', 'sim_time']:
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setStyleSheet("""
                QSlider {
                    height: 20px;
                }
                QSlider::groove:horizontal {
                    background: #303030;
                    height: 10px;
                }
                QSlider::handle:horizontal {
                    background: #ff8c00;
                    border: 2px solid #ff8c00;
                    width: 20px;
                    margin: -10px 0;
                    border-radius: 10px;
                }
                """)
            slider.setFont(slider_font)

            label = QLabel(f"{param}: 1.0")
            label.setFont(label_font)
            label.setStyleSheet("color: white; padding: 5px;")
            control_layout.addWidget(label)
            control_layout.addWidget(slider)

            slider.setToolTip(f"Adjust the {param} parameter")
            slider.valueChanged.connect(lambda value, p=param, l=label: self.update_label(value, p, l))
            self.sliders[param] = slider

        self.start_button = QPushButton('Start Simulation')
        self.start_button.setFont(slider_font)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.start_button.clicked.connect(self.start_simulation)
        control_layout.addWidget(self.start_button)

        self.play_pause_button = QPushButton('Pause')
        self.play_pause_button.setFont(slider_font)
        self.play_pause_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        control_layout.addWidget(self.play_pause_button)

        self.reset_button = QPushButton('Reset to Real-World Parameters')
        self.reset_button.setFont(slider_font)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.reset_button.clicked.connect(self.reset_parameters)
        control_layout.addWidget(self.reset_button)

        self.randomize_button = QPushButton('Randomize Parameters')
        self.randomize_button.setFont(slider_font)
        self.randomize_button.setStyleSheet("""
            QPushButton {
                background-color: #ff8c00;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e07b00;
            }
        """)
        self.randomize_button.clicked.connect(self.randomize_parameters)
        control_layout.addWidget(self.randomize_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #303030;
                border-radius: 5px;
                background: #303030;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #007bff;
            }
        """)
        control_layout.addWidget(self.progress_bar)

        return control_layout

    def setup_plots(self):
        plot_layout = QVBoxLayout()

        self.pendulum_plot, self.pendulum_curve, self.pendulum_points, self.trace_curves = setup_pendulum_plot()
        plot_layout.addWidget(self.pendulum_plot)

        self.energy_plot, self.kinetic_curve, self.potential_curve, self.total_curve = setup_energy_plot()
        plot_layout.addWidget(self.energy_plot)

        self.velocity_plot, self.omega1_curve, self.omega2_curve, self.omega3_curve = setup_velocity_plot()
        plot_layout.addWidget(self.velocity_plot)

        return plot_layout

    def initialize_parameters(self):
        self.sliders['m1'].setValue(50)  # 1 kg
        self.sliders['m2'].setValue(50)  # 1 kg
        self.sliders['m3'].setValue(50)  # 1 kg
        self.sliders['L1'].setValue(50)  # 1 m
        self.sliders['L2'].setValue(50)  # 1 m
        self.sliders['L3'].setValue(50)  # 1 m
        self.sliders['b'].setValue(5)   # 0.1 Ns/m
        self.sliders['g'].setValue(98)  # 9.8 m/s^2
        self.sliders['theta1'].setValue(85)  # 25 degrees (starting from right)
        self.sliders['theta2'].setValue(85)  # 0 degrees
        self.sliders['theta3'].setValue(85)  # -25 degrees
        self.sliders['sim_time'].setValue(60)  # 30 seconds

    def update_label(self, value, param, label):
        if param in ['m1', 'm2', 'm3', 'L1', 'L2', 'L3']:
            val = value / 50
        elif param == 'b':
            val = value / 500
        elif param == 'g':
            val = value / 10
        elif param == 'sim_time':
            val = value / 2
        else:  # theta
            val = value - 50
            if 'theta' in param:
                val = value - 50
                label.setText(f"{param} (deg): {val:.0f}°")
                return
        label.setText(f"{param}: {val:.2f}")

    def randomize_parameters(self):
        for param in self.sliders:
            random_value = random.uniform(0.05, 0.95) * 100
            self.sliders[param].setValue(int(random_value))

    def reset_parameters(self):
        self.initialize_parameters()

    def get_parameters(self):
        params = {}
        for param, slider in self.sliders.items():
            if param in ['m1', 'm2', 'm3', 'L1', 'L2', 'L3']:
                params[param] = slider.value() / 50
            elif param == 'b':
                params[param] = slider.value() / 500
            elif param == 'g':
                params[param] = slider.value() / 10
            elif param == 'sim_time':
                params[param] = slider.value() / 2
            else:  # theta
                params[param] = np.radians(slider.value() - 50)  # Convert degrees to radians internally
        return params

    def start_simulation(self):
        params = self.get_parameters()
        self.simulator.setup_simulation(params)
        self.frame = 0
        self.trace_data = [[], [], []]
        self.timer.start(20)  # 50 fps

    def toggle_play_pause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.play_pause_button.setText('Play')
        else:
            self.timer.start(20)
            self.play_pause_button.setText('Pause')

    def update_plots(self):
        if self.frame >= len(self.simulator.t_eval):
            self.timer.stop()
            return

        params = self.get_parameters()
        t = self.simulator.t_eval[:self.frame+1]
        solution = self.simulator.solution.y[:, :self.frame+1]

        # Update pendulum plot
        x1, y1, x2, y2, x3, y3 = self.simulator.get_positions(solution[:, -1], params)

        self.pendulum_curve.setData([0, x1, x2, x3], [0, y1, y2, y3])
        self.pendulum_points[0].setData([x1], [y1])
        self.pendulum_points[1].setData([x2], [y2])
        self.pendulum_points[2].setData([x3], [y3])

        # Update trace
        self.trace_data[0].append((x1, y1))
        self.trace_data[1].append((x2, y2))
        self.trace_data[2].append((x3, y3))

        visible_frames = int(self.trace_duration * len(self.trace_data[0]) / self.simulator.t_eval[-1])

        for i, trace_curve in enumerate(self.trace_curves):
            trace_data = self.trace_data[i][-visible_frames:] if visible_frames else self.trace_data[i]
            if trace_data:
                x, y = zip(*trace_data)
                trace_curve.setData(x, y)

        # Update energy plot
        E_kinetic, E_potential, E_total = self.simulator.calculate_energy(solution, params)

        self.kinetic_curve.setData(t, E_kinetic)
        self.potential_curve.setData(t, E_potential)
        self.total_curve.setData(t, E_total)

        # Update angular velocity plot
        self.omega1_curve.setData(t, solution[1, :])
        self.omega2_curve.setData(t, solution[3, :])
        self.omega3_curve.setData(t, solution[5, :])

        # Update progress bar
        self.progress_bar.setValue(int(100 * self.frame / len(self.simulator.t_eval)))

        self.frame += 1
