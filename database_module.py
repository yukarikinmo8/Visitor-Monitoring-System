import pymysql
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PySide6.QtWidgets import QStyledItemDelegate, QTableView, QComboBox
from PySide6.QtCore import Qt, QSize, QSortFilterProxyModel
import os
import logging



class ImageDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        data = index.data(Qt.DecorationRole)
        if isinstance(data, QIcon):
            pixmap = data.pixmap(option.rect.size())
            painter.drawPixmap(
                option.rect.x() + (option.rect.width() - pixmap.width()) // 2,
                option.rect.y() + (option.rect.height() - pixmap.height()) // 2,
                pixmap
            )
        else:
            super().paint(painter, option, index)

class MySqlManager:
    model = QStandardItemModel()
    def __init__(self):
        self.dbConnStr = pymysql.connect(host = "localhost",user = "root", passwd="root", database="nh.vms")
        self.cursor = self.dbConnStr.cursor()

        #connection testing
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)
        

    def fillLogsTable(self, table):
        self.cursor.execute("SELECT * FROM `logs.tbl`")
        data = self.cursor.fetchall()

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "DATE", "TIME", "FACE CAPTURE"])

        last_col_index = 3  # The Image column index

        for row_data in data:
            items = []

            for col_index, field in enumerate(row_data):
                if col_index == last_col_index:
                    file_path = field
                    image = self.imageLoader(file_path)  # your method that returns a QStandardItem with an icon
                    image.setTextAlignment(Qt.AlignCenter)

                    # ✅ Store the file path using Qt.UserRole
                    image.setData(file_path, Qt.UserRole)

                    items.append(image)
                else:
                    item = QStandardItem(str(field))
                    item.setTextAlignment(Qt.AlignCenter)
                    items.append(item)

            model.appendRow(items)

            # Table setup
            table.setEditTriggers(QTableView.NoEditTriggers)
            self.proxy_model = QSortFilterProxyModel()
            self.proxy_model.setSourceModel(model)

            table.setModel(self.proxy_model)
            table.setSortingEnabled(True)

            image_delegate = ImageDelegate()
            table.setItemDelegateForColumn(last_col_index, image_delegate)

            table.verticalHeader().setVisible(False)
            table.verticalHeader().setDefaultSectionSize(110)
            table.resizeColumnsToContents()
            table.setIconSize(QSize(100, 100))

            for i in range(model.columnCount()):
                table.setColumnWidth(i, table.width() // model.columnCount())

    def fillComboBox(self, combobox):
        try:
            self.cursor.execute("SELECT DISTINCT date FROM `logs.tbl` ORDER BY date DESC")
            dates = self.cursor.fetchall()

            combobox.clear()  # Clear existing items if any

            for date_tuple in dates:
                combobox.addItem(str(date_tuple[0]))  # date_tuple[0] is the actual date value

        except Exception as e:
            print(f"Error populating combobox: {e}")

    def fillExportTable(self, date, table):
        query = "SELECT * FROM `logs.tbl` WHERE date = %s"
        self.cursor.execute(query, (date,))
        data = self.cursor.fetchall()
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "DATE", "TIME", "FACE CAPTURE"])

        last_col_index = 3 # The Image column is at index 3 (0-based)

        # Iterate through each row of data
        for row_data in data:
            items = []  # Create an empty list to store QStandardItems for the row

            # Step 1: Populate all columns except the last one (Image)
            for col_index, field in enumerate(row_data):
                item = QStandardItem(str(field))
                item.setTextAlignment(Qt.AlignCenter)  # Set alignment here

                # Append the item for the column (ID, Time, Filepath)
                items.append(item)

                # If it's the last column (Image), add the image after populating the other columns
                if col_index == last_col_index:  # If it's the last column (Image)
                    file_path = row_data[last_col_index]  # Get the file path from the row data (last column)
                    image = self.imageLoader(file_path)  # Load the image using your imageLoader method
                    logging.debug(f"File Path for row: {file_path}")
                    # Set the image item in the last column (Image)
                    items[-1] = image  # Replace the last item with the image

            # After filling the row with columns and the image, add the entire row to the model
            model.appendRow(items)

        table.setEditTriggers(QTableView.NoEditTriggers)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)

        table.setModel(self.proxy_model)
        table.setSortingEnabled(True)
      
        image_delegate = ImageDelegate()
        table.setItemDelegateForColumn(last_col_index, image_delegate)

        table.verticalHeader().setVisible(False)   
        table.verticalHeader().setDefaultSectionSize(110)     
        table.resizeColumnsToContents() 
        table.setIconSize(QSize(100, 100))   
        

        for i in range(model.columnCount()):
            table.setColumnWidth(i, table.width() // model.columnCount())

    def insertLogEntries(self, id, date, time, faceCrop):
        self.cursor.execute("SELECT COUNT(*) FROM `logs.tbl` WHERE time = %s", (time,))
        if self.cursor.fetchone()[0] > 0:
            logging.debug(f"Skipping insert: Time {time} already exists.")
            return  # Skip inserting duplicates

        query = """
            INSERT INTO `logs.tbl` (person_id, date, time, face_crops)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (id, date, time, faceCrop))
        self.dbConnStr.commit()

    def upsertLogEntry(self, person_id, date, time, faceCrop):
        """
        Check if person_id exists, update if it does, insert if it doesn't.
        """
        # Check if person_id exists in database
        self.cursor.execute("SELECT COUNT(*) FROM `logs.tbl` WHERE person_id = %s", (person_id,))
        person_exists = self.cursor.fetchone()[0] > 0
        
        if person_exists:
            # Update the existing record
            query = """
                UPDATE `logs.tbl` 
                SET date = %s, time = %s, face_crops = %s
                WHERE person_id = %s
            """
            self.cursor.execute(query, (date, time, faceCrop, person_id))
            logging.debug(f"Updated record for person_id: {person_id}")
        else:
            # Insert a new record
            query = """
                INSERT INTO `logs.tbl` (person_id, date, time, face_crops)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (person_id, date, time, faceCrop))
            logging.debug(f"Inserted new record for person_id: {person_id}")
        
        self.dbConnStr.commit()
        return person_exists
    
    def search_personID(self, person_id):
        self.cursor.execute("SELECT * FROM `logs.tbl` WHERE person_id = %s", (person_id,))
        data = self.cursor.fetchall()

        if not data:
            print(f"No records found for person ID: {person_id}")
            return None
        
        record = data[0]
        
        return {
            'person_id': record[0],
            'date': record[1],
            'time': record[2],
            'face_path': record[3]
        }

        

    def imageLoader(self, imagePath):
        # Check if the image path exists
       
        if not os.path.exists(imagePath):
            print(f"Image not found: {imagePath}")
            return QStandardItem("No Image")

        pixmap = QPixmap(imagePath)
        if pixmap.isNull():
            print(f"Failed to load image: {imagePath}")
            return QStandardItem("Invalid Image")

        item = QStandardItem()  # No text
        item.setIcon(QIcon(pixmap))  # Only icon

        return item
 
    def updateDashboardStats(self, date_labels, count_labels):
        try:
            # Step 1: Get 4 latest unique dates
            self.cursor.execute("""
                SELECT DISTINCT DATE(date) AS log_date
                FROM `logs.tbl`
                ORDER BY log_date DESC
                LIMIT 4
            """)
            recent_dates = [row[0] for row in self.cursor.fetchall()]

            results = []
            # Step 2: For each date, count number of entries
            for log_date in recent_dates:
                self.cursor.execute("""
                    SELECT COUNT(*) FROM `logs.tbl`
                    WHERE DATE(date) = %s
                """, (log_date,))
                count = self.cursor.fetchone()[0]
                results.append((log_date, count))

            # Step 3: Populate passed UI label lists
            for i, (log_date, entry_count) in enumerate(results):
                date_labels[i].setText(f"Date: {log_date}")
                count_labels[i].setText(f"Total Entry: {entry_count}")

            # Step 4: Fill empty labels if fewer than 4 dates
            for j in range(len(results), 4):
                date_labels[j].setText("Date: No Data")
                count_labels[j].setText("Total Entry: 0")

        except Exception as e:
            print(f"Error updating dashboard stats: {e}")

if __name__ == "__main__":
    msm = MySqlManager()

    imagePath = r"D:\Browser Downloads\Taz.jpg"

    if not os.path.exists(imagePath):
            print(f"Image not found: {imagePath}")
    else: 
            print("Valid path")