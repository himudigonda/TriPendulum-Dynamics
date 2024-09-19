import sys
from PySide6.QtWidgets import QApplication
from src.ui import PendulumSimulation

def main():
    """
    Entry point for the Pendulum Simulation application.

    This function initializes the QApplication, creates an instance of the
    PendulumSimulation class, displays the main window, and starts the
    application's event loop.
    """
    app = QApplication(sys.argv)
    ex = PendulumSimulation()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
