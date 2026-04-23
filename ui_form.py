# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QHBoxLayout,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(878, 672)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widgetHeader = QWidget(self.centralwidget)
        self.widgetHeader.setObjectName(u"widgetHeader")
        self.widgetHeader.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widgetHeader)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchBox_2 = QLineEdit(self.widgetHeader)
        self.searchBox_2.setObjectName(u"searchBox_2")

        self.horizontalLayout.addWidget(self.searchBox_2)

        self.searchButton = QPushButton(self.widgetHeader)
        self.searchButton.setObjectName(u"searchButton")

        self.horizontalLayout.addWidget(self.searchButton)

        self.horizontalSpacer = QSpacerItem(241, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalSlider = QSlider(self.widgetHeader)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider)


        self.verticalLayout.addWidget(self.widgetHeader)

        self.widgetMain = QWidget(self.centralwidget)
        self.widgetMain.setObjectName(u"widgetMain")
        self.horizontalLayout_2 = QHBoxLayout(self.widgetMain)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.listWidget = QListWidget(self.widgetMain)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.ArrowCursor))
        self.listWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.listWidget.setProperty(u"showDropIndicator", False)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.listWidget.setIconSize(QSize(256, 256))
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.listWidget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.listWidget.setMovement(QListView.Movement.Static)
        self.listWidget.setFlow(QListView.Flow.LeftToRight)
        self.listWidget.setResizeMode(QListView.ResizeMode.Adjust)
        self.listWidget.setGridSize(QSize(300, 300))
        self.listWidget.setViewMode(QListView.ViewMode.IconMode)
        self.listWidget.setItemAlignment(Qt.AlignmentFlag.AlignTop)

        self.horizontalLayout_2.addWidget(self.listWidget)


        self.verticalLayout.addWidget(self.widgetMain)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BooruExplorer", None))
        self.searchBox_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u0422\u0435\u0433\u0438", None))
        self.searchButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
#if QT_CONFIG(statustip)
        self.statusbar.setStatusTip("")
#endif // QT_CONFIG(statustip)
    # retranslateUi

