"""Команды эмулятора."""

import time

from emulator.navigation import NavigationError, split_path, find_node
from emulator.vfs import VfsNode

class CommandError(Exception):
    """Ошибка выполнения команды."""


class ShellState:
    """Состояние эмулятора: VFS, текущая папка, время запуска."""

    def __init__(self):
        self.root = None
        self.current_parts = []
        self.start_time = time.time()

    def get_current_path(self):
        """Вернуть текущую папку в виде строки, например /home/user."""
        return "/" + "/".join(self.current_parts)


def need_vfs(state):
    """Проверить, что VFS загружена."""
    if state is None or state.root is None:
        raise CommandError("VFS не загружена")


def find_by_text(state, path_text):
    """Найти узел по тексту пути и вернуть (узел, список имён)."""
    parts = split_path(path_text, state.current_parts)
    try:
        node = find_node(state.root, parts)
    except NavigationError as error:
        raise CommandError(path_text + ": " + str(error))
    return node, parts


def cmd_ls(args, state):
    """Показать содержимое папки (по умолчанию текущей)."""
    need_vfs(state)
    if len(args) > 1:
        raise CommandError("ls: слишком много аргументов")

    if len(args) == 1:
        node, parts = find_by_text(state, args[0])
    else:
        node, parts = find_by_text(state, ".")

    if not node.is_dir:
        return node.name

    lines = []
    for name in sorted(node.children):
        if node.children[name].is_dir:
            lines.append(name + "/")
        else:
            lines.append(name)
    return "\n".join(lines)


def cmd_cd(args, state):
    """Перейти в другую папку (без аргументов - в корень)."""
    need_vfs(state)
    if len(args) > 1:
        raise CommandError("cd: слишком много аргументов")

    if len(args) == 0:
        state.current_parts = []
        return ""

    node, parts = find_by_text(state, args[0])
    if not node.is_dir:
        raise CommandError(args[0] + ": не папка")
    state.current_parts = parts
    return ""


def cmd_uptime(args, state):
    """Показать, сколько времени работает эмулятор."""
    if len(args) > 0:
        raise CommandError("uptime: команда не принимает аргументов")

    seconds = int(time.time() - state.start_time)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "up %02d:%02d:%02d" % (hours, minutes, seconds)


def cmd_tac(args, state):
    """Вывести строки файлов в обратном порядке."""
    need_vfs(state)
    if len(args) == 0:
        raise CommandError("tac: не указан файл")

    result = []
    for path_text in args:
        node, parts = find_by_text(state, path_text)
        if node.is_dir:
            raise CommandError(path_text + ": это папка")
        try:
            text = node.content.decode("utf-8")
        except UnicodeDecodeError:
            raise CommandError(path_text + ": не текстовый файл")
        lines = text.splitlines()
        lines.reverse()
        result.extend(lines)
    return "\n".join(result)

def cmd_touch(args, state):
    """Создать пустые файлы в VFS (только в памяти)."""
    need_vfs(state)
    if len(args) == 0:
        raise CommandError("touch: не указан файл")

    for path_text in args:
        parts = split_path(path_text, state.current_parts)
        if len(parts) == 0:
            continue

        try:
            parent = find_node(state.root, parts[:-1])
        except NavigationError as error:
            raise CommandError(path_text + ": " + str(error))
        if not parent.is_dir:
            raise CommandError(path_text + ": родитель не папка")

        name = parts[-1]
        if name not in parent.children:
            parent.children[name] = VfsNode(name, False)
    return ""

def cmd_exit(args):
    """Завершить работу эмулятора."""
    if len(args) > 0:
        raise CommandError("exit: команда не принимает аргументов")
    return "exit"


def cmd_conf_dump(args, config):
    """Вывести параметры запуска в формате ключ=значение."""
    if len(args) > 0:
        raise CommandError("conf-dump: команда не принимает аргументов")
    if config is None:
        raise CommandError("conf-dump: нет параметров запуска")
    params = config.as_dict()
    lines = []
    for key in params:
        lines.append(key + "=" + params[key])
    return "\n".join(lines)


def execute(command, args, config=None, state=None):
    """Выполнить команду и вернуть текст результата."""
    if command == "ls":
        return cmd_ls(args, state)
    elif command == "cd":
        return cmd_cd(args, state)
    elif command == "uptime":
        return cmd_uptime(args, state)
    elif command == "tac":
        return cmd_tac(args, state)
    elif command == "touch":
        return cmd_touch(args, state)
    elif command == "exit":
        return cmd_exit(args)
    elif command == "conf-dump":
        return cmd_conf_dump(args, config)
    else:
        raise CommandError("неизвестная команда: " + command)