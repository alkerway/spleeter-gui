import sys

from pathlib import Path

from PySide2.QtWidgets import QWidget, QFrame, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QScrollArea, QSizePolicy
from PySide2.QtGui import QFont, QCursor
from PySide2.QtCore import Qt, SIGNAL, QCoreApplication

from .StemOptions import StemOptions
from runspleeter import RunSpleeter

boldFont = QFont()
boldFont.setBold(True)
boldFont.setPointSize(12)


class AudioSplitter(QWidget):
    def __init__(self):
        super(AudioSplitter, self).__init__()

        self.inputFile = ''
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.buildUI()


    def buildUI(self):
        self.closeButton = QPushButton('close')
        self.closeButton.setShortcut('Ctrl+W')
        self.closeButton.clicked.connect(self.onClose)
        self.closeButton.setFixedSize(0, 0)

        self.mainWrapperLayout = QVBoxLayout()
        self.mainWrapperLayout.addWidget(self.closeButton)

        self.divider1 = QFrame()
        self.divider1.setFrameShape(QFrame.HLine)
        self.divider1.setFrameShadow(QFrame.Sunken)

        self.divider2 = QFrame()
        self.divider2.setFrameShape(QFrame.HLine)
        self.divider2.setFrameShadow(QFrame.Sunken)

        self.headerLayout = self.buildHeader()
        self.optionsLayout = self.buildOptionsLayout()



        self.statusTextScroll = QScrollArea()
        self.statusTextScroll.setWidgetResizable(True)
        self.statusWidget = QWidget()
        self.statusTextScroll.setWidget(self.statusWidget)
        self.statusText = QVBoxLayout(self.statusWidget)
        self.statusTextScroll.setContentsMargins(0, 0, 0, 50)
        self.statusWidget.setLayout(self.statusText)

        self.mainWrapperLayout.addLayout(self.headerLayout)
        self.mainWrapperLayout.addWidget(self.divider1)
        self.mainWrapperLayout.addLayout(self.optionsLayout)
        self.mainWrapperLayout.addWidget(self.divider2)
        self.mainWrapperLayout.addWidget(self.statusTextScroll)


        self.startButton = QPushButton('Go')
        self.startButton.clicked.connect(self.onStartClick)
        self.mainWrapperLayout.addWidget(self.startButton)

        self.setLayout(self.mainWrapperLayout)
        self.setMinimumWidth(450)

    def buildHeader(self):
        appTitle = QLabel(self)
        appTitle.setText('Audio Splitter')
        appTitle.setFont(boldFont)

        chooseFileButton = QPushButton("Choose File")
        chooseFileButton.clicked.connect(self.loadNewFile)
        chooseFileButton.setShortcut('Ctrl+O')
        chooseFileButton.setMaximumWidth(90)

        self.fileLabel = QLabel()

        titleBar = QHBoxLayout()
        titleBar.addWidget(appTitle)
        titleBar.addWidget(chooseFileButton)


        headerLayout = QVBoxLayout()
        headerLayout.addLayout(titleBar)
        headerLayout.addWidget(self.fileLabel)


        return headerLayout

    def buildOptionsLayout(self):
        stemsRow = QHBoxLayout()
        stemsLabel = QLabel('Split into ')

        stemBox = QComboBox()
        stemBox.addItem('2 tracks')
        stemBox.addItem('4 tracks')
        stemBox.addItem('5 tracks')
        stemBox.setMaximumWidth(100)

        self.stemOptions = StemOptions()
        stemBox.activated[str].connect(self.stemOptions.setStems)

        stemsRow.addWidget(stemsLabel)
        stemsRow.addWidget(stemBox)
        stemsRow.addStretch()


        optionsLayout = QVBoxLayout()
        optionsLayout.addLayout(stemsRow)
        optionsLayout.addLayout(self.stemOptions)
        return optionsLayout


    def getCsvFileName(self):
        success = QFileDialog.getOpenFileName(None, 'Open Audio Track', '', 'Audio Files (*.mp3 *.wav *.flac *.ogg)')[0]
        if success:
            return success

    def loadNewFile(self):
        fileName = self.getCsvFileName()
        if fileName:
            path = Path(fileName)
            self.inputFile = path
            self.fileLabel.setText(f'Input: {self.inputFile.name}')

    def onStartClick(self):
        runInstance = RunSpleeter()
        self.updateStatus('Initializing')
        runInstance.startRun(self.inputFile, self.stemOptions.curStems, self.stemOptions.curOptions, self.updateStatus)

    def updateStatus(self, status, isError=False):
        newLine = QLabel(('ERROR' if isError else 'STATUS') + f': {status}')
        newLine.setWordWrap(True)
        self.statusText.addWidget(newLine)
        self.statusWidget.setLayout(self.statusText)
        QCoreApplication.processEvents()
        QCoreApplication.processEvents()
        self.statusTextScroll.verticalScrollBar().setValue(self.statusTextScroll.verticalScrollBar().maximum() + 1)

    def onClose(self):
        sys.exit()