import numpy as np
from scipy.integrate import solve_ivp

class PendulumSimulator:
    def __init__(self):
        self.t_span = None
        self.t_eval = None
        self.solution = None

    def derivatives(self, t, state, m1, m2, m3, L1, L2, L3, b, g):
        theta1, omega1, theta2, omega2, theta3, omega3 = state

        # Constants for convenience
        c1, c2, c3 = np.cos(theta1), np.cos(theta2), np.cos(theta3)
        s1, s2, s3 = np.sin(theta1), np.sin(theta2), np.sin(theta3)

        # Mass matrix
        M = np.array([
            [(m1 + m2 + m3) * L1, (m2 + m3) * L1 * L2 * np.cos(theta1 - theta2), m3 * L1 * L3 * np.cos(theta1 - theta3)],
            [(m2 + m3) * L1 * L2 * np.cos(theta1 - theta2), (m2 + m3) * L2**2, m3 * L2 * L3 * np.cos(theta2 - theta3)],
            [m3 * L1 * L3 * np.cos(theta1 - theta3), m3 * L2 * L3 * np.cos(theta2 - theta3), m3 * L3**2]
        ])

        # Force vector
        F = np.array([
            -(m1 + m2 + m3) * g * L1 * s1 - b * omega1,
            -(m2 + m3) * g * L2 * s2 - b * omega2,
            -m3 * g * L3 * s3 - b * omega3
        ])

        # Coriolis terms
        C = np.array([
            (m2 + m3) * L1 * L2 * omega2**2 * np.sin(theta1 - theta2) + m3 * L1 * L3 * omega3**2 * np.sin(theta1 - theta3),
            -(m2 + m3) * L1 * L2 * omega1**2 * np.sin(theta1 - theta2) + m3 * L2 * L3 * omega3**2 * np.sin(theta2 - theta3),
            -m3 * L1 * L3 * omega1**2 * np.sin(theta1 - theta3) - m3 * L2 * L3 * omega2**2 * np.sin(theta2 - theta3)
        ])

        # Solve for angular accelerations
        alpha = np.linalg.solve(M, F + C)

        return [omega1, alpha[0], omega2, alpha[1], omega3, alpha[2]]

    def setup_simulation(self, params):
        y0 = [params['theta1'], 0, params['theta2'], 0, params['theta3'], 0]
        self.t_span = (0, params['sim_time'])
        self.t_eval = np.linspace(0, params['sim_time'], int(params['sim_time'] * 50))  # 50 fps

        self.solution = solve_ivp(
            self.derivatives, self.t_span, y0, t_eval=self.t_eval,
            args=(params['m1'], params['m2'], params['m3'], params['L1'], params['L2'], params['L3'], params['b'], params['g']),
            method='RK45', rtol=1e-8, atol=1e-8
        )

    def get_positions(self, state, params):
        theta1, _, theta2, _, theta3, _ = state
        x1 = params['L1'] * np.sin(theta1)
        y1 = -params['L1'] * np.cos(theta1)
        x2 = x1 + params['L2'] * np.sin(theta2)
        y2 = y1 - params['L2'] * np.cos(theta2)
        x3 = x2 + params['L3'] * np.sin(theta3)
        y3 = y2 - params['L3'] * np.cos(theta3)
        return x1, y1, x2, y2, x3, y3

    def calculate_energy(self, solution, params):
        m1, m2, m3 = params['m1'], params['m2'], params['m3']
        L1, L2, L3 = params['L1'], params['L2'], params['L3']
        g = params['g']

        E_kinetic = 0.5 * (m1 * (L1 * solution[1, :])**2 +
                           m2 * ((L1 * solution[1, :])**2 + (L2 * solution[3, :])**2) +
                           m3 * ((L1 * solution[1, :])**2 + (L2 * solution[3, :])**2 + (L3 * solution[5, :])**2))
        E_potential = g * (m1 * L1 * (1 - np.cos(solution[0, :])) +
                           m2 * (L1 * (1 - np.cos(solution[0, :])) + L2 * (1 - np.cos(solution[2, :]))) +
                           m3 * (L1 * (1 - np.cos(solution[0, :])) + L2 * (1 - np.cos(solution[2, :])) + L3 * (1 - np.cos(solution[4, :]))))
        E_total = E_kinetic + E_potential

        return E_kinetic, E_potential, E_total
