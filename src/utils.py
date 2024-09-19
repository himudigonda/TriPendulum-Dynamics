from PySide6.QtGui import QPalette, QColor, QLinearGradient, QBrush

def create_dark_palette():
    palette = QPalette()
    gradient = QLinearGradient(0, 0, 1, 1)
    gradient.setCoordinateMode(QLinearGradient.StretchToDeviceMode)
    gradient.setColorAt(0, QColor(20, 20, 20))
    gradient.setColorAt(1, QColor(45, 45, 45))
    brush = QBrush(gradient)

    palette.setBrush(QPalette.Window, brush)
    palette.setBrush(QPalette.Base, brush)
    palette.setBrush(QPalette.Text, QColor(220, 220, 220))
    return palette
