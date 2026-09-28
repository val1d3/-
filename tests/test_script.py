"""Тесты для script.py: чтение стартового скрипта."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, "src")

from emulator.script import read_script_lines, ScriptError


class TestReadScriptLines(unittest.TestCase):
    """Проверка чтения файла со скриптом."""

    def test_empty_lines_are_skipped(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as script_file:
            script_file.write("ls\n\n   \ncd /tmp\n")
            path = script_file.name

        try:
            lines = read_script_lines(path)
        finally:
            os.remove(path)

        self.assertEqual(lines, ["ls", "cd /tmp"])

    def test_missing_file_raises_error(self):
        with self.assertRaises(ScriptError):
            read_script_lines("no_such_script_file.txt")


if __name__ == "__main__":
    unittest.main()