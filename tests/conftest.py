import pytest
from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def app():
    """
    Fixture to provide a QApplication instance for the test session.

    This fixture ensures that a single QApplication instance is created and
    shared across all tests in the session. If an instance already exists,
    it reuses that instance. The QApplication instance is properly cleaned
    up after the tests are completed.

    Yields:
        QApplication: An instance of the QApplication.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()
