import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from widgets import AudioSplitter

def main():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    wrapper = AudioSplitter()
    mainWindow.setCentralWidget(wrapper)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()