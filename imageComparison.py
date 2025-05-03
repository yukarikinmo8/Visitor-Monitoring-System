from PySide6.QtWidgets import QApplication, QFileDialog, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from imageComparison_backend import run_verification
from ui_image_comparison import Ui_Form
from datetime import datetime
import sys
from database_module import MySqlManager  # Assuming your DB module is named like this

class ImageComparisonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.db_manager = MySqlManager()  # Connect to the database

    def compare_images(self, image_path):
        result = run_verification(image_path)

        now = datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')

        if not result["match_found"]:
            self.ui.label_3.setText("No Match Found")
            self.ui.orig_img.clear()
            self.ui.similar_img.clear()

            # Insert a log entry for failed attempt
            self.db_manager.insertLogEntries(
                id="N/A",
                date=date_str,
                time=time_str,
                faceCrop=image_path
            )
            return

        # Load and display original image
        pixmap1 = QPixmap(image_path).scaled(271, 241, Qt.KeepAspectRatio)
        self.ui.orig_img.setPixmap(pixmap1)

        # Load and display matched image
        matched_path = result["matched_image"]
        pixmap2 = QPixmap(matched_path).scaled(271, 241, Qt.KeepAspectRatio)
        self.ui.similar_img.setPixmap(pixmap2)

        # Fetch metadata from DB using matched image path
        matched_metadata = self.fetch_metadata_by_image(matched_path)

        # Update the UI
        self.ui.label_8.setText(f"ID: {matched_metadata.get('person_id', 'N/A')}")
        self.ui.label_6.setText(f"Date: {matched_metadata.get('date', date_str)}")
        self.ui.label_7.setText(f"Time: {matched_metadata.get('time', time_str)}")

        self.ui.label_9.setText(f"ID: {matched_metadata.get('person_id', 'N/A')}")
        self.ui.label_11.setText(f"Date: {matched_metadata.get('date', date_str)}")
        self.ui.label_10.setText(f"Time: {matched_metadata.get('time', time_str)}")

        self.ui.label_3.setText("Match Found")

        # Insert a log entry for successful match
        self.db_manager.insertLogEntries(
            id=matched_metadata.get('person_id', 'N/A'),
            date=matched_metadata.get('date', date_str),
            time=matched_metadata.get('time', time_str),
            faceCrop=matched_path
        )

    def fetch_metadata_by_image(self, image_path):
        """
        Query the DB to fetch metadata for a given image path.
        """
        try:
            query = "SELECT person_id, date, time FROM `logs.tbl` WHERE face_crops = %s LIMIT 1"
            self.db_manager.cursor.execute(query, (image_path,))
            row = self.db_manager.cursor.fetchone()

            if row:
                return {
                    "person_id": row[0],
                    "date": row[1],
                    "time": row[2]
                }
            else:
                return {}
        except Exception as e:
            print(f"Error fetching metadata: {e}")
            return {}

# To run the UI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageComparisonApp()
    window.show()

    # Optional: Load file dynamically for testing
    file_path, _ = QFileDialog.getOpenFileName(window, "Select Image", "", "Images (*.png *.jpg *.jpeg)")
    if file_path:
        window.compare_images(file_path)

    sys.exit(app.exec())
