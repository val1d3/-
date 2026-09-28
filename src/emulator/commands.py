"""Команды эмулятора: ls, cd, exit и conf-dump."""


class CommandError(Exception):
    """Ошибка выполнения команды: неизвестная команда или неверные аргументы."""
    pass


def cmd_ls(args):
    """Команда-заглушка ls: возвращает текст с именем команды и аргументами."""
    text = "ls"
    for arg in args:
        text = text + " " + arg
    return text


def cmd_cd(args):
    """Команда-заглушка cd: возвращает текст с именем команды и аргументами."""
    text = "cd"
    for arg in args:
        text = text + " " + arg
    return text


def cmd_exit(args):
    """Команда exit: не принимает аргументов."""
    if len(args) > 0:
        raise CommandError("команда exit не принимает аргументов")
    return "exit"


def cmd_conf_dump(args, config):
    """Служебная команда conf-dump: выводит параметры эмулятора.

    Формат вывода: по одной строке вида ключ=значение на каждый параметр.
    """
    if len(args) > 0:
        raise CommandError("команда conf-dump не принимает аргументов")
    if config is None:
        raise CommandError("конфигурация недоступна")

    params = config.as_dict()
    lines = []
    for key in params:
        lines.append(key + "=" + params[key])
    return "\n".join(lines)


def execute(command, args, config=None):
    """Найти нужную команду по имени и выполнить её."""
    if command == "ls":
        result = cmd_ls(args)
    elif command == "cd":
        result = cmd_cd(args)
    elif command == "exit":
        result = cmd_exit(args)
    elif command == "conf-dump":
        result = cmd_conf_dump(args, config)
    else:
        raise CommandError("неизвестная команда: " + command)

    return result