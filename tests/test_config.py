"""Тесты для config.py и команды conf-dump."""

import sys
import unittest

sys.path.insert(0, "src")

from emulator.commands import execute, CommandError
from emulator.config import EmulatorConfig, parse_args


class TestParseArgs(unittest.TestCase):
    """Проверка разбора параметров командной строки."""

    def test_no_arguments(self):
        config = parse_args([])
        self.assertIsNone(config.vfs_path)
        self.assertIsNone(config.script_path)

    def test_vfs_path_only(self):
        config = parse_args(["--vfs-path", "vfs.xml"])
        self.assertEqual(config.vfs_path, "vfs.xml")
        self.assertIsNone(config.script_path)

    def test_script_only(self):
        config = parse_args(["--script", "start.txt"])
        self.assertIsNone(config.vfs_path)
        self.assertEqual(config.script_path, "start.txt")

    def test_both_arguments(self):
        config = parse_args(["--vfs-path", "a.xml", "--script", "b.txt"])
        self.assertEqual(config.vfs_path, "a.xml")
        self.assertEqual(config.script_path, "b.txt")


class TestAsDict(unittest.TestCase):
    """Проверка представления параметров в виде словаря."""

    def test_empty_values_for_missing_params(self):
        params = EmulatorConfig().as_dict()
        self.assertEqual(params["vfs_path"], "")
        self.assertEqual(params["script_path"], "")

    def test_values_for_given_params(self):
        params = EmulatorConfig("a.xml", "b.txt").as_dict()
        self.assertEqual(params["vfs_path"], "a.xml")
        self.assertEqual(params["script_path"], "b.txt")


class TestConfDump(unittest.TestCase):
    """Проверка служебной команды conf-dump."""

    def test_conf_dump_output(self):
        config = EmulatorConfig("a.xml", "b.txt")
        result = execute("conf-dump", [], config)
        self.assertEqual(result, "vfs_path=a.xml\nscript_path=b.txt")

    def test_conf_dump_with_arguments_raises_error(self):
        with self.assertRaises(CommandError):
            execute("conf-dump", ["lishnee"], EmulatorConfig())

    def test_conf_dump_without_config_raises_error(self):
        with self.assertRaises(CommandError):
            execute("conf-dump", [])


if __name__ == "__main__":
    unittest.main()