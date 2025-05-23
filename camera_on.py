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
import json

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
from configurations import loadConfig, save_config, filterMulti1, resDef
from datetime import date
from imageComparison_backend import start_timing, end_timing, create_representations_db, run_verification


class PopupWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.msm = MySqlManager()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

        self._initialize_ui()
        
        # Initialize lock for thread safety
        self.comparison_lock = threading.Lock()
        self.comparison_thread = None
        
        # Start face comparison in a separate thread
        self.start_face_comparison()

    def _initialize_ui(self):
        self.ui.id_lbl1.setText(f"ID: {PERSON_ID1}")
        self.ui.date_lbl1.setText(f"Date: {DATE1}")
        self.ui.time_lbl1.setText(f"Time: {TIME1}")
        self.show_face_crops(FILEPATH1, self.ui.orig_img)
        
        # Initialize second image with placeholder
        self.ui.id_lbl2.setText("ID: Processing...")
        self.ui.date_lbl2.setText("Date: Processing...")
        self.ui.time_lbl2.setText("Time: Processing...")

    def start_face_comparison(self):
        """Start the face comparison process in a background thread"""
        # Cancel any existing thread
        if self.comparison_thread and self.comparison_thread.is_alive():
            return
            
        # Create and start a new thread
        self.comparison_thread = threading.Thread(
            target=self.face_comparison,
            daemon=True  # This ensures the thread won't block application exit
        )
        self.comparison_thread.start()

    def face_comparison(self):
        """Run face comparison in background thread"""
        try:
            with self.comparison_lock:
                img_path = FILEPATH1
                exclude_path = img_path
                saved_path = os.path.join(self.PROJECT_DIR, 'SavedFaces', DATE1)
                
                # Process-intensive operations now run in background
                start_timing("total_representation_creation")
                representations_file = create_representations_db(saved_path)
                end_timing("total_representation_creation")

                start_timing("total_verification")
                result = run_verification(
                    img_path=img_path,
                    exclude_path=exclude_path,
                    db_path=saved_path,
                    representations_file=representations_file
                )
                end_timing("total_verification")

                print(f"Result: {result}")
                # Update UI in the main thread
                if result:
                    print(f"Matched Image: {result['matched_image']}")
                    print(f"Distance: {result['distance']}")
                    print(f"Verified: {result['verified']}")

                    FILEPATH2 = result['matched_image']

                    if FILEPATH2 is None:
                        print("No matching image found.")
                        # Use QTimer to safely update UI from background thread
                        QTimer.singleShot(0, self.update_ui_no_match())
                        return

                    extract_result = self.extract_filename_and_id(FILEPATH2)
                    data = self.msm.search_personID(extract_result['id'])

                    if data:
                        # Update UI in main thread with the results
                        QTimer.singleShot(0, self.update_ui_with_results(FILEPATH2, data))
                        # self.update_ui_with_results(FILEPATH2, data)
                else:
                    QTimer.singleShot(0, lambda: self.update_ui_no_match())
        except Exception as e:
            print(f"Error in face comparison: {e}")
            QTimer.singleShot(0, lambda: self.update_ui_error(str(e)))

    def update_ui_with_results(self, filepath, data):
        """Update UI with the matching results - called in main thread"""
        try:
            self.ui.id_lbl2.setText(f"ID: {data['person_id']}")
            self.ui.date_lbl2.setText(f"Date: {data['date']}")
            self.ui.time_lbl2.setText(f"Time: {data['time']}")
            self.show_face_crops(filepath, self.ui.similar_img)
        except Exception as e:
            print(f"Error updating UI with results: {e}")

    def update_ui_no_match(self):
        """Update UI when no match is found - called in main thread"""
        # QMessageBox.warning(self, "Warning", "No similar faces found in the database.")
        self.ui.id_lbl2.setText("ID: No similar faces found")
        self.ui.date_lbl2.setText("Date: No similar faces found")
        self.ui.time_lbl2.setText("Time: No similar faces found")
        
    def update_ui_error(self, error_msg):
        """Update UI when an error occurs - called in main thread"""
        # QMessageBox.critical(self, "Error", f"An error occurred during face comparison: {error_msg}")
        self.ui.id_lbl2.setText("ID: Error occurred")
        self.ui.date_lbl2.setText("Date: Error occurred")
        self.ui.time_lbl2.setText("Time: Error occurred")

    def extract_filename_and_id(self, filepath: str):
        if filepath is None:
            return {'id': None, 'filename': None}
        parts = filepath.split('\\')  # split by backslash
        filename_with_ext = parts[-1]  # last part is the filename
        uuid = filename_with_ext.split('.')[0]  # remove .jpg extension
        return {'id': uuid, 'filename': filename_with_ext}

    def show_face_crops(self, face_crops, name_label):
        # Check if face_crops is a file path (string) and load the image if needed
        if isinstance(face_crops, str):
            if os.path.exists(face_crops):
                face_crops = cv2.imread(face_crops)
            else:
                print(f"Error: File not found: {face_crops}")
                return
        
        # Now proceed with original logic using the image array
        face_resized = cv2.resize(face_crops, (name_label.width(), name_label.height()), interpolation=cv2.INTER_LINEAR)
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        face_height, face_width, face_channels = face_rgb.shape
        face_bytes_per_line = face_channels * face_width
        face_qimg = QImage(face_rgb.data, face_width, face_height, face_bytes_per_line, QImage.Format_RGB888)
        face_pixmap = QPixmap.fromImage(face_qimg)
        name_label.setPixmap(face_pixmap)
        
    def closeEvent(self, event):
        """Handle window close event properly"""
        # Wait for thread to finish if it's running
        if self.comparison_thread and self.comparison_thread.is_alive():
            self.comparison_thread.join(timeout=0.1)  # Give it a small timeout
        super().closeEvent(event)


class CameraFeedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.msm = MySqlManager()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize video writer and settings
        self.video_writer = None
        self.save_video = True
        self.x, self.y = loadConfig()

        # Default coordinates and file path
        self.coord_point = (filterMulti1(self.x), filterMulti1(self.y))
        # self.area1 = [(261, 434), (337, 428), (522, 516), (450, 537)]
        # self.area2 = [(154, 450), (246, 438), (406, 541), (292, 548)]
        # self.file_path = 'Sample Test File\\test_video.mp4'
        self.area1 = []
        self.area2 = []
        self.file_path = 0

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

    def _initialize_ui(self):
        """Set up UI elements and connect signals."""
        # Disable stop button initially
        self.ui.stop_btn.setEnabled(False)
        self.ui.x_txtbox.setText(f"{self.x}")
        self.ui.y_txtbox.setText(f"{self.y}")
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
        self.ui.saveConfig_btn.clicked.connect(lambda: self.saveConfigs())
        self.ui.def_btn.clicked.connect(lambda: self.restoreDefaults())
        self.ui.logs_tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.logs_tbl.customContextMenuRequested.connect(self.open_menu)
        
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
            QMessageBox.warning(self, "Warning", "Coordinates not set.")
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
                directory_name = os.path.join(project_dir, "SavedFaces", datetime.datetime.now().strftime('%Y-%m-%d'), f"{person_id}.jpg")

                # Call the database manager to check if person exists and update or insert
                updated = self.msm.upsertLogEntry(person_id, details['date'], details['time'], directory_name)
        except Exception as e:
            print(f"Error saving result to database: {e}")
            return

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
                height, width, _ = face_crop.shape
                face_crop = face_crop[:height // 2, :]  # Crop the face in half (left half)
                if isinstance(details['time'], datetime.datetime):
                    time_str = details['time'].strftime('%H-%M-%S')
                else:
                    time_str = details['time'].replace(':', '-')
                filename = os.path.join(directory_name, f"{person_id}.jpg")
                
                # Always write the file, whether it exists or not
                # This will overwrite existing files and create new ones as needed
                cv2.imwrite(filename, face_crop)
                    
                processed_person_ids.add(person_id)
            except Exception as e:
                print(f"Error saving face {person_id}: {e}")

    def show_face_crops(self, face_crops, name_label):
        # Check if face_crops is a file path (string) and load the image if needed
        if isinstance(face_crops, str):
            if os.path.exists(face_crops):
                face_crops = cv2.imread(face_crops)
            else:
                print(f"Error: File not found: {face_crops}")
                return
        
        # Now proceed with original logic using the image array
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
                h, w, _ = x1.shape
                x1 = x1[:h // 2, :]  # Display the top half of the image
                self.show_face_crops(x1, self.ui.cap_4)
                if len(temp) > 1:
                    y1 = pickle.loads(zlib.decompress(temp[1]))
                    h, w, _ = y1.shape
                    y1 = y1[:h // 2, :]  # Display the top half of the image
                    self.show_face_crops(y1, self.ui.cap_6)
                if len(temp) > 2:
                    z1 = pickle.loads(zlib.decompress(temp[2]))
                    h, w, _ = z1.shape
                    z1 = z1[:h // 2, :]  # Display the top half of the image
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
        """Generate or retrieve a UUID for a given person ID combined with the current date and time."""
        unique_key = f"{person_id}"
        if unique_key not in self.person_uuid_map:
            self.person_uuid_map[unique_key] = str(uuid.uuid4())
        return self.person_uuid_map[unique_key]
    
    def open_menu(self, position: QPoint):
        index = self.ui.logs_tbl.indexAt(position)        
        if index.isValid():
            # Get the row of the clicked cell
            row = index.row()
            
            # Map the index of column 3 in the same row from proxy to source
            proxy_index = self.ui.logs_tbl.model().index(row, 3)
            proxy_date = self.ui.logs_tbl.model().index(row, 1)
            proxy_time = self.ui.logs_tbl.model().index(row, 2)
            proxy_person = self.ui.logs_tbl.model().index(row, 0)


            source_index = self.ui.logs_tbl.model().mapToSource(proxy_index)
            source_date = self.ui.logs_tbl.model().mapToSource(proxy_date)
            source_time = self.ui.logs_tbl.model().mapToSource(proxy_time)
            source_person = self.ui.logs_tbl.model().mapToSource(proxy_person)

            # Retrieve the file path stored in Qt.UserRole
            file_path_1 = self.ui.logs_tbl.model().sourceModel().itemFromIndex(source_index).data(Qt.UserRole)
            date_1 = self.ui.logs_tbl.model().sourceModel().itemFromIndex(source_date).data(Qt.DisplayRole)
            time_1 = self.ui.logs_tbl.model().sourceModel().itemFromIndex(source_time).data(Qt.DisplayRole)
            person_id_1 = self.ui.logs_tbl.model().sourceModel().itemFromIndex(source_person).data(Qt.DisplayRole)
            print(f"File path for clicked row: {file_path_1}")

        # Create the menu
        menu = QMenu()
        
        imageSearch_action = QAction("Search for Similar Image", self)
                
        # Connect actions
        imageSearch_action.triggered.connect(lambda: self.show_popup())
        
        # Add actions to the menu
        menu.addAction(imageSearch_action)        
        
        # Show the menu
        menu.exec(self.ui.logs_tbl.viewport().mapToGlobal(position))
        
        global FILEPATH1
        global DATE1
        global PERSON_ID1
        global TIME1
        FILEPATH1 = file_path_1
        DATE1 = date_1
        TIME1 = time_1
        PERSON_ID1 = person_id_1

    def onTextChanged(self, text):       
        self.ui.logs_tbl.model().setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.ui.logs_tbl.model().setFilterKeyColumn(2)  # Column index to filter (e.g., 1 = "Date")
        self.ui.logs_tbl.model().setFilterFixedString(text)    
        
    def show_popup(self):
        # Asynchronously show the popup in the main thread
        QTimer.singleShot(0, self._show_popup_impl)

    def _show_popup_impl(self):
        self.popup = PopupWindow()
        self.popup.show()  # Display the popup widget (non-modal)
    
    def saveConfigs(self):

        x_value = int(self.ui.x_txtbox.text())  # Parse x as an integer
        y_value = int(self.ui.y_txtbox.text())  # Parse y as an integer
        save_config(x_value, y_value)
        self.x, self.y = loadConfig()
        self.coord_point = (filterMulti1(self.x), filterMulti1(self.y))

    def restoreDefaults(self):
        resDef()
        self.x, self.y = loadConfig()
        self.ui.x_txtbox.setText(f"{self.x}")
        self.ui.y_txtbox.setText(f"{self.y}")
        self.coord_point = (filterMulti1(self.x), filterMulti1(self.y))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    
    sys.exit(app.exec())