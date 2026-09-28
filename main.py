"""Точка входа эмулятора."""

import sys
sys.path.insert(0, "src")

from emulator.config import parse_args
from emulator.gui import EmulatorApp

config = parse_args(sys.argv[1:])
app = EmulatorApp(config)
app.run()