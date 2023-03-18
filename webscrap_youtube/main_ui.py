from PyQt5 import QtCore, QtGui, QtWidgets
from main import *
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(764, 500)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 1200))
        
        self.threadcount = 1;
        
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        
        self.textEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.textEdit.setObjectName("textEdit")
        
        
        
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.horizontalLayout_2.addWidget(self.textEdit)
        
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.horizontalSlider = QtWidgets.QSlider(self.centralWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout.addWidget(self.horizontalSlider)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        
      
        
        
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralWidget)
        
        
       
        # proxies list--------------------
        
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_4.addWidget(self.listWidget)
        
        # yturls list -----------------------
        
        self.listView_url = QtWidgets.QListWidget(self.centralWidget)
        self.listView_url.setObjectName("listwidget_url")
        self.horizontalLayout_4.addWidget(self.listView_url)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_5.clicked.connect(self.addProxies)
        self.pushButton_5.clicked.connect(self.addUrls)
        self.pushButton_3.clicked.connect(self.startScape)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_5.setText(_translate("MainWindow", "Load"))
        self.pushButton_3.setText(_translate("MainWindow", "Start scraping"))
        

    def addProxies(self):
        self.threadcount = int(self.textEdit.text())
        print (self.threadcount)
        with open('proxies.txt', 'r') as movieDir:
            cnt = 0
            for row in movieDir:
                cnt += 1
                if cnt <= self.threadcount:
                    self.listWidget.addItem(row)
                else :break
    def addUrls(self):
        
        self.threadcount = int(self.textEdit.text())  
        with open('urls.txt', 'r') as movieDir:  
            cnt = 0
            for row in movieDir:
                cnt += 1
                if cnt <= self.threadcount:
                    self.listView_url.addItem(row)
                else :break
    def startScape(self):
        urlsName = "yturls.txt"
        proxiesName = "proxies.txt"
        filter = Filter()
        proxies =filter.parse_proxies(proxiesFile=proxiesName)
        urls = filter.filtrate_urls(urlsFile=urlsName)
        timeout = float(100)
        
        start_threads(proxies=proxies, urls=urls, amountThreads=self.threadcount, timeout=timeout)
        delimiter = ","
        saver = Saver(delimiter=delimiter)
        saver.save_data_to_csv()
        saver.save_to_json()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())