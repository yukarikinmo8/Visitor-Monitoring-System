import pymysql
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

class MySqlManager:

    def __init__(self):
        self.dbConnStr = pymysql.connect(host="localhost",user = "root", passwd="root", database="nh.vms")
        self.cursor = self.dbConnStr.cursor()

        #connection testing
    
    def fillLogsTable(self, table):
        self.cursor.execute("SELECT * FROM `logs.tbl`")
        data = self.cursor.fetchall()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "TIME", "FACE CAPTURE"])

        for row_data in data:
            items = []
            for field in row_data:
                item = QStandardItem(str(field))
                item.setTextAlignment(Qt.AlignCenter)  # ✅ Set alignment here
                items.append(item)
            self.model.appendRow(items)
            
        table.verticalHeader().setVisible(False)                
        table.setModel(self.model)

        for i in range(self.model.columnCount()):
            table.setColumnWidth(i, table.width() // self.model.columnCount())
        
     

    

if __name__ == "__main__":
    print("hi")