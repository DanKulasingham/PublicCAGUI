from PyQt5 import QtWidgets, QtGui, QtCore
import git, os


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    splashPic = QtGui.QPixmap('icons\\splash.png')
    splash = QtWidgets.QSplashScreen(splashPic, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()

    g = git.Git('.')
    g.pull()

    from CAGUI import CAGUI
    from cutplan._classes import CA_MainWindow

    MainWindow = CA_MainWindow()
    ui = CAGUI()
    ui.setupUi(MainWindow)

    splash.close()
    MainWindow.show()
    sys.exit(app.exec_())
