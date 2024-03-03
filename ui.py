from run_request import SchoolActivityClient

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, \
    QProgressBar, QLabel, QVBoxLayout, QListView, QLineEdit, QMenuBar, \
    QStatusBar, QGridLayout, QHBoxLayout, QTextEdit, QMessageBox, QRadioButton, QButtonGroup, QGroupBox
from PyQt6.QtCore import QRect, QCoreApplication, Qt
from button_func import add_user_to_json, delete_selected_users, select_all_items
from button_func import refresh_list_view,load_selected_users
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon

from PyQt6.QtCore import QThread, pyqtSignal, QObject

# 定义一个用于执行耗时任务的Worker类
class Worker(QObject):
    finished = pyqtSignal(list)  # 处理完成后发射的信号，携带处理结果
    progressUpdated = pyqtSignal(int)  # 新增：发射进度更新信号
    def __init__(self, users, schoolsite, filepath, parent=None):
        super(Worker, self).__init__(parent)
        self.users = users
        self.schoolsite = schoolsite
        self.filepath = filepath

    def run(self):
        results = []
        total = len(self.users)
        for index, user in enumerate(self.users):
            try:
                phone, password = user.get('user_id'), user.get('password')
                client = SchoolActivityClient(phone=phone, password=password)
                client.login()
                result = client.create_and_send_record(school_site=self.schoolsite,file_path=self.filepath)

                try:
                    results.append({'phone':phone,'result':result['response']['resultDesc']})
                except:
                    results.append({'phone':phone,'result':result})

            except Exception as e:
                results.append({'phone':phone,'result':'账号错误'})
            progress = int((index + 1) / total * 100)  # 计算完成的百分比
            self.progressUpdated.emit(progress)  # 发射进度更新信号

        self.finished.emit(results)  # 发射信号，通知主线程处理完成




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 429)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 创建一个水平布局来包含 QVBoxLayout 和 QGridLayout
        self.horizontalLayout = QHBoxLayout(self.centralwidget)

        # 创建 QVBoxLayout 并添加控件
        self.verticalLayout = QVBoxLayout()
        self.listView = QListView()
        self.verticalLayout.addWidget(self.listView)

        #初始化listview
        self.initialize_listView()

        self.buttonsLayout = QHBoxLayout()
        self.selectAllButton = QPushButton("全选")
        self.buttonsLayout.addWidget(self.selectAllButton)
        self.deleteButton = QPushButton("删除")
        self.buttonsLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.buttonsLayout)



        self.label_2 = QLabel("账号")
        self.verticalLayout.addWidget(self.label_2)
        self.user_id = QLineEdit()
        self.verticalLayout.addWidget(self.user_id)
        self.label_3 = QLabel("密码")
        self.verticalLayout.addWidget(self.label_3)
        self.password = QLineEdit()
        self.verticalLayout.addWidget(self.password)
        self.add_user = QPushButton("添加用户")
        self.verticalLayout.addWidget(self.add_user)


        # 将 QVBoxLayout 添加到水平布局中
        self.horizontalLayout.addLayout(self.verticalLayout, 1)  # 参数 1 表示这部分布局占用的比例


        self.hkgRadioButton = QRadioButton("航空港(或者其他学校第一个校区)")
        self.lqRadioButton = QRadioButton("龙泉(或者其他学校第二个校区)")
        self.hkgRadioButton.setChecked(True)  # 默认选中hkg

        # 创建 QGroupBox 作为容器
        self.radioGroupBox = QGroupBox()
        self.radioLayout = QVBoxLayout()  # 使用 QVBoxLayout 管理单选按钮

        # 将单选按钮添加到 QVBoxLayout 中
        self.radioLayout.addWidget(self.hkgRadioButton)
        self.radioLayout.addWidget(self.lqRadioButton)

        # 设置 QGroupBox 的布局
        self.radioGroupBox.setLayout(self.radioLayout)




        # 创建 QGridLayout 并添加控件
        self.gridLayout = QGridLayout()

        self.sign_out = QPushButton("签到/签退")
        self.gridLayout.addWidget(self.sign_out,3, 0, 1,1)
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 1)

        self.runstart = QPushButton("跑步")
        self.gridLayout.addWidget(self.runstart, 2, 0, 1, 1)

        self.gridLayout.addWidget(self.radioGroupBox, 1, 0, 1, 1)


        self.result = QTextEdit("输出结果")
        self.result.setReadOnly(True)
        self.gridLayout.addWidget(self.result, 0, 0, 1, 1)

        # 将 QGridLayout 添加到水平布局中
        self.horizontalLayout.addLayout(self.gridLayout, 2)  # 参数 2 表示这部分布局占用的比例

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QCoreApplication.processEvents()

        # 设置事件监听
        self.setupEventListeners()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "跑步", None))


    def initialize_listView(self):
        # 这里填充您的listView初始化代码
        refresh_list_view(self.listView)

    def setupEventListeners(self):
        # 设置按钮的点击事件
        self.selectAllButton.clicked.connect(lambda: select_all_items(self.listView))
        self.deleteButton.clicked.connect(lambda: delete_selected_users(self.listView))
        self.add_user.clicked.connect(
            lambda: add_user_to_json(self.user_id.text(), self.password.text(), self.listView))

        self.runstart.clicked.connect(self.run_start_action)
        self.sign_out.clicked.connect(self.sign_out_action)


    def sign_out_action(self):
        QMessageBox.information(None, "提示", "还未开发")


    def run_start_action(self):
        # 这里是 runstart 按钮点击后的动作代码

        users =load_selected_users(self.listView)
        if not users:  # 如果 users 列表为空
            # 显示一个信息框提示"未选中用户"
            QMessageBox.information(None, "提示", "未选中用户")
            return  # 结束函数执行
        else:
            QMessageBox.information(None, "提示", "已经开始，请勿重复")
            # 创建Worker对象并移动到子线程
        schoolsite = 0
        filepath = "map_cuit_hkg.json"
        if self.hkgRadioButton.isChecked():
            schoolsite = 0
            filepath = "map_cuit_hkg.json"
        elif self.lqRadioButton.isChecked():
            schoolsite = 1
            filepath = "map_cuit_lq.json"

        self.thread = QThread()  # 创建一个QThread实例
        self.worker = Worker(users, schoolsite, filepath)
        self.worker.moveToThread(self.thread)  # 将worker移动到子线程
        self.thread.started.connect(self.worker.run)  # 线程开始时，执行worker的run方法
        self.worker.finished.connect(self.process_users_finished)  # 处理完成后的信号连接到处理方法
        self.worker.progressUpdated.connect(self.updateProgressBar)
        self.worker.finished.connect(self.process_users_finished)
        self.worker.finished.connect(self.thread.quit)  # 处理完成后结束线程
        self.worker.finished.connect(self.worker.deleteLater)  # 清理worker对象
        self.thread.finished.connect(self.thread.deleteLater)  # 清理线程对象
        self.thread.start()  # 开始线程，执行任务

    def updateProgressBar(self, value):
        self.progressBar.setValue(value)  # 更新进度条的值

    def process_users_finished(self, results):
        # 格式化结果为字符串列表
        formatted_results = [f"{result['phone']}: {result['result']}" for result in results if isinstance(result, dict)]
        # 更新UI显示结果
        self.result.setPlainText("\n".join(formatted_results))




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QIcon('run.ico'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

