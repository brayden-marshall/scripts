#!/usr/bin/env python3

"""
Sends a desktop notification when remaining battery percentage goes under a specified
amount. Intended to be run as a systemd user unit (using the matching
battery_notification.service file)
"""

LOW_PERCENTAGE = 20
CRITICAL_PERCENTAGE = 10
INTERVAL = 60

import subprocess
import logging
import sys
try:
    from systemd.journal import JournalHandler
except ModuleNotFoundError as e:
    print(e)
    sys.exit(1)
import time

def get_battery_percentage(upower_path):
    # command: upower -i <upower_path> | grep percentage
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
    subprocess.check_output(
        ["notify-send", "--urgency=critical", message]
    )

if __name__=="__main__":
    log = logging.getLogger('battery_notification')
    log.addHandler(JournalHandler())
    log.setLevel(logging.INFO)
    log.info("Started battery notification service")

    # keep track of which notifications have been sent so we don't continuously
    # send desktop notifications on every loop
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
            log.info("Sent low battery notification")

        if (percentage < CRITICAL_PERCENTAGE and not critical_notified):
            send_notification(
                "Critical battery: {}%\nYou really need to plug me in."
                    .format(percentage)
            )
            critical_notified = True
            log.info("Sent low battery notification")

        if (percentage >= LOW_PERCENTAGE):
            low_notified = False

        if (percentage >= CRITICAL_PERCENTAGE):
            critical_notified = False

        time.sleep(INTERVAL)
