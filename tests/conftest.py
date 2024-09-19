import pytest
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()
