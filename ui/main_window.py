# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1132, 878)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.columnView = QtWidgets.QColumnView(self.splitter)
        self.columnView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.columnView.sizePolicy().hasHeightForWidth())
        self.columnView.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.columnView.setFont(font)
        self.columnView.setMouseTracking(False)
        self.columnView.setStyleSheet("")
        self.columnView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.columnView.setObjectName("columnView")
        self.tableView = QtWidgets.QTableView(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setMinimumSectionSize(30)
        self.tableView.verticalHeader().setMinimumSectionSize(30)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1132, 26))
        self.menubar.setObjectName("menubar")
        self.menu_L = QtWidgets.QMenu(self.menubar)
        self.menu_L.setObjectName("menu_L")
        self.menu_D = QtWidgets.QMenu(self.menubar)
        self.menu_D.setObjectName("menu_D")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_refresh = QtWidgets.QAction(MainWindow)
        self.action_refresh.setObjectName("action_refresh")
        self.action_openfolder = QtWidgets.QAction(MainWindow)
        self.action_openfolder.setObjectName("action_openfolder")
        self.action_win_explorer_open = QtWidgets.QAction(MainWindow)
        self.action_win_explorer_open.setObjectName("action_win_explorer_open")
        self.action_sort = QtWidgets.QAction(MainWindow)
        self.action_sort.setObjectName("action_sort")
        self.action_detail = QtWidgets.QAction(MainWindow)
        self.action_detail.setObjectName("action_detail")
        self.menu_L.addAction(self.action_refresh)
        self.menu_L.addAction(self.action_openfolder)
        self.menu_L.addAction(self.action_win_explorer_open)
        self.menu_D.addAction(self.action_detail)
        self.menubar.addAction(self.menu_L.menuAction())
        self.menubar.addAction(self.menu_D.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_L.setTitle(_translate("MainWindow", "本地(&L)"))
        self.menu_D.setTitle(_translate("MainWindow", "显示(&D)"))
        self.action_refresh.setText(_translate("MainWindow", "刷新(&R)"))
        self.action_refresh.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.action_openfolder.setText(_translate("MainWindow", "打开(&O)"))
        self.action_openfolder.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.action_win_explorer_open.setText(_translate("MainWindow", "外部打开(&E)"))
        self.action_win_explorer_open.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.action_sort.setText(_translate("MainWindow", "排序(&S)"))
        self.action_sort.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_detail.setText(_translate("MainWindow", "文件详情(&D)"))
        self.action_detail.setShortcut(_translate("MainWindow", "Ctrl+D"))
