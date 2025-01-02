import sys
import cv2
import cvzone_module

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

        self.file_path = 'Sample Test File\\test_video.mp4'
        self.area1 = [(359, 559), (400, 559), (667, 675), (632, 681)]
        self.area2 = [(346, 563), (313, 566), (579, 703), (624, 694)]

        # Initialize the camera (use 0 for default camera, or replace with other index if you have multiple cameras)
        self.capture = cv2.VideoCapture(self.file_path)

        # Timer to update the QLabel with frames from the camera feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30ms

        
    def update_frame(self):
        # Read a frame from the camera
        ret, frame = self.capture.read()
        self.frame_width = 1280
        self.frame_height = int(self.frame_width / 16 * 9)   
        self.algo = Algorithm_Count(self.file_path,self.area1, self.area2, (self.frame_width, self.frame_height))

        
        if ret:
            # Convert the frame from BGR to RGB
            
            frame_resized = cv2.resize(frame, (self.ui.label.width(), self.ui.label.height()))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            detections_person, detections_face = self.algo.detect_BboxOnly(frame_resized)
            self.algo.counter(frame_resized, detections_person, detections_face)
            
            # Convert the frame to QImage
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            qimg = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # Convert QImage to QPixmap and set it to QLabel
            pixmap = QPixmap.fromImage(qimg)
            self.ui.label.setPixmap(pixmap)

    def closeEvent(self, event):
        # Release the camera when the window is closed
        self.capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    sys.exit(app.exec())