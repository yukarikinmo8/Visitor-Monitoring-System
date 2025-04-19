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
from PySide6.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow
from counter_mod import Algorithm_Count
from set_entry import Get_Coordinates


class CameraFeedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stop_btn.setEnabled(False)

        # self.file_path = 'Sample Test File\\test_video.mp4'
        self.file_path = 0
        self.frame_queue = Queue(maxsize=1)

        self.ui.start_btn.clicked.connect(self.start_feed)
        self.ui.stop_btn.clicked.connect(self.stop_feed)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def start_feed(self):
        self.running = False  # stop any previous loop
        while not self.frame_queue.empty():
            self.frame_queue.get()

        self.ui.cap_1.clear()
        self.ui.cap_2.clear()
        self.ui.cap_3.clear()

        self.a1 = None
        self.a2 = None
        area = Get_Coordinates(self.file_path, (self.ui.label.width(), self.ui.label.height()))
        self.a1 = area.get_coordinates(self.a1, self.a2, 1)
        self.a2 = area.get_coordinates(self.a2, self.a1, 2)

        if self.a1 and self.a2:
            self.running = True

            # 🔁 Re-create algorithm to reset memory
            self.algo = Algorithm_Count(self.file_path, self.a1, self.a2, (self.ui.label.width(), self.ui.label.height()))
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
        self.ui.cap_1.setPixmap(QPixmap())
        self.ui.cap_2.setPixmap(QPixmap())
        self.ui.cap_3.setPixmap(QPixmap())

        self.ui.start_btn.setEnabled(True)
        self.ui.stop_btn.setEnabled(False)

    def save_crop_faces(self, result):
        processed_person_ids = set()
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        directory_name = os.path.join(downloads_path, datetime.datetime.now().strftime('%Y-%m-%d'))

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
                
                # Ensure 'details['time']' is a datetime object
                if isinstance(details['time'], str):
                    details['time'] = datetime.datetime.fromisoformat(details['time'])
                filename = os.path.join(directory_name, f"face_{details['time'].strftime('%H-%M-%S')}.jpg")
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
                self.show_face_crops(x1, self.ui.cap_1)
                if len(temp) > 1:
                    y1 = pickle.loads(zlib.decompress(temp[1]))
                    self.show_face_crops(y1, self.ui.cap_2)
                if len(temp) > 2:
                    z1 = pickle.loads(zlib.decompress(temp[2]))
                    self.show_face_crops(z1, self.ui.cap_3)
            except Exception as e:
                print(f"Error showing face crops: {e}")

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeedWindow()
    window.show()
    sys.exit(app.exec())
