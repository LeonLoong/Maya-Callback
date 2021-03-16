from PyQt5 import QtCore, QtGui, QtWidgets, uic
from win32com.client import Dispatch
import os, subprocess, sys, pywintypes
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

local_mayaLauncherDirectory = ("{}\{}".format(local_directory, "Launcher"))
local_mayaLauncher = ("{}\Maya.bat".format(local_mayaLauncherDirectory))

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

global_launcherDirectory = (r"{}\{}".format(global_directory, "Script\Demo_Main"))
global_launcher = (r"{}\Demo\Demo.exe".format(global_launcherDirectory))
global_launcher_version_parser = Dispatch('Scripting.FileSystemObject')
global_launcher_version = global_launcher_version_parser.GetFileVersion(global_launcher)

local_launcherDirectory = (r"{}\{}".format(local_directory, "Program"))
local_launcher = (r"{}\Demo\Demo.exe".format(local_launcherDirectory))
local_launcher_version_parser = Dispatch('Scripting.FileSystemObject')
try:
    local_launcher_version = local_launcher_version_parser.GetFileVersion(local_launcher)
except pywintypes.com_error:
    print ("System unable to locate {} file".format(local_launcher))
    sys.exit()

### function
def copy_File(src, dst):
    from shutil import copyfile
    copyfile(src, dst)

def copy_Directory(src, dst):
    from shutil import copytree
    copytree(src, dst)

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
                launcher_UI_file = UI.find("LAUNCHER").text
                return launcher_UI_file

form_class, base_class = uic.loadUiType(get_UI())

### custom object
class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)
        self.sectionFormat = QtGui.QTextCharFormat()
        self.sectionFormat.setForeground(QtCore.Qt.green)
        self.errorFormat = QtGui.QTextCharFormat()
        self.errorFormat.setForeground(QtCore.Qt.red)

    def highlightBlock(self, text):
        # uncomment this line for Python2
        text = (text)
        if text.startswith('[SUCCESS]'):
            self.setFormat(0, len(text), self.sectionFormat)
        elif text.startswith('[ERROR]'):
            self.setFormat(0, len(text), self.errorFormat)

class Demo_LAUNCHER(base_class, form_class):
    def __init__(self, parent=None):
        super(Demo_LAUNCHER, self).__init__(parent)
        self.pushButton_projectName_list = []
        self.setupUi(self)
        self.setObjectName("Demo_LAUNCHER")
        self.setWindowTitle("Demo_LAUNCHER")
        self.initUI()

    def initUI(self):
        self.highlighter = Highlighter(self.textEdit_messages.document())
        self.verticalSpacer_window = QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        ### signal
        ### Project Name and Icon PushButton
        for global_projectInfo in global_projectInfo_dataRoot:
            for projectInfo in global_projectInfo:
                if projectInfo.attrib["CODE"] != "None" and projectInfo.attrib["NAME"] != "None":
                    projectName = projectInfo.attrib["CODE"]
                    self.pushButton_projectName = QtWidgets.QPushButton(projectName)
                    self.pushButton_projectName.setObjectName(projectName)
                    self.pushButton_projectName.setFixedWidth(64)
                    self.pushButton_projectName.setFixedHeight(64)
                    self.pushButton_projectName.setCheckable(True)
                    self.pushButton_projectName.setChecked(False)
                    #self.pushButton_projectName.setStyleSheet("background-color: rgb(200, 200, 200);")
                    self.verticalLayout_projectIcon.addWidget(self.pushButton_projectName)
                    self.pushButton_projectName.released.connect(self.set_checked)
                    self.pushButton_projectName_list.append(self.pushButton_projectName)
                    if self.pushButton_projectName.objectName() == local_userInfo_projectName:
                        self.pushButton_projectName.setChecked(True)

        self.verticalSpacer_projectIcon = QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_projectIcon.addItem(self.verticalSpacer_projectIcon)

        ### Department and Software ComboBox
        for global_projectInfo in global_projectInfo_dataRoot:
            for projectInfo in global_projectInfo:
                if projectInfo.attrib["CODE"] == local_userInfo_projectName:
                    softwareName = [software for software in projectInfo.findall("PROJECT_SOFTWARE")][0].attrib['NAME']
                    softwareIcon = [software for software in projectInfo.findall("PROJECT_SOFTWARE")][0].attrib['ICON']
                    self.comboBox_software.addItem(softwareName)
                    for info in projectInfo:
                        if info.tag == "DEPARTMENT":
                            departments = info.text.split("|")
                            for department in departments:
                                self.comboBox_department.addItem(department)

        index = self.comboBox_department.findText(local_userInfo_department, QtCore.Qt.MatchFixedString)
        self.comboBox_department.setCurrentIndex(index)

        index = self.comboBox_software.findText(local_userInfo_softwareName, QtCore.Qt.MatchFixedString)
        self.comboBox_software.setCurrentIndex(index)

        self.comboBox_department.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.comboBox_software.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        ### check for synchronization between local and global launcher/userInfo version
        if global_launcher_version == local_launcher_version and global_userInfo_version == local_userInfo_version:
            self.textEdit_messages.append('[SUCCESS] : Launcher Version is Up-2-Date')
            self.textEdit_messages.append('[SUCCESS] : User Info Version is Up-2-Date')
            self.pushButton_start.clicked.connect(self.start_software)
        elif global_launcher_version == local_launcher_version and global_userInfo_version != local_userInfo_version:
            self.textEdit_messages.append('[ERROR]   : User Info Version is Out-2-Date')
            copy_File(global_userInfo, local_userInfo)
            self.textEdit_messages.append('[SUCCESS] : User Info Version is Updated')
            self.pushButton_start.clicked.connect(self.start_software)
        else:
            self.textEdit_messages.append('[ERROR]   : Launcher Version is Out-2-Date')
            self.pushButton_start.setText("Update")
            self.pushButton_start.clicked.connect(self.update_launcher)

    # copy_File(global_userInfo, local_userInfo)
    def set_checked(self):
        sending_button = self.sender()
        for project in local_userInfo_dataRoot.iter('Project'):
            project.text = str(str(sending_button.objectName()))
        local_userInfo_dataTree.write(local_userInfo_dataPath)

        for projectName in self.pushButton_projectName_list:
            if projectName != sending_button:
                projectName.setChecked(False)

    def start_software(self):
        local_userInfo_dataPath = (r"{}\Data\User_Info.xml").format(local_directory)
        local_userInfo_dataTree = xml.parse(local_userInfo_dataPath)
        local_userInfo_dataRoot = local_userInfo_dataTree.getroot()
        def get_newProject():
            for pushButton in self.pushButton_projectName_list:
                if pushButton.isChecked():
                    newProject = pushButton.text()
                    return newProject

        newSoftware = self.comboBox_software.currentText()
        newDepartment = self.comboBox_department.currentText()
        newProject = get_newProject()
        for department in local_userInfo_dataRoot.iter('Department'):
            department.text = str(newDepartment)
        for project in local_userInfo_dataRoot.iter('Project'):
            project.text = str(newProject)
        local_userInfo_dataTree.write(local_userInfo_dataPath)

        print (local_mayaLauncherDirectory, newSoftware)
        subprocess.Popen("{}\{}.bat".format(local_mayaLauncherDirectory, newSoftware), stdin = subprocess.PIPE)

    def update_launcher(self):
        local_to_modify_launcher = (r"{}\Demo".format(local_launcherDirectory))
        local_modified_launcher = (r"{}\Demo_DELETE".format(local_launcherDirectory))
        os.rename(local_to_modify_launcher, local_modified_launcher)
        copy_Directory(r"{}\{}".format(global_launcherDirectory, "Demo"), r"{}\{}".format(local_launcherDirectory, "Demo"))
        subprocess.Popen(local_launcher, stdin=subprocess.PIPE)
        QtWidgets.QApplication.quit()