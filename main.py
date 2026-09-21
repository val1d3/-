"""Точка входа эмулятора."""

import sys
sys.path.insert(0, "src")

from emulator.config import EmulatorConfig
from emulator.gui import EmulatorApp

config = EmulatorConfig()
app = EmulatorApp(config)
app.run()
'ls, ls -la /tmp, cd, cd /home/user, cd "My Documents", exit hello, qwerty, exit'