#!/usr/bin/env python3

import cv2
import notify2
import os
import signal
import sys
import time


THRESHOLD = 1000
SLEEP = 30


def main():
    if len(sys.argv) < 3:
        print('Usage:', sys.argv[0], 'screenshot_image', 'dir_with_icons')
        return

    path_screen = sys.argv[1]
    path_dir_icons = sys.argv[2]

    notify2.init('Imevno')

    screen = cv2.imread(path_screen)

    names = []
    for entry in os.scandir(path_dir_icons):
        if not entry.is_file():
            continue
        icon = cv2.imread(entry.path)
        res = cv2.matchTemplate(screen, icon, cv2.TM_SQDIFF)
        min_val, _, _, _ = cv2.minMaxLoc(res)
        if min_val < THRESHOLD:
            names.append(os.path.splitext(entry.name)[0])

    if len(names) > 0:
        notify2.Notification(
            "Remote notification",
            "You should check remote system for:\n" + ', '.join(names),
            "notification-message-im"
        ).show()


def signal_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        main()
        time.sleep(SLEEP)
