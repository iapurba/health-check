#!/usr/bin/env python3

import shutil
import sys
import os
import socket

def check_reboot():
    "Return true if the computer has pending reboot"
    return os.path.exists("/run/reboot-required")


def check_disk_usage(disk, min_gb, min_percent):
    """Returns True if there is enough free disk space, false otherwise."""
    du = shutil.disk_usage(disk)
    # Calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    # Calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False


def check_root_full():
    """Return True if the root partition is full, False otherwise."""
    return check_disk_usage(disk="/", min_gb=2, min_percent=10)


def check_no_network():
    """Return True if it fails to resolver Google's URL, False otherwise"""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def main():
    checks = [
        [check_reboot, "Pending Reboot"],
        [check_root_full, "Root Partition Full"],
        [check_no_network, "No Working Network"],
    ]
    everything_ok = True
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = false

    if not everything_ok:
        sys.exit(1)

    print("Everything OK.")
    sys.exit(0)

main()
