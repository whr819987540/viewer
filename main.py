import re
import sys

from PyQt5.QtCore import Qt, QUrl, QModelIndex, QSize
from PyQt5.QtGui import (QCursor, QDesktopServices, QIcon, QStandardItem,
                         QStandardItemModel, QPainter, QPen)
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
                             QFileDialog, QFileSystemModel, QMainWindow, QMenu,
                             QMessageBox, QWidget, QTableWidgetItem, QAbstractItemDelegate, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QHeaderView, QSystemTrayIcon, qApp)

import file_func
from ui.main_window import Ui_MainWindow
from ui.test import Ui_Form


class SystemTray(QSystemTrayIcon):
    """
        系统托盘
        功能:
            1、 系统托盘菜单栏(显示、退出主程序)
            2、 所有窗口关闭后程序不退出(可通过托盘查看)
    """

    def __init__(self, parent) -> None:
        super(SystemTray, self).__init__(parent)
        self.parent = parent

        self.tray = QSystemTrayIcon(parent)
        self.tray.setToolTip("Viewer")
        self.tray.setIcon(QIcon("./resource/icon.png"))
        # 点击托盘事件
        self.tray.activated.connect(self.onIconClicked)
        # 托盘菜单栏
        self.create_tray_menu()

        self.tray.show()  # 显示系统托盘

    def create_tray_menu(self):
        # 系统托盘菜单栏
        self.tray_menu = QMenu()

        self.action_display = QAction("启动", self.parent, triggered=self.dispaly)
        # self.action_display.setShortcut("CTRL+ALT+S")
        self.tray_menu.addAction(self.action_display)

        self.tray_menu.addSeparator()

        self.action_quit = QAction("退出", self.parent, triggered=self.quit)
        # self.action_quit.setShortcut("CTRL+ALT+Q")
        self.tray_menu.addAction(self.action_quit)

        self.tray.setContextMenu(self.tray_menu)

    def onIconClicked(self, reason):
        """
            系统图盘图标点击事件
        """
        # Unknown = ... # type: QSystemTrayIcon.ActivationReason
        # Context = ... # type: QSystemTrayIcon.ActivationReason # 右键单击
        # DoubleClick = ... # type: QSystemTrayIcon.ActivationReason # 左键双击
        # Trigger = ... # type: QSystemTrayIcon.ActivationReason # 左键单击
        # MiddleClick = ... # type: QSystemTrayIcon.ActivationReason # 中键
        if reason == QSystemTrayIcon.ActivationReason.Context:
            self.tray_menu.show()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick or reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.dispaly()
        else:
            pass

    def dispaly(self):
        """
            显示主程序
        """
        self.parent.showNormal()
        self.parent.activateWindow()

    def quit(self):
        """
            退出主程序
        """
        qApp.quit()


class Delegate(QStyledItemDelegate):
    """
        绘制右侧表格的垂直网格线
    """

    def __init__(self, parent) -> None:
        super(Delegate, self).__init__()
        # gridHint = parent.style().styleHint(
        #     QStyle.StyleHint.SH_Table_GridLineColor,
        #     QStyleOptionViewItem()
        # )
        # gridColor = gridHint
        self.pen = QPen(parent.gridStyle())
        # self.pen = QPen(gridColor, 0, parent.gridStyle())
        self.view = parent

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        QStyledItemDelegate().paint(painter, option, index)
        oldPen = painter.pen()
        painter.setPen(self.pen)
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())  # 显示垂直网格线
        painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        # painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())# 显示水平网格线

        # 字体
        # font = QFont()
        # font.setFamily('微软雅黑')
        # font.setPointSize(20)
        # font.setPixelSize(20)
        # painter.setFont(font)

        painter.setPen(oldPen)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init()
        self.tray = SystemTray(self)

    def init(self):
        """
            初始化函数
        """
        QFileSystemModel.Option()
        self.create_menu()
        self.create_rightmenu()  # 只执行一次（初始化时）
        self.column_view_init()
        self.table_view_init()

        self.display_init()

    def display_init(self):
        """
            显示配置
        """
        # 主窗口
        self.setWindowTitle("Viewer")
        self.setWindowIcon(QIcon("./resource/64.ico"))

        # 预览水平分裂器位置
        self.ui.splitter.setOpaqueResize(False)

        # 列视图不可编辑
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def create_menu(self):
        """
            点击顶部菜单栏出现菜单, 初始化
        """
        # 刷新
        self.ui.action_refresh.triggered.connect(self.refresh_view)
        # 选择本地文件夹
        self.ui.action_openfolder.triggered.connect(self.open_local_folder)
        # win explorer打开文件夹
        self.ui.action_win_explorer_open.triggered.connect(self.open_win_explorer)
        # 显示文件详情
        self.ui.action_detail.triggered.connect(self.show_tableWidgetdetail)

    def show_tableWidgetdetail(self):
        """
            隐藏详情栏或显示详情栏
        """
        # if self.ui.tableView.isHidden():
        #     self.ui.tableView.show()
        # else:
        #     self.ui.tableView.hide()
        self.ui.tableView.setVisible(not self.ui.tableView.isVisible())
        # self.ui.tableWidget.setVisible(not self.ui.tableWidget.isVisible())

    def open_local_folder(self):
        """
            打开本地文件夹, 并修改column view, 然后显示文件详情
        """
        folder_abs_path = QFileDialog.getExistingDirectory(self, "打开文件夹")
        index = self.model.index(folder_abs_path)

        # 打开本地文件夹时，无法显示文件详情
        self.ui.columnView.setCurrentIndex(index)
        self.display_file_detail(index)

    def table_view_init(self):
        """
            右侧表格视图初始化:
            将右侧视图的点击效果关联到左侧视图
        """
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # self.ui.tableView.clicked.connect(self.click_tableView)
        self.ui.tableView.doubleClicked.connect(self.doubleClick_tableView)
        self.ui.tableView.verticalScrollBar().valueChanged.connect(self.sync_columnView_scrollBar) # 右侧视图竖直滚动条移动

    def tableView_to_columnView(self):
        """
            右侧视图到左侧视图的index映射
        """
        row = self.ui.tableView.currentIndex().row()

        current_index = self.ui.columnView.currentIndex()

        index = current_index.child(row, 0)
        # current_index可能指向文件, 并没有child
        # 此时应该找其父结点
        if index.data() == None:
            index = current_index.parent().child(row, 0)

        return index

    def click_tableView(self):
        """
            单击右侧表格视图
        """
        # index = self.tableView_to_columnView()
        # self.ui.columnView.setCurrentIndex(index)
        # self.display_file_detail(index)

    def doubleClick_tableView(self):
        """
            双击右侧表格视图
        """
        index = self.tableView_to_columnView()
        abs_path = self.model.filePath(index)

        while True:
            file_type = file_func.get_file_type(abs_path)

            if file_type == file_func.FileType.Dir: # 目录, 右侧选中, 左侧显示详情
                print("dir")
                self.ui.columnView.setCurrentIndex(index)
                self.display_file_detail(index)
                break
            elif file_type == file_func.FileType.File: # 文件, 右侧选中, 默认程序打开
                self.open_file(index)
                self.ui.columnView.setCurrentIndex(index)
                break
            else: # 快捷方式, 找到真正指向的位置, 右侧选中并打开, 左侧显示详情
                abs_path = file_func.get_lnk_file_abs_path(abs_path)
                index = self.model.index(abs_path)
                continue
            
    def column_view_init(self):
        """
            列视图初始化
            采用文件系统数据模型: 不用在底层用os.path逐一分析目录结构
        """
        # 数据model(内置)
        self.model = QFileSystemModel()
        # 不解析链接文件, 否则无法判断文件类型
        self.model.setOptions(QFileSystemModel.Option.DontResolveSymlinks)
        # 第一个盘符
        self.model.setRootPath(file_func.get_all_drive_letters()[0])

        self.ui.columnView.setModel(self.model)
        # 禁止修改
        self.ui.columnView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 事件绑定
        self.ui.columnView.doubleClicked.connect(self.open_file)  # 双击
        self.ui.columnView.clicked.connect(self.display_file_detail) # 单击
        self.ui.columnView.verticalScrollBar().valueChanged.connect(self.sync_columnView_scrollBar)

    def display_file_detail(self, index):
        """
            显示当前点击对象的详情(文件夹)或所在文件夹的详情(文件)
        """
        if not self.model.isDir(index):
            # 如果是文件，需要找到父目录, 然后显示父目录的详情
            self.display_file_detail(index.parent())
            print("not dir")
            return

        # 如果是文件夹，直接更新
        # 设置模型
        detail_model = QStandardItemModel(self)
        detail_model.setColumnCount(3)
        self.ui.tableView.setModel(detail_model)

        # 行列标题
        self.ui.tableView.verticalHeader().setVisible(False)  # 不显示行号
        self.ui.tableView.horizontalHeader().setVisible(False)  # 不显示列标题
        self.ui.tableView.setShowGrid(False)  # 不显示网格线
        self.ui.tableView.setItemDelegate(Delegate(self.ui.tableView))  # 只显示竖直网格线

        # 固定行高
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.ui.tableView.verticalHeader().setMinimumSectionSize(0)  # 最小设置为0, 防止与默认值冲突
        self.ui.tableView.verticalHeader().setDefaultSectionSize(20)  # 默认设置为20（刚好与左侧对齐）

        # 列宽
        # 第一列：Interactive
        #   可能很长所以缩略显示, 默认值为defaultSectionSize
        # self.ui.tableView.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeMode.Interactive)

        # 第二、三列：长度固定，通过sizeHint进行调节
        # 如果设置了sizeHint, 在sizeHint与minimumSectionSize之间取最大值
        # 否则通过单元格内容进行计算
        # self.ui.tableView.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeMode.ResizeToContents)
        # self.ui.tableView.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)  # 3 ResizeToContents
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)  # 0 Interactive
        # print( self.ui.tableView.horizontalHeader().sectionResizeMode(0),QHeaderView.ResizeMode.Interactive) # 0 0
        # print( self.ui.tableView.horizontalHeader().sectionResizeMode(1),QHeaderView.ResizeMode.ResizeToContents) # 3 3
        # print( self.ui.tableView.horizontalHeader().sectionResizeMode(2),QHeaderView.ResizeMode.ResizeToContents) # 3 3

        # # 第二列列宽固定
        # self.ui.tableView.horizontalHeader().setMinimumSectionSize(20) # 默认设置为20（刚好与左侧对齐）
        # self.ui.tableView.horizontalHeader().setDefaultSectionSize(160) # 默认设置为100（刚好与左侧对齐）
        # # self.ui.tableView.setColumnWidth(1,200) # 列宽
        # # 第三列列宽固定
        # # self.ui.tableView.setColumnWidth(1,20) # 列宽

        # self.ui.tableView.horizontalHeader().setMinimumSectionSize(20) # 最小设置为20, 防止不可见
        # self.ui.tableView.setColumnWidth(1,60)
        # self.ui.tableView.verticalHeader().setLineWidth(40)
        # self.ui.tableView.resizeColumnToContents(1)

        # self.ui.tableView.setRowHeight(1, 40)
        # self.ui.tableView.setColumnWidth(1, 160)

        # 清空原始数据
        detail_model.setRowCount(0)
        detail_model.clear()

        row = 0
        child = index.child(row, 0)
        # print(self.model.fileInfo(child))
        while child.data() != None:
            filename, date, size = self.get_file_info(child)

            row += 1
            child = index.child(row, 0)

            # self.ui.tableView.setRowCount(row)
            detail_model.setItem(row-1, 0, QStandardItem(filename))
            # detail_model.item(row-1,0).setSizeHint(QSize(100,20))

            detail_model.setItem(row-1, 1, QStandardItem(date))
            detail_model.item(row-1, 1).setSizeHint(QSize(180, 20))
            detail_model.item(row-1, 1).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)

            detail_model.setItem(row-1, 2, QStandardItem(size))
            detail_model.item(row-1, 2).setSizeHint(QSize(90, 20))
            detail_model.item(row-1, 2).setTextAlignment(Qt.AlignmentFlag.AlignHCenter)

            # self.ui.tableView.setItem(row-1,0,QTableWidgetItem(filename))
            # self.ui.tableView.setItem(row-1,1,QTableWidgetItem(date))
            # self.ui.tableView.setItem(row-1,2,QTableWidgetItem(size))

    def create_rightmenu(self):
        """
            右击centralwidget出现菜单, 初始化
        """
        print('create_rightmenu')

        self.ui.centralwidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # 绑定的create_right_menu_func在每次右击时都会被执行
        self.ui.centralwidget.customContextMenuRequested.connect(self.create_right_menu_func)

    def create_right_menu_func(self):
        print('create_right_menu_func')

        # 右击也需要首选刷新文件夹详情
        index = self.ui.columnView.currentIndex()
        self.display_file_detail(index)

        self.groupBox_menu = QMenu(self)
        # 刷新
        # 此处添加快捷键无用，需要和菜单或按钮绑定，通过菜单或按钮触发
        action_refresh = QAction(self)
        action_refresh.setText(QApplication.translate("MainWindow", "刷新(&R)"))
        action_refresh.setShortcut("Ctrl+R")
        action_refresh.triggered.connect(self.refresh_view)
        self.groupBox_menu.addAction(action_refresh)

        # windows explorer打开文件夹
        action_win_explorer_open = QAction(self)
        action_win_explorer_open.setText(QApplication.translate("MainWindow", "外部打开(&E)"))
        action_win_explorer_open.setShortcut("Ctrl+E")
        action_win_explorer_open.triggered.connect(self.open_win_explorer)
        self.groupBox_menu.addAction(action_win_explorer_open)

        self.groupBox_menu.popup(QCursor.pos())  # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以

    def open_win_explorer(self, index):
        """
            用windows explorer打开文件夹
            首先获取当前文件的绝对路径
            然后判断文件类型
        """
        index = self.ui.columnView.currentIndex()
        if index.data() == None:
            # 未选中文件夹或文件
            QMessageBox.critical(
                self, "error", "未选中文件或文件夹",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
        else:
            abs_path = self.model.filePath(index)
            while True:
                type = file_func.get_file_type(abs_path)
                if type == file_func.FileType.File or type == file_func.FileType.Dir:
                    # 文件/目录, 默认软件直接打开
                    QDesktopServices.openUrl(QUrl.fromLocalFile(abs_path))
                    break
                else:
                    # 链接文件, 首先获得指向的绝对路径
                    # 该路径仍然可能是链接文件
                    abs_path = file_func.get_lnk_file_abs_path(abs_path)
                    continue
            print("外部打开", abs_path)

    def refresh_view(self):
        """
            刷新column view, 即文件
            刷新样式表, resource/style.qss
        """
        print("refresh")

        index = self.ui.columnView.currentIndex()
        self.display_file_detail(index)

        self.set_stylesheet()

    def open_file(self, item):
        """
            双击触发
            判断类型:
                文件, 打开
                链接文件, 获取实际指向的路径
                目录, 跳过
        """
        row, column, data = item.row(), item.column(), item.data()
        # print(row, column, data, dir(item), item.parent(), item.parent().data())

        # 获取该文件的绝对路径
        abs_path = self.model.filePath(item)  # 内置的api
        # abs_path = self.get_abs_path_from_fs(item) # 自己的api

        # 判断文件类型
        file_type = file_func.get_file_type(abs_path)
        if file_type == file_func.FileType.File:
            # 以系统默认应用打开该文件
            QDesktopServices.openUrl(QUrl.fromLocalFile(abs_path))
            print('open', QUrl.fromLocalFile(abs_path))  # file:///{path}
        elif file_type == file_func.FileType.Dir:
            print('pass')
            pass
        else:
            while file_type == file_func.FileType.Link:
                abs_path = file_func.get_lnk_file_abs_path(abs_path)
                file_type = file_func.get_file_type(abs_path)
            print('link', abs_path)
            # 点击链接文件, 进行跳转
            # 先根据路径找到索引, 再修改GUI
            self.ui.columnView.setCurrentIndex(self.model.index(abs_path))

        print(row, column, data, abs_path)

    def sync_columnView_scrollBar(self):
        """
            将右侧视图的滚动条同步到左侧
        """
        left_bar = self.ui.columnView.verticalScrollBar()
        right_bar = self.ui.tableView.verticalScrollBar()
        print('before',left_bar.value(),right_bar.value())
        left_bar.setValue(right_bar.value())
        print('after',left_bar.value(),right_bar.value())

    def sync_tableView_scrollBar(self):
        """
            将左侧视图的滚动条同步到右侧
        """
        left_bar = self.ui.columnView.verticalScrollBar()
        right_bar = self.ui.tableView.verticalScrollBar()
        print('before',left_bar.value(),right_bar.value())
        right_bar.setValue(left_bar.value())
        print('after',left_bar.value(),right_bar.value())


    def get_file_info(self, index):
        """
            获取某个文件的详情(文件名, 最近修改时间, 大小)
        """
        fileinfo = self.model.fileInfo(index)
        filename = fileinfo.fileName()
        last_modify_date = fileinfo.lastModified().toString("yyyy/MM/dd hh:mm:ss")
        # size = file_func.size_unit_int_to_str(file_func.get_size(fileinfo.path())) # 弃用, 太慢
        size = file_func.size_unit_int_to_str(fileinfo.size())
        return filename, last_modify_date, size

    def get_abs_path_from_fs(self, item):
        print("first", self.model.filePath(item), self.model.type(item))
        # print(self.model.setRootPath())

        """
            获取文件的绝对路径
        """
        res = []
        while not self.is_drive_letter(item):
            # print(item.data())
            res.append(item.data())
            item = item.parent()
        res.append(self.get_drive_letter_from_fs(item))
        res.reverse()  # 从下往上遍历, 所以应该倒置list
        # print(file_func.path_join(res))
        return file_func.path_join(res)

    def get_drive_letter_from_fs(self, item):
        """
            文件系统数据模型中, 盘符的格式为 本地磁盘/新加卷 ({ALPHA}:)
            本函数用来提取ALPHA
        """
        return re.findall('.*?\(([a-zA-Z]):\)', item.data())[0] + ":/"

    def is_drive_letter(self, item):
        """
            判断一个结点是否是盘符
            特征为parent().data()为None
        """
        return item.parent().data() == None

    def view_menu(self):
        """
            右击触发
        """
        print("view_menu")
    # 第一个版本(弃用)
    # def init(self):
    #     """
    #         初始化函数
    #     """
    #     self.load_const()
    #     self.column_view_init()

    # def load_const(self):
    #     """
    #         常量定义/加载
    #     """
    #     self.model = self.create_model()
    #     self.drive_letters = file_func.get_all_drive_letters()

    # def column_view_init(self):
    #     """
    #         列视图初始化
    #     """
    #     # 列视图属性模型设置
    #     self.ui.columnView.setModel(self.model)
    #     # 列视图不可编辑
    #     self.ui.columnView.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     # 双击某个item
    #     self.ui.columnView.doubleClicked.connect(self.click_model_item)
    #     # 显示盘符
    #     self.column_display(self.drive_letters, 0)
    #     self.column_display(self.drive_letters, 1)

    # def create_model(self):
    #     return QStandardItemModel()

    # def create_model_item(self, item=None):
    #     return QStandardItem(item)

    # def click_model_item(self, index):
    #     """
    #         点击某个文件夹, 在下一列显示目录下的内容
    #     """
    #     # # index的方法
    #     # print(dir(index), index.row(), index.column(), index.data())
    #     # # 设置表格中某个位置的
    #     # print(self.model.setItem(2, 0, self.create_model_item("yew")))

    #     row, column, data = index.row(), index.column(), index.data()
    #     print(self.get_abs_path_from_column_view(row, column, data))
    #     abs_path = self.get_abs_path_from_column_view(row, column, data)
    #     print("abs_path", abs_path)
    #     dirs, files = file_func.list_dir(abs_path)
    #     dirs = sorted(dirs)
    #     files = sorted(files)
    #     print(dirs, files)
    #     self.column_display(dirs+files, column+1)

    # def column_display(self, items, column):
    #     """
    #         以列为单位进行显示
    #     """
    #     for index, item in enumerate(items):
    #         print(index, column, item)
    #         self.model.setRowCount(self.model.rowCount()+1)
    #         self.model.setItem(index, column, self.create_model_item(item))

    # def get_abs_path_from_column_view(self, row, column, path):
    #     """
    #         从[row,column]向前遍历, 返回对应目录的绝对路径
    #     """
    #     res = []
    #     for c in range(0, column):
    #         res.append(self.model.item(row, c).data())
    #     return os_path_join(file_func.path_join(res), path)


class mainWin(QWidget, Ui_Form):
    def __init__(self):
        super(mainWin, self).__init__()
        self.setupUi(self)
        self.model = QFileSystemModel()
        self.model.setRootPath("c:/")
        self.columnView.setModel(self.model)


if __name__ == "__main__":
    import os
    res = os.popen("python ./export_ui_to_py.py")
    for line in res.readlines():
        print(line)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 全部窗口关闭后程序不退出

    main_window = MainWindow()
    # main_window = mainWin()

    main_window.show()

    sys.exit(app.exec_())
