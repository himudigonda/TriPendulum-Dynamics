import sys
from PySide6.QtWidgets import QApplication
from src.ui import PendulumSimulation

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PendulumSimulation()
    ex.show()
    sys.exit(app.exec())
