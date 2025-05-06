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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QTableView, QToolButton,
    QWidget)

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
        self.menu_btn.setGeometry(QRect(0, 0, 111, 51))
        self.menu_btn.setStyleSheet(u"#menu_btn{\n"
"	background-color: transparent;\n"
"	border: none;\n"
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
        self.dash_btn.setGeometry(QRect(0, 90, 111, 51))
        self.dash_btn.setLayoutDirection(Qt.LeftToRight)
        self.dash_btn.setStyleSheet(u"#dash_btn{\n"
"	background-color:transparent;\n"
"	font-size: 25px;\n"
"	font-family: \"Inter\"i;\n"
"	border: none;\n"
"}\n"
"\n"
"#dash_btn:hover{\n"
"	background-color:#5897FB;\n"
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
        self.cam_btn.setGeometry(QRect(0, 150, 111, 51))
        self.cam_btn.setStyleSheet(u"#cam_btn{\n"
"	background-color:transparent;\n"
"	font-size: 25px;\n"
"	font-family: \"Inter\"i;\n"
"	border: none;\n"
"}\n"
"\n"
"#cam_btn:hover{\n"
"background-color:#5897FB;\n"
"}\n"
"\n"
"")
        icon2 = QIcon()
        icon2.addFile(u"resources/Icons/Camera.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cam_btn.setIcon(icon2)
        self.cam_btn.setIconSize(QSize(45, 45))
        self.logs_btn = QToolButton(self.nav_bar)
        self.logs_btn.setObjectName(u"logs_btn")
        self.logs_btn.setGeometry(QRect(0, 210, 111, 51))
        self.logs_btn.setStyleSheet(u"#logs_btn{\n"
"	background-color:transparent;\n"
"	font-size: 25px;\n"
"	font-family: \"Inter\"i;\n"
"	border: none;\n"
"}\n"
"\n"
"#logs_btn:hover{\n"
"background-color:#5897FB;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u"resources/Icons/Logs.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.logs_btn.setIcon(icon3)
        self.logs_btn.setIconSize(QSize(45, 45))
        self.settings_btn = QToolButton(self.nav_bar)
        self.settings_btn.setObjectName(u"settings_btn")
        self.settings_btn.setGeometry(QRect(0, 270, 111, 51))
        self.settings_btn.setStyleSheet(u"#settings_btn{\n"
"	background-color:transparent;\n"
"	font-size: 25px;\n"
"	font-family: \"Inter\"i;\n"
"	border: none;\n"
"}\n"
"\n"
"#settings_btn:hover{\n"
"background-color:#5897FB;\n"
"}\n"
"\n"
"\n"
"")
        icon4 = QIcon()
        icon4.addFile(u"resources/Icons/Settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_btn.setIcon(icon4)
        self.settings_btn.setIconSize(QSize(45, 45))
        self.logo_lbl = QLabel(self.nav_bar)
        self.logo_lbl.setObjectName(u"logo_lbl")
        self.logo_lbl.setGeometry(QRect(30, 10, 201, 51))
        font = QFont()
        font.setFamilies([u"Inter i"])
        font.setBold(True)
        self.logo_lbl.setFont(font)
        self.logo_lbl.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 20px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
" }")
        self.logo_lbl.setPixmap(QPixmap(u"resources/Icons/logonhvms.png"))
        self.logo_lbl.raise_()
        self.menu_btn.raise_()
        self.dash_btn.raise_()
        self.cam_btn.raise_()
        self.logs_btn.raise_()
        self.settings_btn.raise_()
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(130, -10, 1421, 821))
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
        self.dashFrame1 = QFrame(self.DashBoard)
        self.dashFrame1.setObjectName(u"dashFrame1")
        self.dashFrame1.setGeometry(QRect(40, 170, 301, 281))
        self.dashFrame1.setStyleSheet(u"#dashFrame1 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#dashFrame1::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.dashFrame1.setFrameShape(QFrame.StyledPanel)
        self.dashFrame1.setFrameShadow(QFrame.Raised)
        self.dateLabel1 = QLabel(self.dashFrame1)
        self.dateLabel1.setObjectName(u"dateLabel1")
        self.dateLabel1.setGeometry(QRect(10, 30, 261, 41))
        self.dateLabel1.setStyleSheet(u"#dateLabel1 {\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#dateLabel1:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.totalEntry1 = QLabel(self.dashFrame1)
        self.totalEntry1.setObjectName(u"totalEntry1")
        self.totalEntry1.setGeometry(QRect(10, 220, 271, 41))
        self.totalEntry1.setStyleSheet(u"#totalEntry1{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#totalEntry1:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.dashFrame2 = QFrame(self.DashBoard)
        self.dashFrame2.setObjectName(u"dashFrame2")
        self.dashFrame2.setGeometry(QRect(360, 170, 301, 281))
        self.dashFrame2.setStyleSheet(u"#dashFrame2 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#dashFrame2::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.dashFrame2.setFrameShape(QFrame.StyledPanel)
        self.dashFrame2.setFrameShadow(QFrame.Raised)
        self.dateLabel2 = QLabel(self.dashFrame2)
        self.dateLabel2.setObjectName(u"dateLabel2")
        self.dateLabel2.setGeometry(QRect(10, 30, 261, 41))
        self.dateLabel2.setStyleSheet(u"#dateLabel2 {\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#dateLabel2:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.totalEntry2 = QLabel(self.dashFrame2)
        self.totalEntry2.setObjectName(u"totalEntry2")
        self.totalEntry2.setGeometry(QRect(10, 220, 261, 41))
        self.totalEntry2.setStyleSheet(u"#totalEntry2{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#totalEntry2:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.dashFrame3 = QFrame(self.DashBoard)
        self.dashFrame3.setObjectName(u"dashFrame3")
        self.dashFrame3.setGeometry(QRect(680, 170, 301, 281))
        self.dashFrame3.setStyleSheet(u"#dashFrame3 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#dashFrame3::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.dashFrame3.setFrameShape(QFrame.StyledPanel)
        self.dashFrame3.setFrameShadow(QFrame.Raised)
        self.totalEntry3 = QLabel(self.dashFrame3)
        self.totalEntry3.setObjectName(u"totalEntry3")
        self.totalEntry3.setGeometry(QRect(10, 220, 271, 41))
        self.totalEntry3.setStyleSheet(u"#totalEntry3{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#totalEntry3:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.dateLabel3 = QLabel(self.dashFrame3)
        self.dateLabel3.setObjectName(u"dateLabel3")
        self.dateLabel3.setGeometry(QRect(10, 30, 251, 41))
        self.dateLabel3.setStyleSheet(u"#dateLabel3 {\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#dateLabel3:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.dashFrame4 = QFrame(self.DashBoard)
        self.dashFrame4.setObjectName(u"dashFrame4")
        self.dashFrame4.setGeometry(QRect(1000, 170, 301, 281))
        self.dashFrame4.setStyleSheet(u"#dashFrame4 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#dashFrame4::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.dashFrame4.setFrameShape(QFrame.StyledPanel)
        self.dashFrame4.setFrameShadow(QFrame.Raised)
        self.totalEntry4 = QLabel(self.dashFrame4)
        self.totalEntry4.setObjectName(u"totalEntry4")
        self.totalEntry4.setGeometry(QRect(10, 220, 271, 41))
        self.totalEntry4.setStyleSheet(u"#totalEntry4{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#totalEntry4:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.dateLabel4 = QLabel(self.dashFrame4)
        self.dateLabel4.setObjectName(u"dateLabel4")
        self.dateLabel4.setGeometry(QRect(10, 30, 271, 41))
        self.dateLabel4.setStyleSheet(u"#dateLabel4 {\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#dateLabel4:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.dashFrame5 = QFrame(self.DashBoard)
        self.dashFrame5.setObjectName(u"dashFrame5")
        self.dashFrame5.setGeometry(QRect(40, 470, 621, 311))
        self.dashFrame5.setStyleSheet(u"#dashFrame5 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#dashFrame5::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.dashFrame5.setFrameShape(QFrame.StyledPanel)
        self.dashFrame5.setFrameShadow(QFrame.Raised)
        self.logsPrev = QLabel(self.dashFrame5)
        self.logsPrev.setObjectName(u"logsPrev")
        self.logsPrev.setGeometry(QRect(10, 10, 181, 41))
        self.logsPrev.setStyleSheet(u"#logsPrev{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#logsPrev:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.logsPrev_tbl = QTableView(self.dashFrame5)
        self.logsPrev_tbl.setObjectName(u"logsPrev_tbl")
        self.logsPrev_tbl.setGeometry(QRect(20, 61, 581, 231))
        self.logsPrev_tbl.setLayoutDirection(Qt.LeftToRight)
        self.logsPrev_tbl.setStyleSheet(u"#logsPrev_tbl {\n"
"    background-color: white;\n"
"    color: black;\n"
"    font-size: 20px;\n"
" 	border: 1px solid white;\n"
"    selection-background-color: #5897FB;\n"
"    alternate-background-color:#dbe9f4;\n"
"}\n"
"\n"
"#logsPrev_tbl::item:selected {\n"
"    background-color: #a7c8fb;\n"
"}\n"
"\n"
"#logsPrev_tbl QHeaderView::section {\n"
"    background-color:#2c2f40;  /* Dark navy blue for header */\n"
"    color: white;  /* White text */\n"
"    font-size: 14px;  /* Optional: Adjust font size */\n"
"    font-weight: bold;  /* Optional: Make text bold */\n"
"    padding: 5px;  /* Optional: Adjust padding */\n"
"    border: 1px solid #d3d3d3;  /* Border color for header */\n"
"}\n"
"")
        self.dashFrame6 = QFrame(self.DashBoard)
        self.dashFrame6.setObjectName(u"dashFrame6")
        self.dashFrame6.setGeometry(QRect(680, 470, 621, 311))
        self.dashFrame6.setStyleSheet(u"#dashFrame6 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#dashFrame6::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.dashFrame6.setFrameShape(QFrame.StyledPanel)
        self.dashFrame6.setFrameShadow(QFrame.Raised)
        self.stackedWidget.addWidget(self.DashBoard)
        self.LiveFeed = QWidget()
        self.LiveFeed.setObjectName(u"LiveFeed")
        self.label = QLabel(self.LiveFeed)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 90, 1001, 551))
        font1 = QFont()
        font1.setPointSize(12)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"background-color:#EAEAEA;")
        self.stop_btn = QPushButton(self.LiveFeed)
        self.stop_btn.setObjectName(u"stop_btn")
        self.stop_btn.setGeometry(QRect(560, 650, 151, 51))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.stop_btn.setFont(font2)
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
        self.start_btn.setGeometry(QRect(390, 650, 151, 51))
        self.start_btn.setMinimumSize(QSize(5, 5))
        self.start_btn.setFont(font2)
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
        self.label_7.setGeometry(QRect(10, 30, 201, 31))
        self.label_7.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.configFrame1 = QFrame(self.Settings)
        self.configFrame1.setObjectName(u"configFrame1")
        self.configFrame1.setGeometry(QRect(50, 170, 301, 281))
        self.configFrame1.setStyleSheet(u"#configFrame1 {\n"
"  border-radius: 15px;\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #3A8DFF,\n"
"        stop: 1 #1D69E2\n"
"    );\n"
"    border: 2px solid #2a85ff;\n"
"}\n"
"\n"
"#configFrame1::hover {\n"
"    background: qlineargradient(\n"
"        x1: 0, y1: 0,\n"
"        x2: 0, y2: 1,\n"
"        stop: 0 #5BAEFF,\n"
"        stop: 1 #3284E6\n"
"    );\n"
"}")
        self.configFrame1.setFrameShape(QFrame.StyledPanel)
        self.configFrame1.setFrameShadow(QFrame.Raised)
        self.configLabel1 = QLabel(self.configFrame1)
        self.configLabel1.setObjectName(u"configLabel1")
        self.configLabel1.setGeometry(QRect(20, 20, 261, 41))
        self.configLabel1.setStyleSheet(u"#configLabel1 {\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 20px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#configLabel1:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.x_lbl = QLabel(self.configFrame1)
        self.x_lbl.setObjectName(u"x_lbl")
        self.x_lbl.setGeometry(QRect(10, 90, 121, 31))
        self.x_lbl.setStyleSheet(u"#x_lbl{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 15px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#x_lbl:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.y_lbl = QLabel(self.configFrame1)
        self.y_lbl.setObjectName(u"y_lbl")
        self.y_lbl.setGeometry(QRect(10, 140, 121, 31))
        self.y_lbl.setStyleSheet(u"#y_lbl{\n"
"    color: white;\n"
"    background: transparent;  /* Let the frame's gradient show through */\n"
"    font-weight: bold;\n"
"    font-size: 15px;\n"
"    padding: 4px 8px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#y_lbl:hover {\n"
"    color: #E0F0FF;  /* Slightly lighter on hover for subtle interactivity */\n"
"}")
        self.x_txtbox = QLineEdit(self.configFrame1)
        self.x_txtbox.setObjectName(u"x_txtbox")
        self.x_txtbox.setGeometry(QRect(130, 90, 141, 31))
        self.x_txtbox.setStyleSheet(u"#x_txtbox {\n"
"    border: 2px solid #5897FB;\n"
"    padding: 5px;\n"
"    background-color: #f5f5f5;\n"
"    color: #333;\n"
"	font-size: 17px;\n"
"}")
        self.x_txtbox.setAlignment(Qt.AlignCenter)
        self.y_txtbox = QLineEdit(self.configFrame1)
        self.y_txtbox.setObjectName(u"y_txtbox")
        self.y_txtbox.setGeometry(QRect(130, 140, 141, 31))
        self.y_txtbox.setStyleSheet(u"#y_txtbox {\n"
"    border: 2px solid #5897FB;\n"
"    padding: 5px;\n"
"    background-color: #f5f5f5;\n"
"    color: #333;\n"
"	font-size: 17px;\n"
"}")
        self.y_txtbox.setAlignment(Qt.AlignCenter)
        self.saveConfig_btn = QPushButton(self.configFrame1)
        self.saveConfig_btn.setObjectName(u"saveConfig_btn")
        self.saveConfig_btn.setGeometry(QRect(90, 220, 121, 41))
        self.saveConfig_btn.setStyleSheet(u"#saveConfig_btn {\n"
"    background-color: #0F52BA; /* More vibrant blue */\n"
"    color: white;\n"
"    font-size: 20px;\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#saveConfig_btn:hover {\n"
"    background-color: #357ABD; /* Deeper blue for hover */;\n"
"}")
        self.def_btn = QPushButton(self.Settings)
        self.def_btn.setObjectName(u"def_btn")
        self.def_btn.setGeometry(QRect(1110, 770, 221, 41))
        self.def_btn.setStyleSheet(u"#def_btn {\n"
"    background-color: #4A90E2; /* More vibrant blue */\n"
"    color: white;\n"
"    font-size: 15px;\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#def_btn:hover {\n"
"    background-color: #357ABD; /* Deeper blue for hover */;\n"
"}")
        self.stackedWidget.addWidget(self.Settings)
        self.export_page = QWidget()
        self.export_page.setObjectName(u"export_page")
        self.export_btn2 = QPushButton(self.export_page)
        self.export_btn2.setObjectName(u"export_btn2")
        self.export_btn2.setGeometry(QRect(1020, 120, 291, 51))
        self.export_btn2.setStyleSheet(u"#export_btn2{\n"
"    background-color: #5897FB; /* Default color */\n"
"    color: white;\n"
"	font-size: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"#export_btn2:hover{\n"
"	background-color: #2F6CDF;\n"
"}")
        self.export_tbl = QTableView(self.export_page)
        self.export_tbl.setObjectName(u"export_tbl")
        self.export_tbl.setGeometry(QRect(40, 200, 1271, 601))
        self.export_tbl.setLayoutDirection(Qt.LeftToRight)
        self.export_tbl.setStyleSheet(u"#export_tbl {\n"
"    background-color: white;\n"
"    color: black;\n"
"    font-size: 20px;\n"
" 	border: 1px solid white;\n"
"    selection-background-color: #5897FB;\n"
"    alternate-background-color:#dbe9f4;\n"
"}\n"
"\n"
"#export_tbl::item:selected {\n"
"    background-color: #a7c8fb;\n"
"}\n"
"\n"
"#export_tbl::QHeaderView::section {\n"
"    background-color:#2c2f40;  /* Dark navy blue for header */\n"
"    color: white;  /* White text */\n"
"    font-size: 14px;  /* Optional: Adjust font size */\n"
"    font-weight: bold;  /* Optional: Make text bold */\n"
"    padding: 5px;  /* Optional: Adjust padding */\n"
"    border: 1px solid #d3d3d3;  /* Border color for header */\n"
"}\n"
"")
        self.dateFilter_cbx = QComboBox(self.export_page)
        self.dateFilter_cbx.setObjectName(u"dateFilter_cbx")
        self.dateFilter_cbx.setGeometry(QRect(40, 141, 521, 41))
        self.dateFilter_cbx.setLayoutDirection(Qt.LeftToRight)
        self.dateFilter_cbx.setStyleSheet(u"#dateFilter_cbx {\n"
"    border: 2px solid #1D69E2;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 20px;\n"
"    font-family: 'Roboto', sans-serif;\n"
"    background-color: white;\n"
"    color: black;\n"
"}\n"
"\n"
"#dateFilter_cbx:hover {\n"
"    border: 2px solid transparent;\n"
"}\n"
"\n"
"#dateFilter_cbx:focus {\n"
"    border: 2px solid transparent;\n"
"    background-color: white;\n"
"}\n"
"\n"
"#dateFilter_cbx::drop-down {\n"
"    border-left: 1px solid transparent;\n"
"    background-color: white;\n"
"}\n"
"\n"
"#dateFilter_cbx QAbstractItemView {\n"
"    background-color: white;\n"
"    selection-background-color: #1D69E2;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"#dateFilter_cbx QAbstractItemView::item {\n"
"    padding: 10px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    font-family: 'Roboto', sans-serif;\n"
"    color: black;\n"
"}")
        self.label_3 = QLabel(self.export_page)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 30, 201, 31))
        self.label_3.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 30px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.label_8 = QLabel(self.export_page)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(40, 120, 261, 20))
        self.label_8.setStyleSheet(u"QLabel {\n"
"    font-family: \"Inter\"i;\n"
"    font-size: 15px; /* Adjust based on your UI scale */\n"
"    font-weight: bold;\n"
"    color: white;\n"
"    letter-spacing: 1px; /* Adjust for spacing */\n"
"    text-transform: uppercase; /* Makes text all caps */\n"
"}")
        self.stackedWidget.addWidget(self.export_page)
        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.raise_()
        self.nav_bar.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Visitor Monitoring System", None))
        self.menu_btn.setText("")
        self.dash_btn.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.cam_btn.setText(QCoreApplication.translate("MainWindow", u"Live Video Feed", None))
        self.logs_btn.setText(QCoreApplication.translate("MainWindow", u"Logs", None))
        self.settings_btn.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.logo_lbl.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.dateLabel1.setText(QCoreApplication.translate("MainWindow", u"Date: ", None))
        self.totalEntry1.setText(QCoreApplication.translate("MainWindow", u"Total Entry:", None))
        self.dateLabel2.setText(QCoreApplication.translate("MainWindow", u"Date: ", None))
        self.totalEntry2.setText(QCoreApplication.translate("MainWindow", u"Total Entry:", None))
        self.totalEntry3.setText(QCoreApplication.translate("MainWindow", u"Total Entry:", None))
        self.dateLabel3.setText(QCoreApplication.translate("MainWindow", u"Date: ", None))
        self.totalEntry4.setText(QCoreApplication.translate("MainWindow", u"Total Entry:", None))
        self.dateLabel4.setText(QCoreApplication.translate("MainWindow", u"Date: ", None))
        self.logsPrev.setText(QCoreApplication.translate("MainWindow", u"Logs for Today", None))
        self.label.setText("")
        self.stop_btn.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Live Video Feed", None))
        self.start_btn.setText("")
        self.cap_4.setText("")
        self.cap_5.setText("")
        self.cap_6.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Face Capture", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"LOGS", None))
        self.export_btn.setText(QCoreApplication.translate("MainWindow", u"Export  PDF", None))
        self.search_txt.setText("")
        self.search_txt.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.configLabel1.setText(QCoreApplication.translate("MainWindow", u"Tracking Point Settings", None))
        self.x_lbl.setText(QCoreApplication.translate("MainWindow", u"X Coordinate:", None))
        self.y_lbl.setText(QCoreApplication.translate("MainWindow", u"Y Coordinate:", None))
        self.x_txtbox.setText("")
        self.y_txtbox.setText("")
        self.saveConfig_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.def_btn.setText(QCoreApplication.translate("MainWindow", u"Restore Defaults", None))
        self.export_btn2.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"export pdf", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"available dates for export:", None))
    # retranslateUi

