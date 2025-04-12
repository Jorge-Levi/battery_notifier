import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtNetwork import QLocalSocket, QLocalServer
from tray_icon import TrayApp


def is_already_running(app_id="BatteryNotifierApp") -> bool:
    socket = QLocalSocket()
    socket.connectToServer(app_id)
    if socket.waitForConnected(100):
        return True
    socket.abort()
    server = QLocalServer()
    server.listen(app_id)
    return False


def main():
    if is_already_running():
        print("[INFO] BatteryNotifier ya se está ejecutando.")
        sys.exit()

    try:
        app = TrayApp()
        app.run()
    except Exception as e:
        print(f"[ERROR] Fallo en la ejecución de la app: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
