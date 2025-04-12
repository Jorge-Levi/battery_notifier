# tray_icon.py

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction, QIcon
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer
from battery_monitor import BatteryMonitor
import sys
import os


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Cargar iconos
        icon_path_on = os.path.join("assets", "icon_on.png")
        icon_path_off = os.path.join("assets", "icon_off.png")
        self.icon_on = QIcon(icon_path_on)
        self.icon_off = QIcon(icon_path_off)

        # Inicializa como activo
        self.monitor = BatteryMonitor()
        self.is_active = True

        # Crear icono de sistema
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon_on)
        self.tray.setToolTip("BatteryNotifier - Monitoreo activo")
        self.tray.setVisible(True)

        # Menú de clic derecho
        self.menu = QMenu()

        self.toggle_action = QAction("Desactivar monitoreo")
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(self.toggle_action)

        exit_action = QAction("Salir")
        exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(exit_action)

        self.tray.setContextMenu(self.menu)

        # Timer para chequear batería cada minuto
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_monitor)
        self.timer.start(60 * 1000)  # cada 60 segundos

        # Permitir acción con clic izquierdo
        self.tray.activated.connect(self.on_click)

        # Primera revisión inmediata
        self.run_monitor()

    def run_monitor(self):
        if self.is_active:
            self.monitor.check_battery()
            self.tray.setToolTip("BatteryNotifier - Monitoreo activo")
        else:
            self.tray.setToolTip("BatteryNotifier - Monitoreo inactivo")

    def toggle_monitoring(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.tray.setIcon(self.icon_on)
            self.toggle_action.setText("Desactivar monitoreo")
        else:
            self.tray.setIcon(self.icon_off)
            self.toggle_action.setText("Activar monitoreo")
        self.run_monitor()

    def on_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Clic izquierdo
            self.toggle_monitoring()

    def exit_app(self):
        self.tray.hide()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())
