"""Тесты команд ls, cd, uptime и tac."""

import sys
import unittest

sys.path.insert(0, "src")

from emulator.commands import (
    CommandError, ShellState, execute)
from emulator.vfs import VfsNode


def make_state():
    """Собрать небольшую VFS для проверок."""
    root = VfsNode("root", True)
    home = VfsNode("home", True)
    todo = VfsNode("todo.txt", False)
    todo.content = "one\ntwo\nthree".encode("utf-8")
    binary = VfsNode("bin.dat", False)
    binary.content = bytes([255, 254, 253])
    home.children["todo.txt"] = todo
    root.children["home"] = home
    root.children["bin.dat"] = binary
    state = ShellState()
    state.root = root
    return state


class TestLs(unittest.TestCase):
    """Проверки команды ls."""

    def test_root(self):
        self.assertEqual(execute("ls", [], None, make_state()),
                         "bin.dat\nhome/")

    def test_path(self):
        self.assertEqual(execute("ls", ["home"], None, make_state()),
                         "todo.txt")

    def test_file(self):
        self.assertEqual(execute("ls", ["bin.dat"], None, make_state()),
                         "bin.dat")

    def test_missing(self):
        with self.assertRaises(CommandError):
            execute("ls", ["nope"], None, make_state())

    def test_no_vfs(self):
        with self.assertRaises(CommandError):
            execute("ls", [], None, ShellState())

    def test_too_many(self):
        with self.assertRaises(CommandError):
            execute("ls", ["a", "b"], None, make_state())


class TestCd(unittest.TestCase):
    """Проверки команды cd."""

    def test_into_dir_and_back(self):
        state = make_state()
        execute("cd", ["home"], None, state)
        self.assertEqual(state.get_current_path(), "/home")
        self.assertEqual(execute("ls", [], None, state), "todo.txt")
        execute("cd", [".."], None, state)
        self.assertEqual(state.get_current_path(), "/")

    def test_absolute_and_no_args(self):
        state = make_state()
        execute("cd", ["/home"], None, state)
        execute("cd", [], None, state)
        self.assertEqual(state.get_current_path(), "/")

    def test_up_from_root(self):
        state = make_state()
        execute("cd", ["../.."], None, state)
        self.assertEqual(state.get_current_path(), "/")

    def test_to_file(self):
        with self.assertRaises(CommandError):
            execute("cd", ["bin.dat"], None, make_state())

    def test_missing(self):
        state = make_state()
        with self.assertRaises(CommandError):
            execute("cd", ["nope"], None, state)
        self.assertEqual(state.get_current_path(), "/")


class TestUptime(unittest.TestCase):
    """Проверки команды uptime."""

    def test_format(self):
        result = execute("uptime", [], None, ShellState())
        self.assertEqual(result, "up 00:00:00")

    def test_with_args(self):
        with self.assertRaises(CommandError):
            execute("uptime", ["x"], None, ShellState())


class TestTac(unittest.TestCase):
    """Проверки команды tac."""

    def test_reverse(self):
        self.assertEqual(
            execute("tac", ["home/todo.txt"], None, make_state()),
            "three\ntwo\none")

    def test_no_args(self):
        with self.assertRaises(CommandError):
            execute("tac", [], None, make_state())

    def test_dir(self):
        with self.assertRaises(CommandError):
            execute("tac", ["home"], None, make_state())

    def test_binary(self):
        with self.assertRaises(CommandError):
            execute("tac", ["bin.dat"], None, make_state())

    def test_missing(self):
        with self.assertRaises(CommandError):
            execute("tac", ["nope"], None, make_state())


if __name__ == "__main__":
    unittest.main()