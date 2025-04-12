# battery_monitor.py

import psutil


class BatteryMonitor:
    """
    Monitorea el nivel de batería y lanza notificaciones en puntos clave.
    """

    def __init__(self, tray_icon=None, high_threshold=80, low_threshold=20):
        self.tray_icon = (
            tray_icon  # Aquí inyectamos el ícono de bandeja desde tray_icon.py
        )
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.last_state = None

    def check_battery(self, force_notify=False):
        battery = psutil.sensors_battery()
        if battery is None:
            return

        percent = battery.percent
        plugged = battery.power_plugged

        if (
            percent >= self.high_threshold
            and plugged
            and (self.last_state != "high" or force_notify)
        ):
            self._notify("Batería al 80%", "Puedes desconectar el cargador.")
            self.last_state = "high"

        elif (
            percent <= self.low_threshold
            and not plugged
            and (self.last_state != "low" or force_notify)
        ):
            self._notify("Batería al 20%", "Conecta el cargador.")
            self.last_state = "low"

        elif self.low_threshold < percent < self.high_threshold:
            self.last_state = None

    def _notify(self, title, message):
        if self.tray_icon:
            self.tray_icon.showMessage(title, message, self.tray_icon.icon(), 5000)
