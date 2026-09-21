"""Конфигурация эмулятора."""


class EmulatorConfig:
    """Хранит параметры запуска эмулятора."""

    def __init__(self, vfs_path=None):
        self.vfs_path = vfs_path

    def get_vfs_name(self):
        """Вернуть имя VFS для показа в заголовке окна."""
        if self.vfs_path is None:
            return "no-vfs"
        return self.vfs_path
