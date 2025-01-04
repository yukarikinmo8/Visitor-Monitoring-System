import sys
import cv2
import cvzone

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow  # Import the generated UI file
from counter import Algorithm_Count

class CameraFeedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stop_btn.setEnabled(False)

        self.file_path = 'Sample Test File\\test_video.mp4'

        self.area1 = [(359, 559), (400, 559), (667, 675), (632, 681)]

        self.area2 = [(346, 563), (313, 566), (579, 703), (624, 694)]

        # Initialize the video capture and algorithm
        
        

        # Timer for updating frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Connect the "On" button to start the feed
        self.ui.start_btn.clicked.connect(self.start_feed)
        self.ui.stop_btn.clicked.connect(self.stop_feed)

    def start_feed(self):
        self.capture = cv2.VideoCapture(self.file_path)
        self.algo = Algorithm_Count(self.file_path, self.area1, self.area2, (self.ui.label.width(), self.ui.label.height()))
        self.timer.start(10)  # Start the timer to update frames every 30ms
        self.ui.start_btn.setEnabled(False)  # Disable the "On" button while the feed is running
        self.ui.stop_btn.setEnabled(True)

    def stop_feed(self):
        self.capture.release()
        self.ui.label.setPixmap(QPixmap())
        self.timer.stop()
        self.ui.start_btn.setEnabled(True)

    def update_frame(self):
        
        ret, frame = self.capture.read()
        # self.frame_width = 1280
        # self.frame_height = int(self.frame_width / 16 * 9)   
        self.algo = Algorithm_Count(self.file_path, self.area1, self.area2, (self.ui.label.width(), self.ui.label.height()))

        
        if ret:
            # Resize the frame to match the QLabel size
            frame = cv2.resize(frame, (self.ui.label.width(), self.ui.label.height()))

            # Perform detection with the algorithm
            # detections_person, detections_face = self.algo.detect_BboxOnly(frame)
            # self.algo.counter(frame, detections_person, detections_face)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to QImage
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            qimg = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # Convert QImage to QPixmap and set it to QLabel
            pixmap = QPixmap.fromImage(qimg)
            self.ui.label.setPixmap(pixmap)

    def closeEvent(self, event):
        """Release the video capture when the window is closed."""
        self.capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    sys.exit(app.exec())