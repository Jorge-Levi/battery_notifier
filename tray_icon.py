# tray_icon.py

import os
import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QTimer
from battery_monitor import BatteryMonitor


def resource_path(relative_path):
    """
    Obtiene la ruta absoluta de recursos, compatible tanto en desarrollo
    como cuando se empaqueta con PyInstaller (.exe)
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Rutas a los iconos
        icon_path_on = resource_path(os.path.join("assets", "icon_on.png"))
        icon_path_off = resource_path(os.path.join("assets", "icon_off.png"))
        self.icon_on = QIcon(icon_path_on)
        self.icon_off = QIcon(icon_path_off)

        # Inicia monitor
        self.monitor = BatteryMonitor()
        self.is_active = True

        # Crear icono de sistema
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon_on)
        self.tray.setToolTip("BatteryNotifier - Monitoreo activo")
        self.tray.setVisible(True)

        # Menú contextual (clic derecho)
        self.menu = QMenu()

        self.toggle_action = QAction("Desactivar monitoreo")
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(self.toggle_action)

        exit_action = QAction("Salir")
        exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(exit_action)

        self.tray.setContextMenu(self.menu)

        # Temporizador para verificar batería cada minuto
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_monitor)
        self.timer.start(60 * 1000)  # 60 segundos

        # Acción para clic izquierdo
        self.tray.activated.connect(self.on_click)

        # Revisión inicial inmediata
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
