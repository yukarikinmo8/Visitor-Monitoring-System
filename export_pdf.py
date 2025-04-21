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
            pdf_writer.setPageMargins(QMarginsF(20, 16, 20, 20))

            painter = QPainter()
            if not painter.begin(pdf_writer):
                print("Failed to start painting on PDF.")
                return

            font = QFont("Arial", 10)
            painter.setFont(font)

            # Margins and spacing
            margin_x, margin_y = 50, 50
            row_height = 600
            col_widths = [300, 500, 550, 500]  # Adjust based on number/type of columns

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
            # Draw each row with grid
            for row in range(row_count):
                x = margin_x
                for col in range(column_count):
                    proxy_index = proxy_model.index(row, col)
                    source_index = proxy_model.mapToSource(proxy_index)
                    item = model.itemFromIndex(source_index)

                    # Define current cell width and height
                    cell_width = col_widths[col] if col < len(col_widths) else 100
                    cell_height = row_height

                    # Draw grid rectangle
                    painter.drawRect(x, y, cell_width, cell_height)

                    # Draw icon or text centered
                    if item:
                        icon = item.icon()
                        if not icon.isNull():
                            pixmap = icon.pixmap(cell_height - 100, cell_height - 100)
                            painter.drawPixmap(x + (cell_width - pixmap.width()) // 2,
                                            y + (cell_height - pixmap.height()) // 2,
                                            pixmap)
                        else:
                            text = item.text()
                            text_width = painter.fontMetrics().horizontalAdvance(text)
                            text_height = painter.fontMetrics().height()
                            text_x = x + (cell_width - text_width) / 2
                            text_y = y + (cell_height + text_height) / 2 - 10
                            painter.drawText(text_x, text_y, text)

                    x += cell_width
                y += row_height

            painter.end()
            msg = QMessageBox()
            msg.setText(f"PDF exported to: {filePath}")
            msg.setWindowTitle("Pdf Export Success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            

        except Exception as e:
            if painter.isActive():
                painter.end()
            painter.end()
            msg = QMessageBox()
            msg.setText(f"Pdf Export Failed: {e}")
            msg.setWindowTitle("Info")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            
