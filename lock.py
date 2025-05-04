import os
import psutil

LOCK_COMMAND = "rundll32.exe user32.dll,LockWorkStation" if os.name == 'nt' else "gnome-screensaver-command -l"


def lock_computer():
   
    os.system(LOCK_COMMAND)