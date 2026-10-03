"""Загрузка виртуальной файловой системы (VFS) из XML-файла."""

import base64
import xml.etree.ElementTree as ElementTree


class VfsError(Exception):
    """Ошибка загрузки VFS: файл не найден или неверный формат."""
    pass


class VfsNode:
    """Один узел VFS: каталог или файл.

    Атрибуты:
        name - имя узла;
        is_dir - True для каталога, False для файла;
        children - словарь {имя: VfsNode}, заполнен только у каталогов;
        content - содержимое файла в виде байтов, заполнено только у файлов.
    """

    def __init__(self, name, is_dir):
        self.name = name
        self.is_dir = is_dir
        self.children = {}
        self.content = b""


def build_node(element):
    """Построить VfsNode из одного XML-элемента directory или file."""
    name = element.get("name")
    if name is None:
        raise VfsError("у элемента " + element.tag + " нет атрибута name")

    if element.tag == "directory":
        node = VfsNode(name, True)
        for child_element in element:
            child_node = build_node(child_element)
            node.children[child_node.name] = child_node
        return node

    if element.tag == "file":
        node = VfsNode(name, False)
        text = element.text
        if text is None:
            text = ""
        text = text.strip()
        try:
            node.content = base64.b64decode(text)
        except ValueError as error:
            raise VfsError("неверные base64-данные в файле " + name + ": " + str(error))
        return node

    raise VfsError("неизвестный элемент в VFS: " + element.tag)


def load_vfs(path):
    """Загрузить VFS из XML-файла, вернуть пару (имя VFS, корневой каталог).

    Все данные загружаются в память целиком, обращений к диску после
    этой функции больше не происходит. Если файл не найден, повреждён
    или не соответствует формату, выбрасывается VfsError.
    """
    try:
        tree = ElementTree.parse(path)
    except OSError as error:
        raise VfsError("не удалось открыть VFS " + path + ": " + str(error))
    except ElementTree.ParseError as error:
        raise VfsError("неверный формат VFS " + path + ": " + str(error))

    root_element = tree.getroot()
    if root_element.tag != "vfs":
        raise VfsError("корневой элемент VFS должен называться vfs")

    vfs_name = root_element.get("name")
    if vfs_name is None:
        raise VfsError("у элемента vfs нет атрибута name")

    root_node = VfsNode("/", True)
    for child_element in root_element:
        child_node = build_node(child_element)
        root_node.children[child_node.name] = child_node

    return vfs_name, root_node