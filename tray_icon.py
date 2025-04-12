# tray_icon.py

import sys
import os
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QTimer
from battery_monitor import BatteryMonitor


def resource_path(relative_path):
    """
    Obtiene la ruta absoluta del recurso.
    Compatible con PyInstaller (.exe)
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Iconos
        self.icon_active = QIcon(resource_path("assets/icon_on.png"))
        self.icon_inactive = QIcon(resource_path("assets/icon_off.png"))

        # Bandeja del sistema
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon_active)
        self.tray_icon.setToolTip("BatteryNotifier - Monitoreo activo")
        self.tray_icon.setVisible(True)

        # Monitoreo de batería
        self.monitor = BatteryMonitor(tray_icon=self.tray_icon)
        self.monitoring_enabled = True

        # Menú contextual
        self.menu = QMenu()
        self.toggle_action = QAction("Desactivar monitoreo")
        self.toggle_action.triggered.connect(self.toggle_monitoring)
        self.menu.addAction(self.toggle_action)

        exit_action = QAction("Salir")
        exit_action.triggered.connect(self.exit_application)
        self.menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.menu)

        # Clic izquierdo = toggle
        self.tray_icon.activated.connect(self.handle_click)

        # Timer de verificación cada minuto
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_monitor)
        self.timer.start(60 * 1000)  # 60 segundos

        # Primer chequeo inmediato
        self.monitor.check_battery(force_notify=True)

    def run_monitor(self):
        if self.monitoring_enabled:
            self.monitor.check_battery()
            self.tray_icon.setToolTip("BatteryNotifier - Monitoreo activo")
        else:
            self.tray_icon.setToolTip("BatteryNotifier - Monitoreo inactivo")

    def toggle_monitoring(self):
        self.monitoring_enabled = not self.monitoring_enabled
        if self.monitoring_enabled:
            self.tray_icon.setIcon(self.icon_active)
            self.toggle_action.setText("Desactivar monitoreo")
        else:
            self.tray_icon.setIcon(self.icon_inactive)
            self.toggle_action.setText("Activar monitoreo")
        self.run_monitor()

    def handle_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Clic izquierdo
            self.toggle_monitoring()

    def exit_application(self):
        self.tray_icon.hide()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())
