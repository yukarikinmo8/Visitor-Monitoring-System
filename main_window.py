import sys
import cv2
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow  # Import the generated UI class from main_ui.py
from video_processor import VideoProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Instantiate the UI class
        self.ui.setupUi(self)  # Set up the UI within the main window
        
        # Get the QLabel from the UI file, the camera feed will use the qlabel widget on qt designer as the place holder for the 
        #camera feed so the camera feed size will depend on the size of the qlabel
        self.label = self.ui.label  # Assuming you named your label 'label' in Qt Designer
        
        # Set up the camera feed, opencv will now open the camera feed
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Camera not accessible") #catching errrors if camera isn't available
            sys.exit()

# Run the application
if __name__ == "__main__":
      
    app = QApplication([])  # Create a QApplication instance
    window = MainWindow()  # Create the main window instance
    window.show()  # Show the main window
    app.exec()  # Start the event loop (this is necessary for the UI to be responsive)