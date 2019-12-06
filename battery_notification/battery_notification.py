#!/usr/bin/env python3

import subprocess
import time

def get_battery_percentage(upower_path):
    # upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage
    p1 = subprocess.Popen(
        ["upower", "-i", upower_path],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    p2 = subprocess.Popen(
        ["grep", "percentage"], stdin=p1.stdout, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    p1.stdout.close()
    reply = p2.communicate()[0]
    p1.wait()

    # converts from 'percentage: 99%' -> 99
    return int(reply.decode('utf-8').strip().split()[1].strip('%'))

def send_notification(message):
    output = subprocess.check_output(
        ["notify-send", message]
    )


if __name__=="__main__":
    LOW_PERCENTAGE = 20
    CRITICAL_PERCENTAGE = 10

    low_notified = False
    critical_notified = False

    while True:
        percentage = get_battery_percentage(
            "/org/freedesktop/UPower/devices/battery_BAT0"
        )

        if ((percentage >= CRITICAL_PERCENTAGE and percentage < LOW_PERCENTAGE)
                and not low_notified):
            send_notification(
                "Low battery: {}%\nYou should plug me in."
                    .format(percentage)
            )
            low_notified = True

        if (percentage < CRITICAL_PERCENTAGE and not critical_notified):
            send_notification(
                "Critical battery: {}%\nYou really need to plug me in."
                    .format(percentage)
            )
            critical_notified = True

        time.sleep(60)
