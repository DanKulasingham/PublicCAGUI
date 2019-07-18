from PyQt5 import QtWidgets, QtGui, QtCore
import git, os


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication.instance()

    splashPic = QtGui.QPixmap('icons\\splash.png')
    splash = QtWidgets.QSplashScreen(splashPic, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()

    g = git.cmd.Git(os.path.dirname(os.path.realpath(__file__)))
    g.pull('https://github.com/DanKulasingham/CutplanGUI.git', 'master')

    from CAGUI import CAGUI
    from cutplan._classes import CA_MainWindow

    MainWindow = CA_MainWindow()
    ui = CAGUI()
    ui.setupUi(MainWindow)

    splash.close()
    MainWindow.show()
    sys.exit(app.exec_())
