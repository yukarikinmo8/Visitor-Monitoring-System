from PySide6.QtGui import QPainter, QPdfWriter, QFont, QPageSize
from PySide6.QtCore import Qt,QMarginsF,QSortFilterProxyModel
from PySide6.QtWidgets import QMessageBox
import os

class exportPDF:
    def exportTableToPDF(self, table, filePath):
        try:
            pdf_writer = QPdfWriter(filePath)
            pdf_writer.setPageSize(QPageSize(QPageSize.A4))
            pdf_writer.setResolution(300)
            pdf_writer.setPageMargins(QMarginsF(12, 16, 12, 20))

            painter = QPainter()
            if not painter.begin(pdf_writer):
                print("Failed to start painting on PDF.")
                return

            font = QFont("Arial", 10)
            painter.setFont(font)

            # Margins and spacing
            margin_x, margin_y = 50, 50
            row_height = 600
            col_widths = [500, 1100, 500]  # Adjust based on number/type of columns

            proxy_model = table.model()
            if isinstance(proxy_model, QSortFilterProxyModel):
                model = proxy_model.sourceModel()
            else:
                model = proxy_model

            row_count = proxy_model.rowCount()
            column_count = proxy_model.columnCount()

            # Draw headers
            x = margin_x
            y = margin_y
            for col in range(column_count):
                header = model.headerData(col, Qt.Horizontal)
                header_width = painter.fontMetrics().horizontalAdvance(str(header))
                # Center the header text based on the column width
                header_x = x + (col_widths[col] - header_width) / 2
                painter.drawText(header_x, y, str(header))
                x += col_widths[col] if col < len(col_widths) else 100
            y += 100  # space after headers

            # Draw each row
            for row in range(row_count):
                x = margin_x
                for col in range(column_count):
                    proxy_index = proxy_model.index(row, col)
                    source_index = proxy_model.mapToSource(proxy_index)
                    item = model.itemFromIndex(source_index)

                    if item:
                        icon = item.icon()
                        if not icon.isNull():
                            pixmap = icon.pixmap(500, 500)
                            painter.drawPixmap(x, y, pixmap)
                        else:
                            text = item.text()
                            text_width = painter.fontMetrics().horizontalAdvance(text)
                            # Center the text based on the column width
                            text_x = x + (col_widths[col] - text_width) / 2
                            painter.drawText(text_x, y + 20, text)
                    x += col_widths[col] if col < len(col_widths) else 100
                y += row_height

            painter.end()
            msg = QMessageBox()
            msg.setText(f"PDF exported to: {filePath}")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            

        except Exception as e:
            if painter.isActive():
                painter.end()
            painter.end()
            msg = QMessageBox()
            msg.setText(f"Error exporting table to PDF: {e}")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            
