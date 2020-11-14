
from PySide2.QtWidgets import QWidget, QCheckBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QAction, QSizePolicy
from PySide2.QtGui import QFont, QCursor
from PySide2.QtCore import Qt, SIGNAL
from utils import clearLayout

boldFont = QFont()
boldFont.setBold(True)
boldFont.setPointSize(12)

class StemOptions(QVBoxLayout):
    def __init__(self):
        super(StemOptions, self).__init__()
        self.curStems = '2 tracks'
        self.curOptions = (set(), set())
        self.buildLayout()

    def buildLayout(self, pastOptions=(set(), set())):
        isolateTitle = QLabel('Isolate')
        removeTitle = QLabel('Remove')

        isolateBoxes = self.buildBoxes(True, pastOptions[0])
        removeBoxes = self.buildBoxes(False, pastOptions[1])

        isolateCol = QVBoxLayout()
        removeCol = QVBoxLayout()

        isolateCol.addWidget(isolateTitle)
        isolateCol.addLayout(isolateBoxes)
        removeCol.addWidget(removeTitle)
        removeCol.addLayout(removeBoxes)

        columns = QHBoxLayout()
        columns.addLayout(isolateCol)
        columns.addLayout(removeCol)

        self.previewOutput = QLabel()
        self.previewOutput.setWordWrap(True)
        self.updatePreview()

        self.addLayout(columns)
        self.addWidget(self.previewOutput)

    def setStems(self, stems):
        self.curStems = stems
        if stems != '5 tracks':
            self.curOptions[0].discard('piano')
            self.curOptions[1].discard('piano')
        if stems == '2 tracks':
            self.curOptions[0].discard('bass')
            self.curOptions[1].discard('bass')
            self.curOptions[0].discard('drums')
            self.curOptions[1].discard('drums')
        clearLayout(self)
        self.buildLayout(self.curOptions)

    def setChecked(self, stem, isIsolate, checked):
        if checked:
            self.curOptions[0 if isIsolate else 1].add(stem)
        else:
            self.curOptions[0 if isIsolate else 1].remove(stem)
        self.updatePreview()

    def updatePreview(self):
        text = 'Output Tracks: '
        iso = map(lambda x: x + '.wav', self.curOptions[0])
        rem = map(lambda x: 'no_' + x + '.wav', self.curOptions[1])
        self.previewOutput.setText(text + ', '.join(list(iso) + list(rem)))

    def buildBoxes(self, isIsolate, pastOptions):
        boxColumn = QVBoxLayout()

        vocals = QCheckBox("Vocals")
        if 'vocals' in pastOptions:
            vocals.setChecked(True)
        vocals.toggled.connect(lambda x: self.setChecked('vocals', isIsolate, x))
        boxColumn.addWidget(vocals)

        if self.curStems != '2 tracks':
            if self.curStems == '5 tracks':
                piano = QCheckBox("Piano")
                if 'piano' in pastOptions:
                    piano.setChecked(True)
                piano.toggled.connect(lambda x: self.setChecked('piano', isIsolate, x))
                boxColumn.addWidget(piano)

            bass = QCheckBox("Bass")
            if 'bass' in pastOptions:
                bass.setChecked(True)
            bass.toggled.connect(lambda x: self.setChecked('bass', isIsolate, x))
            boxColumn.addWidget(bass)

            drums = QCheckBox("Drums")
            if 'drums' in pastOptions:
                drums.setChecked(True)
            drums.toggled.connect(lambda x: self.setChecked('drums', isIsolate, x))
            boxColumn.addWidget(drums)

        other = QCheckBox('Other')
        if 'other' in pastOptions:
            other.setChecked(True)
        other.toggled.connect(lambda x: self.setChecked('other', isIsolate, x))
        boxColumn.addWidget(other)

        return boxColumn
