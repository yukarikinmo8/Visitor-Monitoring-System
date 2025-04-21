import pymysql
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PySide6.QtWidgets import QStyledItemDelegate, QTableView
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
        self.dbConnStr = pymysql.connect(host = "localhost",user = "root", passwd="admin", database="nh.vms")
        self.cursor = self.dbConnStr.cursor()

        #connection testing
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)
        

    def fillLogsTable(self, table):
        self.cursor.execute("SELECT * FROM `logs.tbl`")
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
 
    

if __name__ == "__main__":
    msm = MySqlManager()

    imagePath = r"D:\Browser Downloads\Taz.jpg"

    if not os.path.exists(imagePath):
            print(f"Image not found: {imagePath}")
    else: 
            print("Valid path")