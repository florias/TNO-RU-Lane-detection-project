from GUI.mainwindow import MainWindow
from PyQt4 import QtGui
import sys


if __name__ == "__main__":
    # Start the program, create the GUI.
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.run()
    if window.file_available or window.live:
        window.show()
        sys.exit(app.exec_())
    else:
        window.close()
