import sys
import cv2
import cvzone

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow  # Import the generated UI file
from counter_mod import Algorithm_Count


class CameraFeedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stop_btn.setEnabled(False)

        self.file_path = 'Sample Test File\\test_video.mp4'

        self.area1 = [(300, 300), (400, 559), (667, 675), (632, 681)]
        self.area2 = [(220, 200), (313, 566), (579, 703), (624, 694)]

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
        self.frame_generator = self.algo.main()  # Initialize the generator
        self.timer.start(10)  # Start the timer to update frames every 30ms
        
        self.ui.start_btn.setEnabled(False)  # Disable the "On" button while the feed is running
        self.ui.stop_btn.setEnabled(True)

    def stop_feed(self):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
        self.ui.label.setPixmap(QPixmap())
        self.timer.stop()
        self.ui.start_btn.setEnabled(True)
        self.ui.stop_btn.setEnabled(False)
        # self.capture.release()
        # self.ui.label.setPixmap(QPixmap())
        # self.timer.stop()
        # self.ui.start_btn.setEnabled(True)
        # self.ui.stop_btn.setEnabled(False)

    def update_frame(self):
        try:
            frame, result = next(self.frame_generator)  # Get the next frame from the generator
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            qimg = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.ui.label.setPixmap(pixmap)
            self.update_cap()
            print(result)


        except StopIteration:
            self.timer.stop()  # Stop the timer when frames are done
            self.ui.start_btn.setEnabled(True)
            self.ui.stop_btn.setEnabled(False)

    def update_cap(self):
        # Initialize the video capture only once
        if not hasattr(self, 'capture') or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(self.file_path)

        # Read the first frame (or capture the frame at a specific moment)
        ret, frame = self.capture.read()

        if ret:
            # Resize the frame for each QLabel
            label_width1 = self.ui.cap_1.width()
            label_height1 = self.ui.cap_1.height()

            label_width2 = self.ui.cap_2.width()
            label_height2 = self.ui.cap_2.height()

            label_width3 = self.ui.cap_3.width()
            label_height3 = self.ui.cap_3.height()

            # Resize the frame to fit each label
            frame_resized1 = cv2.resize(frame, (label_width1, label_height1), interpolation=cv2.INTER_LINEAR)
            frame_resized2 = cv2.resize(frame, (label_width2, label_height2), interpolation=cv2.INTER_LINEAR)
            frame_resized3 = cv2.resize(frame, (label_width3, label_height3), interpolation=cv2.INTER_LINEAR)

            # Convert the frame from BGR (OpenCV default) to RGB (for QImage compatibility)
            frame_rgb1 = cv2.cvtColor(frame_resized1, cv2.COLOR_BGR2RGB)
            frame_rgb2 = cv2.cvtColor(frame_resized2, cv2.COLOR_BGR2RGB)
            frame_rgb3 = cv2.cvtColor(frame_resized3, cv2.COLOR_BGR2RGB)

            # Get the dimensions of the resized frame and create QImage for each resized frame
            height1, width1, channels1 = frame_rgb1.shape
            bytes_per_line1 = channels1 * width1
            qimg1 = QImage(frame_rgb1.data, width1, height1, bytes_per_line1, QImage.Format_RGB888)

            height2, width2, channels2 = frame_rgb2.shape
            bytes_per_line2 = channels2 * width2
            qimg2 = QImage(frame_rgb2.data, width2, height2, bytes_per_line2, QImage.Format_RGB888)

            height3, width3, channels3 = frame_rgb3.shape
            bytes_per_line3 = channels3 * width3
            qimg3 = QImage(frame_rgb3.data, width3, height3, bytes_per_line3, QImage.Format_RGB888)

            # Convert the QImage to QPixmap and update the QLabel widgets
            pixmap1 = QPixmap.fromImage(qimg1)
            pixmap2 = QPixmap.fromImage(qimg2)
            pixmap3 = QPixmap.fromImage(qimg3)

            # Set pixmap for each QLabel
            self.ui.cap_1.setPixmap(pixmap1)
            self.ui.cap_2.setPixmap(pixmap2)
            self.ui.cap_3.setPixmap(pixmap3)

    def closeEvent(self, event):
        """Release the video capture when the window is closed."""
        self.capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    sys.exit(app.exec())