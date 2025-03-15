# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sample.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 823)
        MainWindow.setMinimumSize(QSize(1500, 800))
        MainWindow.setMaximumSize(QSize(1500, 823))
        MainWindow.setStyleSheet(u"background-color: #232531")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(180, 90, 1001, 551))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color:#EAEAEA;")
        self.start_btn = QPushButton(self.centralwidget)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setGeometry(QRect(640, 670, 51, 51))
        self.start_btn.setMinimumSize(QSize(5, 5))
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.start_btn.setFont(font1)
        self.start_btn.setAutoFillBackground(False)
        self.start_btn.setStyleSheet(u"#start_btn {\n"
"    background-color: #232531; /* Default color */\n"
"    color: white;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"#start_btn:hover {\n"
"    background-color: #5897FB; /* Hover color */\n"
"}")
        icon = QIcon()
        icon.addFile(u"resources/Icons/Play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.start_btn.setIcon(icon)
        self.start_btn.setIconSize(QSize(45, 45))
        self.stop_btn = QPushButton(self.centralwidget)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setGeometry(QRect(700, 670, 51, 51))
        self.stop_btn.setFont(font1)
        self.stop_btn.setStyleSheet(u"#stop_btn {\n"
"    background-color: #232531; /* Default color */\n"
"    color: white;\n"
"    border-radius: 25px;\n"
"\n"
"}\n"
"\n"
"#stop_btn:hover {\n"
"    background-color: #5897FB; /* Hover color */\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"resources/Icons/stop.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stop_btn.setIcon(icon1)
        self.stop_btn.setIconSize(QSize(45, 45))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(1210, -10, 291, 831))
        self.frame.setStyleSheet(u"background-color:#2C2F40")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.cap_1 = QLabel(self.frame)
        self.cap_1.setObjectName(u"cap_1")
        self.cap_1.setGeometry(QRect(20, 100, 251, 231))
        self.cap_1.setStyleSheet(u"background-color:#EAEAEA;")
        self.cap_3 = QLabel(self.frame)
        self.cap_3.setObjectName(u"cap_3")
        self.cap_3.setGeometry(QRect(20, 580, 251, 231))
        self.cap_3.setStyleSheet(u"background-color:#EAEAEA;")
        self.cap_2 = QLabel(self.frame)
        self.cap_2.setObjectName(u"cap_2")
        self.cap_2.setGeometry(QRect(20, 340, 251, 231))
        self.cap_2.setStyleSheet(u"background-color:#EAEAEA;")
        self.nav_bar = QFrame(self.centralwidget)
        self.nav_bar.setObjectName(u"nav_bar")
        self.nav_bar.setGeometry(QRect(0, 0, 111, 831))
        self.nav_bar.setStyleSheet(u"background-color:#2C2F40")
        self.nav_bar.setFrameShape(QFrame.StyledPanel)
        self.nav_bar.setFrameShadow(QFrame.Raised)
        self.menu_btn = QToolButton(self.nav_bar)
        self.menu_btn.setObjectName(u"menu_btn")
        self.menu_btn.setGeometry(QRect(30, 20, 51, 51))
        self.menu_btn.setStyleSheet(u"#menu_btn{\n"
"	background-color: transparent;\n"
"}\n"
"\n"
"#menu_btn:hover{\n"
"	background-color:#5897FB;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"resources/Icons/Menu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_btn.setIcon(icon2)
        self.menu_btn.setIconSize(QSize(45, 45))
        self.dash_btn = QToolButton(self.nav_bar)
        self.dash_btn.setObjectName(u"dash_btn")
        self.dash_btn.setGeometry(QRect(30, 90, 51, 51))
        self.dash_btn.setStyleSheet(u"#dash_btn{\n"
"background-color:transparent;\n"
"}\n"
"\n"
"#dash_btn:hover{\n"
"background-color:#5897FB;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u"resources/Icons/Dashboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dash_btn.setIcon(icon3)
        self.dash_btn.setIconSize(QSize(45, 45))
        self.dash_btn.setPopupMode(QToolButton.InstantPopup)
        self.dash_btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.cam_btn = QToolButton(self.nav_bar)
        self.cam_btn.setObjectName(u"cam_btn")
        self.cam_btn.setGeometry(QRect(30, 150, 51, 51))
        self.cam_btn.setStyleSheet(u"#cam_btn{\n"
"background-color:transparent;\n"
"}\n"
"\n"
"#cam_btn:hover{\n"
"background-color:#5897FB;\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u"resources/Icons/Camera.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cam_btn.setIcon(icon4)
        self.cam_btn.setIconSize(QSize(45, 45))
        self.logs_btn = QToolButton(self.nav_bar)
        self.logs_btn.setObjectName(u"logs_btn")
        self.logs_btn.setGeometry(QRect(30, 210, 51, 51))
        self.logs_btn.setStyleSheet(u"#logs_btn{\n"
"background-color:transparent;\n"
"}\n"
"\n"
"#logs_btn:hover{\n"
"background-color:#5897FB;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u"resources/Icons/Logs.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logs_btn.setIcon(icon5)
        self.logs_btn.setIconSize(QSize(45, 45))
        self.setttings_btn = QToolButton(self.nav_bar)
        self.setttings_btn.setObjectName(u"setttings_btn")
        self.setttings_btn.setGeometry(QRect(30, 270, 51, 51))
        self.setttings_btn.setStyleSheet(u"#settings_btn{\n"
"background-color:transparent;\n"
"}\n"
"\n"
"#settings_btn:hover{\n"
"background-color:#5897FB;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u"resources/Icons/Settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.setttings_btn.setIcon(icon6)
        self.setttings_btn.setIconSize(QSize(45, 45))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 30, 291, 31))
        self.label_2.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.pause_btn = QPushButton(self.centralwidget)
        self.pause_btn.setObjectName(u"pause_btn")
        self.pause_btn.setGeometry(QRect(570, 670, 51, 51))
        self.pause_btn.setMinimumSize(QSize(5, 5))
        self.pause_btn.setFont(font1)
        self.pause_btn.setAutoFillBackground(False)
        self.pause_btn.setStyleSheet(u"#pause_btn{\n"
"    background-color: #232531; /* Default color */\n"
"    color: white;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"#pause_btn:hover{\n"
"	background-color:#5897FB ;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u"resources/Icons/Pause.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pause_btn.setIcon(icon7)
        self.pause_btn.setIconSize(QSize(45, 45))
        self.refresh_btn = QPushButton(self.centralwidget)
        self.refresh_btn.setObjectName(u"refresh_btn")
        self.refresh_btn.setGeometry(QRect(780, 670, 51, 51))
        self.refresh_btn.setMinimumSize(QSize(5, 5))
        self.refresh_btn.setFont(font1)
        self.refresh_btn.setAutoFillBackground(False)
        self.refresh_btn.setStyleSheet(u"#refresh_btn{\n"
"    background-color: #232531; /* Default color */\n"
"    color: white;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"#refresh_btn:hover{\n"
"	background-color:#5897FB ;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u"resources/Icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_btn.setIcon(icon8)
        self.refresh_btn.setIconSize(QSize(45, 45))
        self.upload_btn = QPushButton(self.centralwidget)
        self.upload_btn.setObjectName(u"upload_btn")
        self.upload_btn.setGeometry(QRect(840, 670, 51, 51))
        self.upload_btn.setMinimumSize(QSize(5, 5))
        self.upload_btn.setFont(font1)
        self.upload_btn.setAutoFillBackground(False)
        self.upload_btn.setStyleSheet(u"#upload_btn{\n"
"    background-color: #232531; /* Default color */\n"
"    color: white;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"#upload_btn:hover{\n"
"	background-color:#5897FB ;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u"resources/Icons/Upload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.upload_btn.setIcon(icon9)
        self.upload_btn.setIconSize(QSize(45, 45))
        self.prec_btn = QPushButton(self.centralwidget)
        self.prec_btn.setObjectName(u"prec_btn")
        self.prec_btn.setGeometry(QRect(500, 670, 51, 51))
        self.prec_btn.setMinimumSize(QSize(5, 5))
        self.prec_btn.setFont(font1)
        self.prec_btn.setAutoFillBackground(False)
        self.prec_btn.setStyleSheet(u"#prec_btn{\n"
"    background-color: #232531; /* Default color */\n"
"    color: white;\n"
"    border-radius: 25px;\n"
"}\n"
"\n"
"#prec_btn:hover{\n"
"	background-color:#5897FB ;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u"resources/Icons/target.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.prec_btn.setIcon(icon10)
        self.prec_btn.setIconSize(QSize(45, 45))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visitor Monitoring System", None))
        self.label.setText("")
        self.start_btn.setText("")
        self.stop_btn.setText("")
        self.cap_1.setText("")
        self.cap_3.setText("")
        self.cap_2.setText("")
        self.menu_btn.setText("")
        self.dash_btn.setText("")
        self.cam_btn.setText("")
        self.logs_btn.setText("")
        self.setttings_btn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Live Video Feed", None))
        self.pause_btn.setText("")
        self.refresh_btn.setText("")
        self.upload_btn.setText("")
        self.prec_btn.setText("")
    # retranslateUi

