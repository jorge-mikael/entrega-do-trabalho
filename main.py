import sys
from PyQt6.QtWidgets import QApplication, QDialog
from config.excecao_global import excecao_global
from ui.login_ui import LoginUI
from controllers.login_controller import LoginController
from ui.main_window_ui import MainWindowUI
from controllers.main_window_controller import MainWindowController

sys.excepthook = excecao_global
app = QApplication(sys.argv)

login_ui = LoginUI()
login_controller = LoginController(login_ui)
login_controller.carregar()
if login_ui.exec() == QDialog.DialogCode.Accepted:
    main_window = MainWindowUI()
    main_window_controller = MainWindowController(main_window)
    main_window_controller.carregar()
    main_window.show()
    sys.exit(app.exec())
else:
    sys.exit()

