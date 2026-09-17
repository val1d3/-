"""Команды эмулятора: ls, cd и exit."""


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


def execute(command, args):
    """Найти нужную команду по имени и выполнить её."""
    if command == "ls":
        result = cmd_ls(args)
    elif command == "cd":
        result = cmd_cd(args)
    elif command == "exit":
        result = cmd_exit(args)
    else:
        raise CommandError("неизвестная команда: " + command)

    return result
