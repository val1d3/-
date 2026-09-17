"""Точка входа эмулятора."""

import sys
sys.path.insert(0, "src")

from emulator.config import EmulatorConfig
from emulator.gui import EmulatorApp

config = EmulatorConfig()
app = EmulatorApp(config)
app.run()
