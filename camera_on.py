import sys
import cv2
import cvzone
import datetime
import os
import pickle
import zlib
import torch

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from main_ui import Ui_MainWindow  # Import the generated UI file
from counter_mod import Algorithm_Count
from set_entry import Get_Coordinates
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from database_module import MySqlManager 
from datetime import date

from export_pdf import exportPDF

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
        self.file_path = 'Sample Test File\\test_video.mp4'
        self.ui.stackedWidget.setCurrentIndex(0)
        # self.area1 = [(300, 300), (400, 559), (667, 675), (632, 681)]
        # self.area2 = [(110, 400), (313, 566), (579, 703), (624, 694)]
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
        filepathexport = "Logs for " + date_today.strftime("%Y-%m-%d") + ".pdf"
        
        self.ui.logs_tbl.setAlternatingRowColors(True)
        msm.fillLogsTable(self.ui.logs_tbl);      
        self.ui.export_btn.clicked.connect(lambda: pdf.exportTableToPDF(self.ui.logs_tbl, filepathexport))

    def start_feed(self):
        self.capture = cv2.VideoCapture(self.file_path)
        self.a1 =  None
        self.a2 =  None
        area = Get_Coordinates(self.file_path, (self.ui.label.width(), self.ui.label.height()))
        self.a1 = area.get_coordinates(self.a1, self.a2, 1)
        self.a2 = area.get_coordinates(self.a2, self.a1, 2)
        
        if self.a1 and self.a2:
            # Initialize the video capture and algorithm
            self.algo = Algorithm_Count(self.file_path, self.a1, self.a2, (self.ui.label.width(), self.ui.label.height()))
            self.frame_generator = self.algo.main()  # Initialize the generator
            self.timer.start(10)  # Start the timer to update frames every 30ms        
            self.ui.start_btn.setEnabled(False)  # Disable the "On" button while the feed is running
            self.ui.stop_btn.setEnabled(True)
        else:
            print("walang laman ang coordinates")
            return


    def stop_feed(self):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
        self.ui.label.setPixmap(QPixmap())
        self.ui.cap_4.setPixmap(QPixmap())
        self.ui.cap_5.setPixmap(QPixmap())
        self.ui.cap_6.setPixmap(QPixmap())
        self.timer.stop()
        self.ui.start_btn.setEnabled(True)
        self.ui.stop_btn.setEnabled(False)

    def update_frame(self):
        try:
            frame, result = next(self.frame_generator)  # Get the next frame from the generator
            self.show_face_crops(frame, self.ui.label)
            self.update_cap()

            self.save_crop_faces()      

        except StopIteration:
            self.timer.stop()  # Stop the timer when frames are done
            self.ui.start_btn.setEnabled(True)
            self.ui.stop_btn.setEnabled(False)

    def save_crop_faces(self):
        processed_person_ids = set()  # To track already saved person IDs

        try:
            frame, result = next(self.frame_generator)  # Get the next frame from the generator
            
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            directory_name = os.path.join(downloads_path, datetime.datetime.now().strftime('%Y-%m-%d'))
            
            # Ensure the directory exists
            if not os.path.exists(directory_name):
                try:
                    os.makedirs(directory_name)
                    print(f"Directory '{directory_name}' created.")
                except PermissionError:
                    print(f"Permission denied: Unable to create '{directory_name}'.")
                    return
                except Exception as e:
                    print(f"An unexpected error occurred while creating directory '{directory_name}': {e}")
                    return
            
            for person_id, details in result['entering_details'].items():
                # Check if the face crop for this person has already been saved
                if person_id in processed_person_ids:
                    print(f"Skipping already processed Person ID: {person_id}")
                    continue
                
                print(f"Processing Person ID: {person_id}, entered at {details['time']}")
                try:
                    face_crop = pickle.loads(zlib.decompress(details['face_crops']))
                    
                    # Save the face crop to the directory
                    filename = os.path.join(directory_name, f"face_{details['time'].strftime('%H-%M-%S')}.jpg")
                    cv2.imwrite(filename, face_crop)
                    print(f"Saved face crop to {filename}")
                    
                    # Mark this person_id as processed
                    processed_person_ids.add(person_id)
                except Exception as e:
                    print(f"An error occurred while processing Person ID {person_id}: {e}")
        
        except StopIteration:
            print("No more frames to process.")


    def show_face_crops(self, face_crops, name_label):
        face_resized = cv2.resize(face_crops, (name_label.width(), name_label.height()), interpolation=cv2.INTER_LINEAR)
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        face_height, face_width, face_channels = face_rgb.shape
        face_bytes_per_line = face_channels * face_width
        face_qimg = QImage(face_rgb.data, face_width, face_height, face_bytes_per_line, QImage.Format_RGB888)
        face_pixmap = QPixmap.fromImage(face_qimg)
        name_label.setPixmap(face_pixmap)

    def update_cap(self):
        """
        Update the camera feed with the latest frame and display face crops.
        This method retrieves the next frame from the frame generator and processes
        the face crops detected in the frame. It displays up to three face crops in
        the UI.
        Raises:
            StopIteration: If the frame generator has no more frames to provide.
        How it works:
        1. Retrieves the next frame and result from the frame generator.
        2. Initializes an empty list to store face crops.
        3. Iterates over the detected persons and their details, printing the person ID and entry time.
        4. Inserts the face crops into the list.
        5. If there are face crops, decompresses and displays up to three face crops in the UI.
        """
        try:
            frame, result = next(self.frame_generator)  # Get the next frame from the generator

            # print(result)
            temp = []
        
            # Access face crops from the result
            for person_id, details in result['entering_details'].items():
                print(f"Person ID: {person_id}, entered at {details['time']}")
                temp.insert(0, details['face_crops'])

            if temp:
                x = temp[0] # Get the face crop
                x1 = pickle.loads(zlib.decompress(x)) # Decompress the face crop
                self.show_face_crops(x1, self.ui.cap_4) # Display the face crop in the QLabel
                if len(temp) > 1:
                    y = temp[1]
                    y1 = pickle.loads(zlib.decompress(y))
                    self.show_face_crops(y1, self.ui.cap_6)
                if len(temp) > 2:
                    z = temp[2]
                    z1 = pickle.loads(zlib.decompress(z))
                    self.show_face_crops(z1, self.ui.cap_5)
        except StopIteration:
            pass

    def closeEvent(self, event):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
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