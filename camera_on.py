import sys
import cv2
import cvzone
import datetime
import os
import pickle
import zlib
import threading
from queue import Queue
import shutil
import uuid

from PySide6.QtCore import QTimer, QPoint
from PySide6.QtGui import QImage, QPixmap, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,  QWidget, QMenu, QMessageBox
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QFileDialog

from database_module import MySqlManager 
from counter_mod import Algorithm_Count
from set_entry import Get_Coordinates
from export_pdf import exportPDF
from main_ui import Ui_MainWindow  # Import the generated UI file
from ui_image_comparison import Ui_Form

from datetime import date

class PopupWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 

class CameraFeedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.msm = MySqlManager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize video writer and settings
        self.video_writer = None
        self.save_video = True

        # Default coordinates and file path
        self.coord_point = (0.5, 0.04)
        self.area1 = [(261, 434), (337, 428), (522, 516), (450, 537)]
        self.area2 = [(154, 450), (246, 438), (406, 541), (292, 548)]
        self.file_path = 'Sample Test File\\test_video.mp4'

        # Frame queue for processing
        self.frame_queue = Queue(maxsize=1)

        # Timer for updating frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Initialize UI elements
        self._initialize_ui()

        # Initialize database and export functionality
        self._initialize_database_and_export()

        self.person_uuid_map = {}
        self.ui.logs_tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.logs_tbl.customContextMenuRequested.connect(self.open_menu)

    def _initialize_ui(self):
        """Set up UI elements and connect signals."""
        # Disable stop button initially
        self.ui.stop_btn.setEnabled(False)

        # Hide navigation labels
        self.ui.logo_lbl.setVisible(False)        
        self.ui.search_txt.textChanged.connect(self.onTextChanged)
        # Set default stacked widget page
        self.ui.stackedWidget.setCurrentIndex(0)

        # Connect button signals
        self.ui.start_btn.clicked.connect(self.start_feed)
        self.ui.stop_btn.clicked.connect(self.stop_feed)
        self.ui.menu_btn.clicked.connect(self.navbar_toggle)
        self.ui.dash_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.cam_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.logs_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.settings_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.export_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))

    def _initialize_database_and_export(self):       
        pdf = exportPDF()
        date_today = date.today()   
     
        self.msm.updateDashboardStats(
            date_labels=[
                self.ui.dateLabel1, self.ui.dateLabel2,
                self.ui.dateLabel3, self.ui.dateLabel4
            ],
            count_labels=[
                self.ui.totalEntry1, self.ui.totalEntry2,
                self.ui.totalEntry3, self.ui.totalEntry4
            ]
        )
        self.ui.logs_tbl.setAlternatingRowColors(True)
        self.ui.export_tbl.setAlternatingRowColors(True)
        self.ui.logsPrev_tbl.setAlternatingRowColors(True)
        self.msm.fillLogsTable(self.ui.logs_tbl)
        self.msm.fillLogsTable(self.ui.logsPrev_tbl) #for testing
        self.msm.fillComboBox(self.ui.dateFilter_cbx)
        self.onDateChanged(self.ui.dateFilter_cbx.currentText())  
        self.ui.dateFilter_cbx.currentTextChanged.connect(self.onDateChanged)    
        self.ui.export_btn2.clicked.connect(
            lambda: pdf.exportTableToPDF(
                self.ui.export_tbl, "Logs for " + self.ui.dateFilter_cbx.currentText() + ".pdf"
            )
        ) 
        self.ui.stackedWidget.currentChanged.connect(self.onPageChanged)

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

            if self.save_video:
                output_dir = "recordings"
                os.makedirs(output_dir, exist_ok=True)
                # Create a folder with the current month and year
                current_date = datetime.datetime.now()
                month_year_folder = os.path.join(output_dir, current_date.strftime('%Y-%m'))
                os.makedirs(month_year_folder, exist_ok=True)

                # Set the filename to the current date
                filename = f"{current_date.strftime('%Y-%m-%d')}.avi"
                self.temp_video_path = os.path.join(month_year_folder, filename)
                self.temp_video_path = os.path.join(output_dir, filename)

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                size = (self.ui.label.width(), self.ui.label.height())
                self.video_writer = cv2.VideoWriter(self.temp_video_path, fourcc, 24.0, size)

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

            uuid_result = {'entering_details': {}} # Initialize with empty dictionary
            for person_id, details in result['entering_details'].items(): # Iterate through each person_id and details
                uid = self.get_uuid_for_person(person_id) 
                uuid_result['entering_details'][uid] = details # Store details with UUID as key

            self.last_result = uuid_result
            self.show_face_crops(frame, self.ui.label)
            self.update_cap(uuid_result)
            self.save_crop_faces(uuid_result)
            self.save_result_to_database(uuid_result)
            
            if self.save_video and self.video_writer is not None:
                self.video_writer.write(frame)

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

        if self.save_video and self.video_writer:
            self.video_writer.release()
            self.video_writer = None

            # Show save dialog
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            default_filename = f"processed_video_{current_date}.avi"
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Processed Video", 
                default_filename, 
                "AVI Files (*.avi);;All Files (*)"
            )

            if file_path:
                # Move temp file to selected location
                try:
                    shutil.move(self.temp_video_path, file_path)  # Use shutil.move instead of os.rename
                    print(f"Video saved to: {file_path}")
                except Exception as e:
                    print(f"Error saving video: {e}")
            else:
                # User canceled - delete temp file
                if os.path.exists(self.temp_video_path):
                    os.remove(self.temp_video_path)

    def save_result_to_database(self, result):
        """Save the result data to the database."""
        try:
            for person_id, details in result['entering_details'].items():
                # Example data to save
                face_crop = zlib.compress(pickle.dumps(details['face_crops']))
                timestamp = details['time'].replace(':', '-')
                project_dir = os.path.dirname(os.path.abspath(__file__))
                directory_name = os.path.join(project_dir, "SavedFaces", datetime.datetime.now().strftime('%Y-%m-%d'), f"{person_id}-face_{timestamp}.jpg")

                # Call the database manager to save the data
                self.msm.insertLogEntries(person_id, details['date'], details['time'], directory_name)


        except Exception as e:
            print(f"Error saving result to database: {e}")

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
        """""Update the UI with the face crops."""
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

            self.animation.finished.connect(lambda: self.ui.nav_bar.setFixedWidth(300))

            self.ui.menu_btn.setGeometry(250, 0, 50, 50)
            self.ui.dash_btn.setFixedWidth(300)
            self.ui.dash_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.cam_btn.setFixedWidth(300)
            self.ui.cam_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.logs_btn.setFixedWidth(300)
            self.ui.logs_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.settings_btn.setFixedWidth(300)
            self.ui.settings_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.logo_lbl.setVisible(True)

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
        self.ui.menu_btn.setGeometry(0, 0, 111, 51)
        self.ui.dash_btn.setFixedWidth(111)
        self.ui.cam_btn.setFixedWidth(111)
        self.ui.logs_btn.setFixedWidth(111)
        self.ui.settings_btn.setFixedWidth(111)
        self.ui.cam_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.logs_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.settings_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.dash_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.ui.logo_lbl.setVisible(True)
        self.ui.logo_lbl.setVisible(False)
    
    def clearUiMem(self):
        if hasattr(self, "animation"):
            if self.animation.state() == QPropertyAnimation.Running:
                self.animation.stop()
            self.animation.deleteLater()  # Mark for memory cleanup
            self.animation = None

    def onDateChanged(self, selected_date):
        self.msm.fillExportTable(selected_date, self.ui.export_tbl)

    def onPageChanged(self, index):
        if index == 2:  # for example, index 2 is your logs page
            self.msm.fillLogsTable(self.ui.logs_tbl)
            self.msm.fillComboBox(self.ui.dateFilter_cbx)

            # Optionally, refresh filtered table too
            selected_date = self.ui.dateFilter_cbx.currentText()
            self.onDateChanged(selected_date)
        
    def get_uuid_for_person(self, person_id):
        """"Generate or retrieve a UUID for a given person ID."""
        if person_id not in self.person_uuid_map:
            self.person_uuid_map[person_id] = str(uuid.uuid4())
        return self.person_uuid_map[person_id]
    
    def open_menu(self, position: QPoint):
        index = self.ui.logs_tbl.indexAt(position)        
        if index.isValid():
            # Get the row of the clicked cell
            row = index.row()

            # Map the index of column 3 in the same row from proxy to source
            proxy_index = self.ui.logs_tbl.model().index(row, 3)
            source_index = self.ui.logs_tbl.model().mapToSource(proxy_index)

            # Retrieve the file path stored in Qt.UserRole
            file_path = self.ui.logs_tbl.model().sourceModel().itemFromIndex(source_index).data(Qt.UserRole)

            print(f"File path for clicked row: {file_path}")

        # Create the menu
        menu = QMenu()
        
        imageSearch_action = QAction("Search for Similar Image", self)
                
        # Connect actions
        imageSearch_action.triggered.connect(lambda: self.show_popup())
        
        # Add actions to the menu
        menu.addAction(imageSearch_action)        
        
        # Show the menu
        menu.exec(self.ui.logs_tbl.viewport().mapToGlobal(position))
        
        return file_path

    def onTextChanged(self, text):       
        self.ui.logs_tbl.model().setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.ui.logs_tbl.model().setFilterKeyColumn(2)  # Column index to filter (e.g., 1 = "Date")
        self.ui.logs_tbl.model().setFilterFixedString(text)    
        
    def show_popup(self):
        # Create an instance of the PopupWindow and show it
        self.popup = PopupWindow()
        self.popup.show()  # Display the popup widget (non-modal)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    
    sys.exit(app.exec())