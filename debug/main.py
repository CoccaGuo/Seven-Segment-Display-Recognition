# main.py by CoccaGuo at 2022/03/02 11:23
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication
import sys

from ui import Ui_Dialog

# serve as an UI thread
if __name__ == '__main__':
    # the thread for app
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    dialog = QDialog()
    ui.setupUi(dialog)
    dialog.setWindowIcon(QIcon('pressure.ico'))
    dialog.show()
    sys.exit(app.exec_())
