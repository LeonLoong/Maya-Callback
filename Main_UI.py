from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, os, qdarkstyle
import xml.etree.ElementTree as xml

### define path
global_directory = (r"A:\Demo\Global")
local_directory = os.path.join('C:', os.path.expanduser('~'), 'Demo_Main')

global_dataDirectory = (r"{}\{}".format(global_directory, "Data"))
global_userInfo = (r"{}\Demo_Main\User_Info.xml".format(global_dataDirectory))

local_dataDirectory = (r"{}\{}".format(local_directory, "Data"))
local_userInfo = (r"{}\User_Info.xml".format(local_dataDirectory))

global_launcherDirectory = ("{}\{}".format(global_directory, "Launcher"))
global_launcher = ("{}\Demo_Main\Maya.bat".format(global_launcherDirectory))

local_launcherDirectory = ("{}\{}".format(local_directory, "Launcher"))
local_launcher = ("{}\Maya.bat".format(local_launcherDirectory))

### function
def copy_File(src, dst):
    from shutil import copyfile
    copyfile(src, dst)

def create_Demo():
    if not os.path.isfile(local_userInfo):
        if not os.path.exists(local_dataDirectory):
            os.makedirs(local_dataDirectory)
            copy_File((global_userInfo), (local_userInfo))
            print ("Data Copied")

    if not os.path.isfile(local_launcher):
        if not os.path.exists(local_launcherDirectory):
            os.makedirs(local_launcherDirectory)
            copy_File((global_launcher), (local_launcher))
            print ("Launcher Copied")

create_Demo()

from Launcher import Demo_LAUNCHER

global_projectInfo_dataPath = (r"{}\Data\Demo_Main\Project_Info.xml".format(global_directory))
global_projectInfo_dataTree = xml.parse(global_projectInfo_dataPath)
global_projectInfo_dataRoot = global_projectInfo_dataTree.getroot()

global_userInfo_dataPath = (r"{}\Data\Demo_Main\User_Info.xml").format(global_directory)
global_userInfo_dataTree = xml.parse(global_userInfo_dataPath)
global_userInfo_dataRoot = global_userInfo_dataTree.getroot()

local_userInfo_dataPath = (r"{}\Data\User_Info.xml").format(local_directory)
local_userInfo_dataTree = xml.parse(local_userInfo_dataPath)
local_userInfo_dataRoot = local_userInfo_dataTree.getroot()

global_UI_dataPath = (r"{}\Data\Demo_Main\UI_Info.xml".format(global_directory))
global_UI_dataTree = xml.parse(global_UI_dataPath)
global_UI_dataRoot = global_UI_dataTree.getroot()

def get_global_userInfo():
    for global_userInfo in global_userInfo_dataRoot:
        for userInfo in global_userInfo:
            version = userInfo.attrib["VERSION"]
            return version

global_userInfo_version = get_global_userInfo()

def get_local_userInfo():
    for local_userInfo in local_userInfo_dataRoot:
        for userInfo in local_userInfo:
            version = userInfo.attrib["VERSION"]
            username = userInfo.find("Username").text
            department = userInfo.find("Department").text
            projectName = userInfo.find("Project").text
            softwareName = [software for software in userInfo.findall("Software")][0].attrib['NAME']
            softwareVersion = [software for software in userInfo.findall("Software")][0].text
            return version, username, department, projectName, softwareName, softwareVersion

local_userInfo_version = get_local_userInfo()[0]
local_userInfo_username = get_local_userInfo()[1]
local_userInfo_department = get_local_userInfo()[2]
local_userInfo_projectName = get_local_userInfo()[3]
local_userInfo_softwareName = get_local_userInfo()[4]
local_userInfo_softwareVersion = get_local_userInfo()[5]

def get_UI():
    for UI_data in global_UI_dataRoot:
        for UI in UI_data:
            if UI.attrib["CODE"] == ("MAIN"):
                launcher_UI_file = UI.find("MAIN").text
                return launcher_UI_file

form_class, base_class = uic.loadUiType(get_UI())

### custom object
class HoverButton(QtWidgets.QToolButton):
    def __init__(self, text, parent = None):
        super(HoverButton, self).__init__(parent)
        self.setText(text)

class Demo_MAIN(base_class, form_class):
    def __init__(self, parent=None):
        super(Demo_MAIN, self).__init__(parent)
        self.setupUi(self)
        self.setObjectName("Demo_MAIN")
        self.setWindowTitle("Demo_MAIN")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.initUI()

    def initUI(self):
        self.Launcher = Demo_LAUNCHER(self)
        self.tabWidget_tab.addTab(self.Launcher, "Launcher")

        self.verticalSpacer_window = QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_window.addItem(self.verticalSpacer_window)
        self.button_minimize = HoverButton("_")
        self.horizontalLayout_window.addWidget(self.button_minimize)
        self.button_close = HoverButton("X")
        self.button_close.setStyleSheet("background-color: rgb(255,0,0);")
        self.horizontalLayout_window.addWidget(self.button_close)

        ### signal
        self.button_minimize.clicked.connect(self.showMinimized)
        self.button_close.clicked.connect(QtWidgets.QApplication.quit)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

if __name__ == '__main__':
    global ui
    try:
        ui.close()
    except:
        pass

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #app.setStyle(QtWidgets.QStyleFactory.create("Plastique"))
    #print (QtWidgets.QStyleFactory.keys())

    ui = Demo_MAIN()
    ui.show()
    sys.exit(app.exec_())