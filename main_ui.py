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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStackedWidget, QTableView, QToolButton, QWidget)

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
        icon = QIcon()
        icon.addFile(u"resources/Icons/Menu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menu_btn.setIcon(icon)
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
        icon1 = QIcon()
        icon1.addFile(u"resources/Icons/Dashboard.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dash_btn.setIcon(icon1)
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
        icon2 = QIcon()
        icon2.addFile(u"resources/Icons/Camera.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cam_btn.setIcon(icon2)
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
        icon3 = QIcon()
        icon3.addFile(u"resources/Icons/Logs.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logs_btn.setIcon(icon3)
        self.logs_btn.setIconSize(QSize(45, 45))
        self.settings_btn = QToolButton(self.nav_bar)
        self.settings_btn.setObjectName(u"settings_btn")
        self.settings_btn.setGeometry(QRect(30, 270, 51, 51))
        self.settings_btn.setStyleSheet(u"#settings_btn{\n"
"background-color:transparent;\n"
"}\n"
"\n"
"#settings_btn:hover{\n"
"background-color:#5897FB;\n"
"}\n"
"\n"
"")
        icon4 = QIcon()
        icon4.addFile(u"resources/Icons/Settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_btn.setIcon(icon4)
        self.settings_btn.setIconSize(QSize(45, 45))
        self.dash_lbl = QLabel(self.nav_bar)
        self.dash_lbl.setObjectName(u"dash_lbl")
        self.dash_lbl.setGeometry(QRect(100, 90, 261, 51))
        font = QFont()
        font.setFamilies([u"Inter i"])
        self.dash_lbl.setFont(font)
        self.dash_lbl.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 25px; /* Adjust based on your UI scale */\n"
"    color: #EAEAEA;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
" }")
        self.lvf_lbl = QLabel(self.nav_bar)
        self.lvf_lbl.setObjectName(u"lvf_lbl")
        self.lvf_lbl.setGeometry(QRect(100, 150, 271, 51))
        self.lvf_lbl.setFont(font)
        self.lvf_lbl.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 25px; /* Adjust based on your UI scale */\n"
"    color: #EAEAEA;\n"
"    letter-spacing:1px; /* Adjust for spacing */\n"
" }")
        self.logs_lbl = QLabel(self.nav_bar)
        self.logs_lbl.setObjectName(u"logs_lbl")
        self.logs_lbl.setGeometry(QRect(100, 210, 181, 51))
        self.logs_lbl.setFont(font)
        self.logs_lbl.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 25px; /* Adjust based on your UI scale */\n"
"    color: #EAEAEA;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
" }")
        self.setts_lbl = QLabel(self.nav_bar)
        self.setts_lbl.setObjectName(u"setts_lbl")
        self.setts_lbl.setGeometry(QRect(100, 270, 181, 51))
        self.setts_lbl.setFont(font)
        self.setts_lbl.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 25px; /* Adjust based on your UI scale */\n"
"    color: #EAEAEA;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
" }")
        self.logo_lbl = QLabel(self.nav_bar)
        self.logo_lbl.setObjectName(u"logo_lbl")
        self.logo_lbl.setGeometry(QRect(40, 20, 481, 51))
        font1 = QFont()
        font1.setFamilies([u"Inter i"])
        font1.setBold(True)
        self.logo_lbl.setFont(font1)
        self.logo_lbl.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
" }")
        self.logo_lbl.raise_()
        self.menu_btn.raise_()
        self.dash_btn.raise_()
        self.cam_btn.raise_()
        self.logs_btn.raise_()
        self.settings_btn.raise_()
        self.dash_lbl.raise_()
        self.lvf_lbl.raise_()
        self.logs_lbl.raise_()
        self.setts_lbl.raise_()
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(120, 0, 1421, 821))
        self.stackedWidget.setLayoutDirection(Qt.RightToLeft)
        self.DashBoard = QWidget()
        self.DashBoard.setObjectName(u"DashBoard")
        self.label_5 = QLabel(self.DashBoard)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 30, 231, 31))
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.stackedWidget.addWidget(self.DashBoard)
        self.LiveFeed = QWidget()
        self.LiveFeed.setObjectName(u"LiveFeed")
        self.label = QLabel(self.LiveFeed)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 90, 1001, 551))
        font2 = QFont()
        font2.setPointSize(12)
        self.label.setFont(font2)
        self.label.setStyleSheet(u"background-color:#EAEAEA;")
        self.stop_btn = QPushButton(self.LiveFeed)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setGeometry(QRect(580, 670, 51, 51))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.stop_btn.setFont(font3)
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
        icon5 = QIcon()
        icon5.addFile(u"resources/Icons/stop.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.stop_btn.setIcon(icon5)
        self.stop_btn.setIconSize(QSize(45, 45))
        self.label_2 = QLabel(self.LiveFeed)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 291, 31))
        self.label_2.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.start_btn = QPushButton(self.LiveFeed)
        self.start_btn.setObjectName(u"start_btn")
        self.start_btn.setGeometry(QRect(520, 670, 51, 51))
        self.start_btn.setMinimumSize(QSize(5, 5))
        self.start_btn.setFont(font3)
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
        icon6 = QIcon()
        icon6.addFile(u"resources/Icons/Play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.start_btn.setIcon(icon6)
        self.start_btn.setIconSize(QSize(45, 45))
        self.frame = QFrame(self.LiveFeed)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(1090, -10, 291, 831))
        self.frame.setStyleSheet(u"background-color:#2C2F40")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.cap_4 = QLabel(self.frame)
        self.cap_4.setObjectName(u"cap_4")
        self.cap_4.setGeometry(QRect(20, 100, 251, 231))
        self.cap_4.setStyleSheet(u"background-color:#EAEAEA;")
        self.cap_5 = QLabel(self.frame)
        self.cap_5.setObjectName(u"cap_5")
        self.cap_5.setGeometry(QRect(20, 580, 251, 231))
        self.cap_5.setStyleSheet(u"background-color:#EAEAEA;")
        self.cap_6 = QLabel(self.frame)
        self.cap_6.setObjectName(u"cap_6")
        self.cap_6.setGeometry(QRect(20, 340, 251, 231))
        self.cap_6.setStyleSheet(u"background-color:#EAEAEA;")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 40, 291, 31))
        self.label_4.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 20px; /* Adjust based on your UI scale */\n"
"    font-weight:bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.refresh_btn = QPushButton(self.LiveFeed)
        self.refresh_btn.setObjectName(u"refresh_btn")
        self.refresh_btn.setGeometry(QRect(640, 670, 51, 51))
        self.refresh_btn.setMinimumSize(QSize(5, 5))
        self.refresh_btn.setFont(font3)
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
        icon7 = QIcon()
        icon7.addFile(u"resources/Icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.refresh_btn.setIcon(icon7)
        self.refresh_btn.setIconSize(QSize(45, 45))
        self.pause_btn = QPushButton(self.LiveFeed)
        self.pause_btn.setObjectName(u"pause_btn")
        self.pause_btn.setGeometry(QRect(450, 670, 51, 51))
        self.pause_btn.setMinimumSize(QSize(5, 5))
        self.pause_btn.setFont(font3)
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
        icon8 = QIcon()
        icon8.addFile(u"resources/Icons/Pause.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pause_btn.setIcon(icon8)
        self.pause_btn.setIconSize(QSize(45, 45))
        self.upload_btn = QPushButton(self.LiveFeed)
        self.upload_btn.setObjectName(u"upload_btn")
        self.upload_btn.setGeometry(QRect(700, 670, 51, 51))
        self.upload_btn.setMinimumSize(QSize(5, 5))
        self.upload_btn.setFont(font3)
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
        self.prec_btn = QPushButton(self.LiveFeed)
        self.prec_btn.setObjectName(u"prec_btn")
        self.prec_btn.setGeometry(QRect(380, 670, 51, 51))
        self.prec_btn.setMinimumSize(QSize(5, 5))
        self.prec_btn.setFont(font3)
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
        self.stackedWidget.addWidget(self.LiveFeed)
        self.Logs = QWidget()
        self.Logs.setObjectName(u"Logs")
        self.label_6 = QLabel(self.Logs)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 30, 201, 31))
        self.label_6.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.logs_tbl = QTableView(self.Logs)
        self.logs_tbl.setObjectName(u"logs_tbl")
        self.logs_tbl.setGeometry(QRect(40, 200, 1271, 601))
        self.logs_tbl.setLayoutDirection(Qt.LeftToRight)
        self.logs_tbl.setStyleSheet(u"#logs_tbl {\n"
"    background-color: white;\n"
"    color: black;\n"
"    font-size: 20px;\n"
" 	border: 1px solid white;\n"
"    selection-background-color: #5897FB;\n"
"    alternate-background-color:#dbe9f4;\n"
"}\n"
"\n"
"#logs_tbl::item:selected {\n"
"    background-color: #a7c8fb;\n"
"}\n"
"\n"
"#logs_tbl QHeaderView::section {\n"
"    background-color:#2c2f40;  /* Dark navy blue for header */\n"
"    color: white;  /* White text */\n"
"    font-size: 14px;  /* Optional: Adjust font size */\n"
"    font-weight: bold;  /* Optional: Make text bold */\n"
"    padding: 5px;  /* Optional: Adjust padding */\n"
"    border: 1px solid #d3d3d3;  /* Border color for header */\n"
"}\n"
"")
        self.export_btn = QPushButton(self.Logs)
        self.export_btn.setObjectName(u"export_btn")
        self.export_btn.setGeometry(QRect(1020, 130, 291, 51))
        self.export_btn.setStyleSheet(u"#export_btn{\n"
"    background-color: #5897FB; /* Default color */\n"
"    color: white;\n"
"	font-size: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#export_btn:hover{\n"
"	background-color: #2F6CDF;\n"
"}")
        self.search_txt = QLineEdit(self.Logs)
        self.search_txt.setObjectName(u"search_txt")
        self.search_txt.setGeometry(QRect(40, 130, 581, 51))
        self.search_txt.setStyleSheet(u"#search_txt {\n"
"    border: 2px solid #5897FB;\n"
"    border-radius: 25px;\n"
"    padding: 5px;\n"
"    background-color: #f5f5f5;\n"
"    font-size: 14px;\n"
"    color: #333;\n"
"	font-size: 20px;\n"
"}")
        self.stackedWidget.addWidget(self.Logs)
        self.Settings = QWidget()
        self.Settings.setObjectName(u"Settings")
        self.label_7 = QLabel(self.Settings)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(610, 450, 201, 101))
        self.label_7.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.stackedWidget.addWidget(self.Settings)
        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.raise_()
        self.nav_bar.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visitor Monitoring System", None))
        self.menu_btn.setText("")
        self.dash_btn.setText("")
        self.cam_btn.setText("")
        self.logs_btn.setText("")
        self.settings_btn.setText("")
        self.dash_lbl.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.lvf_lbl.setText(QCoreApplication.translate("MainWindow", u"Live Video Feed", None))
        self.logs_lbl.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.setts_lbl.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.logo_lbl.setText(QCoreApplication.translate("MainWindow", u"Visitor Monitoring System", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.label.setText("")
        self.stop_btn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Live Video Feed", None))
        self.start_btn.setText("")
        self.cap_4.setText("")
        self.cap_5.setText("")
        self.cap_6.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Face Capture", None))
        self.refresh_btn.setText("")
        self.pause_btn.setText("")
        self.upload_btn.setText("")
        self.prec_btn.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"LOGS", None))
        self.export_btn.setText(QCoreApplication.translate("MainWindow", u"Export  PDF", None))
        self.search_txt.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

