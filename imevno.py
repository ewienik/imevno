#!/usr/bin/env python3

import cv2
import notify2
import os
import signal
import sys
import time


THRESHOLD = 100000
SLEEP = 30


def notify(txt):
    notification = notify2.Notification("Remote notification", txt, "notification-message-im")
    notification.set_urgency(notify2.URGENCY_CRITICAL)
    notification.show()


def main():
    if len(sys.argv) < 3:
        print('Usage:', sys.argv[0], 'screenshot_image', 'dir_with_icons')
        return

    path_screen = sys.argv[1]
    path_dir_icons = sys.argv[2]

    screen = cv2.imread(path_screen)

    names = []
    found = False
    for entry in os.scandir(path_dir_icons):
        if not entry.is_file():
            continue
        found = True
        icon = cv2.imread(entry.path)
        res = cv2.matchTemplate(screen, icon, cv2.TM_SQDIFF)
        min_val, _, _, _ = cv2.minMaxLoc(res)
        if min_val < THRESHOLD:
            names.append(os.path.splitext(entry.name)[0])

    if len(names) > 0:
        notify("You should check remote system for:\n" + ', '.join(names))
        return

    if not found:
        notify("No icons for checking found in " + path_dir_icons)
        return


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    notify2.init('Imevno')
    notify("Start listen with args " + ' '.join(sys.argv))
    while True:
        try:
            main()
        except:
            notify("Exception:\n" + str(sys.exc_info()[0]))
        time.sleep(SLEEP)
