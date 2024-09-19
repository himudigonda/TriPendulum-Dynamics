from PySide6.QtGui import QPalette, QColor, QLinearGradient, QBrush

def create_dark_palette():
    """
    Create a dark color palette for the application.

    This function creates a QPalette object with a dark gradient background
    and light text color. The gradient transitions from a dark gray to a
    slightly lighter gray.

    Returns:
        QPalette: A QPalette object configured with the dark theme.
    """
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
