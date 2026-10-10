"""Поиск узлов в виртуальной файловой системе."""


class NavigationError(Exception):
    """Ошибка поиска пути в VFS."""


def split_path(path_text, current_parts):
    """Превратить текст пути в список имён от корня.

    Путь, начинающийся с "/", считается от корня, иначе от текущей
    папки. Части "." пропускаются, ".." поднимает на уровень выше.
    """
    if path_text.startswith("/"):
        parts = []
    else:
        parts = list(current_parts)

    for name in path_text.split("/"):
        if name == "" or name == ".":
            continue
        if name == "..":
            if len(parts) > 0:
                parts.pop()
        else:
            parts.append(name)
    return parts


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