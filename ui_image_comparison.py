# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'image_comparison.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(862, 544)
        Form.setStyleSheet(u"background-color: #232531;")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 10, 231, 41))
        self.label_3.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 20px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 110, 391, 421))
        self.frame.setStyleSheet(u"background-color:#2C2F40")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.orig_img = QLabel(self.frame)
        self.orig_img.setObjectName(u"orig_img")
        self.orig_img.setGeometry(QRect(60, 40, 271, 241))
        self.orig_img.setStyleSheet(u"background-color:#EAEAEA;")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 0, 231, 31))
        self.label_4.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.date_lbl1 = QLabel(self.frame)
        self.date_lbl1.setObjectName(u"date_lbl1")
        self.date_lbl1.setGeometry(QRect(20, 340, 351, 31))
        self.date_lbl1.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.time_lbl1 = QLabel(self.frame)
        self.time_lbl1.setObjectName(u"time_lbl1")
        self.time_lbl1.setGeometry(QRect(20, 370, 351, 31))
        self.time_lbl1.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.id_lbl1 = QLabel(self.frame)
        self.id_lbl1.setObjectName(u"id_lbl1")
        self.id_lbl1.setGeometry(QRect(20, 310, 351, 31))
        self.id_lbl1.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(450, 110, 391, 421))
        self.frame_2.setStyleSheet(u"background-color:#2C2F40")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.similar_img = QLabel(self.frame_2)
        self.similar_img.setObjectName(u"similar_img")
        self.similar_img.setGeometry(QRect(60, 40, 271, 241))
        self.similar_img.setStyleSheet(u"background-color:#EAEAEA;")
        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 0, 231, 31))
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.id_lbl2 = QLabel(self.frame_2)
        self.id_lbl2.setObjectName(u"id_lbl2")
        self.id_lbl2.setGeometry(QRect(20, 310, 351, 31))
        self.id_lbl2.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.time_lbl2 = QLabel(self.frame_2)
        self.time_lbl2.setObjectName(u"time_lbl2")
        self.time_lbl2.setGeometry(QRect(20, 370, 351, 31))
        self.time_lbl2.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.date_lbl2 = QLabel(self.frame_2)
        self.date_lbl2.setObjectName(u"date_lbl2")
        self.date_lbl2.setGeometry(QRect(20, 340, 351, 31))
        self.date_lbl2.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.frame_2.raise_()
        self.frame.raise_()
        self.label_3.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Image Comparison", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"image comparison", None))
        self.orig_img.setText("")
        self.label_4.setText(QCoreApplication.translate("Form", u"reference image:", None))
        self.date_lbl1.setText(QCoreApplication.translate("Form", u"Date:", None))
        self.time_lbl1.setText(QCoreApplication.translate("Form", u"Time:", None))
        self.id_lbl1.setText(QCoreApplication.translate("Form", u"ID:", None))
        self.similar_img.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"matched image:", None))
        self.id_lbl2.setText(QCoreApplication.translate("Form", u"ID:", None))
        self.time_lbl2.setText(QCoreApplication.translate("Form", u"Time:", None))
        self.date_lbl2.setText(QCoreApplication.translate("Form", u"Date:", None))
    # retranslateUi

