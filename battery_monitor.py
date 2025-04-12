# battery_monitor.py

import psutil
from win10toast import ToastNotifier


class BatteryMonitor:
    def __init__(self):
        self.last_state = None
        self.notifier = ToastNotifier()

    def check_battery(self):
        battery = psutil.sensors_battery()
        if battery is None:
            return

        percent = battery.percent
        plugged = battery.power_plugged

        if percent >= 80 and plugged and self.last_state != "high":
            self.notifier.show_toast(
                "Batería al 80%",
                "Puedes desconectar el cargador.",
                duration=5,
                threaded=True,
            )
            self.last_state = "high"

        elif percent <= 20 and not plugged and self.last_state != "low":
            self.notifier.show_toast(
                "Batería al 20%", "Conecta el cargador.", duration=5, threaded=True
            )
            self.last_state = "low"

        elif 20 < percent < 80:
            self.last_state = None
