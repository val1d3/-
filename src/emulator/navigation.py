"""Поиск узлов в виртуальной файловой системе."""


class NavigationError(Exception):
    """Ошибка поиска пути в VFS."""


def find_node(root, parts):
    """Пройти по списку имён от корня и вернуть найденный узел."""
    node = root
    for name in parts:
        if not node.is_dir:
            raise NavigationError("не папка: " + node.name)
        if name not in node.children:
            raise NavigationError("нет такого файла или папки: " + name)
        node = node.children[name]
    return node


def resolve_path(root, current_parts, path_text):
    """Найти узел по тексту пути, проверяя каждую часть пути.

    Путь, начинающийся с "/", считается от корня, иначе от текущей
    папки. Часть "." означает текущую папку, ".." - родительскую.
    Как в настоящей оболочке, каждая промежуточная папка должна
    существовать, даже если дальше путь возвращается через "..".
    Возвращает узел и список имён от корня до него.
    """
    if path_text.startswith("/"):
        parts = []
    else:
        parts = list(current_parts)
    node = find_node(root, parts)

    for name in path_text.split("/"):
        if name == "" or name == ".":
            continue
        if not node.is_dir:
            raise NavigationError("не папка: " + node.name)
        if name == "..":
            if len(parts) > 0:
                parts.pop()
                node = find_node(root, parts)
        else:
            if name not in node.children:
                raise NavigationError(
                    "нет такого файла или папки: " + name)
            node = node.children[name]
            parts.append(name)
    return node, parts