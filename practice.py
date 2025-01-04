import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow  # Import the generated UI

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set transparency attributes after UI setup
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the window background transparent
        self.setWindowFlag(Qt.FramelessWindowHint)     # Optional: Remove window borders and title bar
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)  # Ensure the paint event is not opaque

        # Optional: Set a minimum size for the window
        self.setMinimumSize(400, 300)

    def paintEvent(self, event):
        # This method ensures the background is filled with transparency
        painter = QPainter(self)
        painter.setOpacity(100)  # Adjust opacity for content if needed (optional)
        painter.fillRect(self.rect(), Qt.transparent)  # Fill the window with a transparent background
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Create and show the transparent window
    window = TransparentWindow()
    window.show()

    sys.exit(app.exec())