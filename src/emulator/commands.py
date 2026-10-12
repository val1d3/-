"""Команды эмулятора."""

import time

from emulator.navigation import NavigationError, find_node, resolve_path
from emulator.vfs import VfsNode

KILO = 1024
DIR_SIZE = 4096


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
    try:
        return resolve_path(state.root, state.current_parts, path_text)
    except NavigationError as error:
        raise CommandError(path_text + ": " + str(error))


def parse_ls_args(args):
    """Разделить аргументы ls на буквы опций и пути."""
    letters = ""
    paths = []
    for arg in args:
        if arg.startswith("-") and len(arg) > 1:
            for letter in arg[1:]:
                if letter not in "lha":
                    raise CommandError("ls: неизвестная опция: -" + letter)
                letters += letter
        else:
            paths.append(arg)
    return letters, paths


def get_size(node):
    """Размер узла в байтах (для папки условно 4096)."""
    if node.is_dir:
        return DIR_SIZE
    return len(node.content)


def format_size(size, human):
    """Записать размер числом или в виде 4.0K, 1.5M (для опции -h)."""
    if not human:
        return str(size)
    value = float(size)
    for unit in ["", "K", "M", "G"]:
        if value < KILO or unit == "G":
            if unit == "":
                return str(size)
            return "%.1f%s" % (value, unit)
        value = value / KILO


def format_long_lines(entries, human):
    """Собрать строки подробного списка для ls -l."""
    sizes = []
    for name, node in entries:
        sizes.append(format_size(get_size(node), human))
    width = max(len(text) for text in sizes)

    lines = []
    for i in range(len(entries)):
        name, node = entries[i]
        kind = "d" if node.is_dir else "-"
        moment = time.strftime("%Y-%m-%d %H:%M",
                               time.localtime(node.mtime))
        if node.is_dir:
            name = name + "/"
        lines.append(kind + " " + sizes[i].rjust(width) + " "
                     + moment + " " + name)
    return lines


def collect_entries(state, node, parts, letters):
    """Собрать список (имя, узел) для вывода ls."""
    if not node.is_dir:
        return [(node.name, node)]

    show_all = "a" in letters
    entries = []
    if show_all:
        entries.append((".", node))
        entries.append(("..", find_node(state.root, parts[:-1])))
    for name in sorted(node.children):
        if show_all or not name.startswith("."):
            entries.append((name, node.children[name]))
    return entries


def format_short_lines(entries):
    """Собрать строки обычного списка: у папок в конце стоит /."""
    lines = []
    for name, node in entries:
        if node.is_dir:
            name = name + "/"
        lines.append(name)
    return lines


def cmd_ls(args, state):
    """Показать содержимое папки; опции: -l подробно, -h, -a скрытые."""
    need_vfs(state)
    letters, paths = parse_ls_args(args)
    if len(paths) > 1:
        raise CommandError("ls: слишком много аргументов")

    path_text = "."
    if len(paths) == 1:
        path_text = paths[0]
    node, parts = find_by_text(state, path_text)
    entries = collect_entries(state, node, parts, letters)

    if len(entries) == 0:
        return ""
    if "l" in letters:
        return "\n".join(format_long_lines(entries, "h" in letters))
    return "\n".join(format_short_lines(entries))


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


def touch_path(state, path_text):
    """Создать файл по пути или обновить время изменения у узла."""
    head, slash, name = path_text.rpartition("/")
    if name == "" or name == "." or name == "..":
        node, parts = find_by_text(state, path_text)
        node.mtime = time.time()
        return

    dir_text = "."
    if head != "":
        dir_text = head
    elif slash != "":
        dir_text = "/"
    parent, parts = find_by_text(state, dir_text)
    if not parent.is_dir:
        raise CommandError(path_text + ": родитель не папка")

    if name in parent.children:
        parent.children[name].mtime = time.time()
    else:
        parent.children[name] = VfsNode(name, False)


def cmd_touch(args, state):
    """Создать пустой файл или обновить время изменения (в памяти)."""
    need_vfs(state)
    if len(args) == 0:
        raise CommandError("touch: не указан файл")

    for path_text in args:
        touch_path(state, path_text)
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