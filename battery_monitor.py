# battery_monitor.py

import psutil
from plyer import notification


class BatteryMonitor:
    def __init__(self):
        self.last_state = None

    def check_battery(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return

        percent = battery.percent
        plugged = battery.power_plugged

        if percent >= 80 and plugged and self.last_state != "high":
            notification.notify(
                title="Batería al 80%",
                message="Puedes desconectar el cargador.",
                timeout=5,
            )
            self.last_state = "high"

        elif percent <= 20 and not plugged and self.last_state != "low":
            notification.notify(
                title="Batería al 20%", message="Conecta el cargador.", timeout=5
            )
            self.last_state = "low"

        elif 20 < percent < 80:
            self.last_state = None
