"""Тесты для parser.py."""

import sys
import unittest

sys.path.insert(0, "src")

from emulator.parser import parse_line, split_command, ParserError


class TestParseLine(unittest.TestCase):
    """Проверка функции parse_line."""

    def test_simple_command(self):
        result = parse_line("ls -la")
        self.assertEqual(result, ["ls", "-la"])

    def test_empty_line(self):
        result = parse_line("")
        self.assertEqual(result, [])

    def test_quoted_argument(self):
        result = parse_line('cd "My Documents"')
        self.assertEqual(result, ["cd", "My Documents"])

    def test_unclosed_quote_raises_error(self):
        with self.assertRaises(ParserError):
            parse_line('cd "unclosed')


class TestSplitCommand(unittest.TestCase):
    """Проверка функции split_command."""

    def test_command_with_args(self):
        command, args = split_command(["ls", "-la", "/tmp"])
        self.assertEqual(command, "ls")
        self.assertEqual(args, ["-la", "/tmp"])

    def test_empty_tokens(self):
        command, args = split_command([])
        self.assertEqual(command, "")
        self.assertEqual(args, [])


if __name__ == "__main__":
    unittest.main()
