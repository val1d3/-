"""Тесты для vfs.py: загрузка VFS из XML."""

import base64
import os
import sys
import tempfile
import unittest

sys.path.insert(0, "src")

from emulator.vfs import load_vfs, VfsError


def make_temp_xml(text):
    """Создать временный XML-файл с заданным текстом и вернуть его путь."""
    temp_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".xml", delete=False, encoding="utf-8"
    )
    temp_file.write(text)
    temp_file.close()
    return temp_file.name


class TestLoadVfs(unittest.TestCase):
    """Проверка загрузки VFS из XML-файлов."""

    def test_minimal_vfs(self):
        content = base64.b64encode(b"hello").decode("ascii")
        xml_text = '<vfs name="Test"><file name="a.txt">' + content + "</file></vfs>"
        path = make_temp_xml(xml_text)
        try:
            vfs_name, root = load_vfs(path)
        finally:
            os.remove(path)

        self.assertEqual(vfs_name, "Test")
        self.assertIn("a.txt", root.children)
        self.assertEqual(root.children["a.txt"].content, b"hello")
        self.assertFalse(root.children["a.txt"].is_dir)

    def test_nested_directories(self):
        content = base64.b64encode(b"data").decode("ascii")
        xml_text = (
            '<vfs name="Test">'
            '<directory name="a"><directory name="b">'
            '<file name="c.txt">' + content + "</file>"
            "</directory></directory></vfs>"
        )
        path = make_temp_xml(xml_text)
        try:
            vfs_name, root = load_vfs(path)
        finally:
            os.remove(path)

        node_a = root.children["a"]
        node_b = node_a.children["b"]
        node_c = node_b.children["c.txt"]
        self.assertTrue(node_a.is_dir)
        self.assertTrue(node_b.is_dir)
        self.assertEqual(node_c.content, b"data")

    def test_binary_content_round_trip(self):
        binary_data = bytes([0, 1, 2, 255, 254, 10, 13])
        content = base64.b64encode(binary_data).decode("ascii")
        xml_text = '<vfs name="Test"><file name="bin.dat">' + content + "</file></vfs>"
        path = make_temp_xml(xml_text)
        try:
            vfs_name, root = load_vfs(path)
        finally:
            os.remove(path)

        self.assertEqual(root.children["bin.dat"].content, binary_data)

    def test_missing_file_raises_error(self):
        with self.assertRaises(VfsError):
            load_vfs("no_such_vfs_file.xml")

    def test_invalid_xml_raises_error(self):
        path = make_temp_xml('<vfs name="Test"><file name="a">')
        try:
            with self.assertRaises(VfsError):
                load_vfs(path)
        finally:
            os.remove(path)

    def test_missing_name_attribute_raises_error(self):
        path = make_temp_xml('<vfs><file name="a.txt">aGk=</file></vfs>')
        try:
            with self.assertRaises(VfsError):
                load_vfs(path)
        finally:
            os.remove(path)

    def test_invalid_base64_raises_error(self):
        path = make_temp_xml('<vfs name="Test"><file name="a.txt">не_base64!!!</file></vfs>')
        try:
            with self.assertRaises(VfsError):
                load_vfs(path)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()