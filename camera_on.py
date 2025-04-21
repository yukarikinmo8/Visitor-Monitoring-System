import sys
import cv2
import cvzone
import datetime
import os
import pickle
import zlib
import threading
from queue import Queue

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QStandardItemModel, QStandardItem

from database_module import MySqlManager 
from counter_mod import Algorithm_Count
from set_entry import Get_Coordinates
from export_pdf import exportPDF
from main_ui import Ui_MainWindow  # Import the generated UI file

from datetime import date


class CameraFeedWindow(QMainWindow):
    def __init__(self):
        msm = MySqlManager()
        pdf = exportPDF()
        super().__init__()
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        self.ui.stop_btn.setEnabled(False)
        self.ui.dash_lbl.setVisible(False)
        self.ui.logo_lbl.setVisible(False)
        self.ui.setts_lbl.setVisible(False)
        self.ui.logs_lbl.setVisible(False)
        self.ui.lvf_lbl.setVisible(False)

        # TODO: access ui point for area
        self.coord_point = (0.5, 0.04) # default coordinates for the area of interest x=50% y=4%
        self.area1 = [(261, 434), (337, 428), (522, 516), (450, 537)] # coordinates for the area of interest
        self.area2 = [(154, 450), (246, 438), (406, 541), (292, 548)] # coordinates for the area of interest
        self.file_path = 'Sample Test File\\test_video.mp4' # path to the video file
        # self.file_path = 0 # for webcam feed
        self.frame_queue = Queue(maxsize=1)

        self.ui.stackedWidget.setCurrentIndex(0)
        # self.ui.cap_4.setPixmap(QPixmap())

        # Timer for updating frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
 
        # Connect the "On" button to start the feed
        self.ui.start_btn.clicked.connect(self.start_feed)
        self.ui.stop_btn.clicked.connect(self.stop_feed)
        self.ui.menu_btn.clicked.connect(self.navbar_toggle)
        self.ui.dash_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.cam_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.logs_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.settings_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(3))

        date_today = date.today()
        file_path_export = "Logs for " + date_today.strftime("%Y-%m-%d") + ".pdf"
        
        self.ui.logs_tbl.setAlternatingRowColors(True)
        msm.fillLogsTable(self.ui.logs_tbl);      
        self.ui.export_btn.clicked.connect(lambda: pdf.exportTableToPDF(self.ui.logs_tbl, file_path_export))

    def start_feed(self):
        self.running = False  # stop any previous loop
        while not self.frame_queue.empty():
            self.frame_queue.get()

        self.ui.cap_4.clear()
        self.ui.cap_5.clear()
        self.ui.cap_6.clear()

        self.a1 = self.area1
        self.a2 = self.area2
        area = Get_Coordinates(self.file_path, (self.ui.label.width(), self.ui.label.height()))
        self.a1 = area.get_coordinates(self.a1, self.a2, 1)
        self.a2 = area.get_coordinates(self.a2, self.a1, 2)

        if self.a1 and self.a2:
            self.running = True

            # 🔁 Re-create algorithm to reset memory
            self.algo = Algorithm_Count(self.file_path, self.a1, self.a2, (self.ui.label.width(), self.ui.label.height()), self.coord_point)
            self.frame_generator = self.algo.main()

            # Start fresh capture thread
            self.capture_thread = threading.Thread(target=self.capture_frames, daemon=True)
            self.capture_thread.start()

            self.timer.start(30)
            self.ui.start_btn.setEnabled(False)
            self.ui.stop_btn.setEnabled(True)
        else:
            print("Coordinates not set.")
        return

    def capture_frames(self):
        try:
            while self.running:
                frame_data = next(self.frame_generator)
                if self.frame_queue.full():
                    self.frame_queue.get()
                self.frame_queue.put(frame_data)
        except StopIteration:
            pass

    def update_frame(self):
        if not self.frame_queue.empty():
            frame, result = self.frame_queue.get()
            self.last_result = result  # Save for use in other functions
            self.show_face_crops(frame, self.ui.label)
            self.update_cap(result)
            self.save_crop_faces(result)

    def stop_feed(self):
        self.running = False
        self.timer.stop()

        while not self.frame_queue.empty():
            self.frame_queue.get()

        self.ui.label.setPixmap(QPixmap())
        self.ui.cap_4.setPixmap(QPixmap())
        self.ui.cap_5.setPixmap(QPixmap())
        self.ui.cap_6.setPixmap(QPixmap())

        self.ui.start_btn.setEnabled(True)
        self.ui.stop_btn.setEnabled(False)

    def save_crop_faces(self, result):
        processed_person_ids = set()
        
        # Use the current project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        directory_name = os.path.join(project_dir, "SavedFaces", datetime.datetime.now().strftime('%Y-%m-%d'))

        if not os.path.exists(directory_name):
            try:
                os.makedirs(directory_name)
            except Exception as e:
                print(f"Failed to create directory: {e}")
                return

        for person_id, details in result['entering_details'].items():
            if person_id in processed_person_ids:
                continue
            try:
                face_crop = pickle.loads(zlib.decompress(details['face_crops']))
                if isinstance(details['time'], datetime.datetime):
                    time_str = details['time'].strftime('%H-%M-%S')
                else:
                    time_str = details['time'].replace(':', '-')
                filename = os.path.join(directory_name, f"{person_id}-face_{time_str}.jpg")
                cv2.imwrite(filename, face_crop)
                processed_person_ids.add(person_id)
            except Exception as e:
                print(f"Error saving face {person_id}: {e}")


    def show_face_crops(self, face_crops, name_label):
        face_resized = cv2.resize(face_crops, (name_label.width(), name_label.height()), interpolation=cv2.INTER_LINEAR)
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        face_height, face_width, face_channels = face_rgb.shape
        face_bytes_per_line = face_channels * face_width
        face_qimg = QImage(face_rgb.data, face_width, face_height, face_bytes_per_line, QImage.Format_RGB888)
        face_pixmap = QPixmap.fromImage(face_qimg)
        name_label.setPixmap(face_pixmap)

    def update_cap(self, result):
        temp = []
        for person_id, details in result['entering_details'].items():
            temp.insert(0, details['face_crops'])

        if temp:
            try:
                x1 = pickle.loads(zlib.decompress(temp[0]))
                self.show_face_crops(x1, self.ui.cap_4)
                if len(temp) > 1:
                    y1 = pickle.loads(zlib.decompress(temp[1]))
                    self.show_face_crops(y1, self.ui.cap_6)
                if len(temp) > 2:
                    z1 = pickle.loads(zlib.decompress(temp[2]))
                    self.show_face_crops(z1, self.ui.cap_5)
            except Exception as e:
                print(f"Error showing face crops: {e}")

    def closeEvent(self, event):
        self.timer.stop()
        # if hasattr(self, 'capture') and self.capture.isOpened():
        #     self.capture.release()
        event.accept()
    
    def navbar_toggle(self):
  
        if self.ui.nav_bar.width() == 111:
            self.animation = QPropertyAnimation(self.ui.nav_bar, b"minimumWidth")
            self.animation.setDuration(200)  # Animation duration (300ms)
            self.animation.setStartValue(self.ui.nav_bar.width())  # Start from current width
            self.animation.setEndValue(401)  # Expand or Collapse
            self.animation.start()

            self.animation.finished.connect(lambda: self.ui.nav_bar.setFixedWidth(401))

            self.ui.menu_btn.setGeometry(340, 20, 50, 50)
            self.ui.dash_lbl.setVisible(True)
            self.ui.logo_lbl.setVisible(True)
            self.ui.setts_lbl.setVisible(True)
            self.ui.logs_lbl.setVisible(True)
            self.ui.lvf_lbl.setVisible(True)

        else: 

            self.clearUiMem()

            self.ui.nav_bar.setMinimumWidth(111)
            self.animation = QPropertyAnimation(self.ui.nav_bar, b"maximumWidth")
            self.animation.setDuration(200)  # Animation duration (300ms)
            self.animation.setStartValue(self.ui.nav_bar.width())  # Start from current width
            self.animation.setEndValue(111)  # Expand or Collapse
            self.animation.start()
            self.ui.nav_bar.update()
            self.ui.nav_bar.repaint()
            self.animation.finished.connect(lambda: self.ui.nav_bar.setFixedWidth(111))      
            self.animation.finished.connect(lambda: self.update_ui()) 
        
    def update_ui(self):
        self.ui.menu_btn.setGeometry(30, 20, 50, 50)
        self.ui.dash_lbl.setVisible(False)
        self.ui.logo_lbl.setVisible(False)
        self.ui.setts_lbl.setVisible(False)
        self.ui.logs_lbl.setVisible(False)
        self.ui.lvf_lbl.setVisible(False)
    
    def clearUiMem(self):
        if hasattr(self, "animation"):
            if self.animation.state() == QPropertyAnimation.Running:
                self.animation.stop()
            self.animation.deleteLater()  # Mark for memory cleanup
            self.animation = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    
    sys.exit(app.exec())