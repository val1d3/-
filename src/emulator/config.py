"""Конфигурация эмулятора."""


class EmulatorConfig:
    """Хранит параметры запуска эмулятора."""

    def __init__(self, vfs_path=None):
        self.vfs_path = vfs_path
        self.vfs_name = "VFS"  # имя VFS, пока просто зафиксировано в коде

    def get_vfs_name(self):
        """Вернуть имя VFS для показа в заголовке окна."""
        return self.vfs_nam
