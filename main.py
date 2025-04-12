import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtNetwork import QLocalSocket, QLocalServer


def is_already_running(app_id="BatteryNotifierApp"):
    socket = QLocalSocket()
    socket.connectToServer(app_id)
    if socket.waitForConnected(100):
        return True
    socket.abort()
    server = QLocalServer()
    server.listen(app_id)
    return False


if is_already_running():
    sys.exit()

from tray_icon import TrayApp

if __name__ == "__main__":
    app = TrayApp()
    app.run()
