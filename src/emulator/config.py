"""Конфигурация эмулятора."""

import argparse


class EmulatorConfig:
    """Хранит параметры запуска эмулятора.

    Атрибуты:
        vfs_path - путь к физическому расположению VFS (или None);
        script_path - путь к стартовому скрипту (или None);
        vfs_name - имя VFS для заголовка окна, пока зафиксировано в коде.
    """

    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path
        self.script_path = script_path
        self.vfs_name = "MyVFS"

    def get_vfs_name(self):
        """Вернуть имя VFS для показа в заголовке окна."""
        return self.vfs_name

    def as_dict(self):
        """Вернуть параметры запуска в виде словаря ключ-значение.

        Если параметр не задан, вместо None подставляется пустая строка.
        """
        params = {}

        if self.vfs_path is None:
            params["vfs_path"] = ""
        else:
            params["vfs_path"] = self.vfs_path

        if self.script_path is None:
            params["script_path"] = ""
        else:
            params["script_path"] = self.script_path

        return params


def parse_args(argv):
    """Разобрать параметры командной строки и вернуть EmulatorConfig.

    Поддерживаются параметры --vfs-path и --script. Список argv
    обычно берётся из sys.argv[1:].
    """
    parser = argparse.ArgumentParser(
        description="Эмулятор командной оболочки UNIX-подобной ОС."
    )
    parser.add_argument(
        "--vfs-path",
        default=None,
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        default=None,
        help="путь к стартовому скрипту с командами эмулятора",
    )
    args = parser.parse_args(argv)
    return EmulatorConfig(vfs_path=args.vfs_path, script_path=args.script)