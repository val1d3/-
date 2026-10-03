"""Графическое окно эмулятора (REPL)."""

import tkinter

from emulator.parser import parse_line, split_command, ParserError
from emulator.commands import execute, CommandError
from emulator.script import read_script_lines, ScriptError
from emulator.vfs import load_vfs, VfsError


class EmulatorApp:
    """Главное окно эмулятора."""

    def __init__(self, config):
        self.config = config
        self.exit_requested = False
        self.vfs_name = None
        self.vfs_root = None

        self.window = tkinter.Tk()
        self.window.title(config.get_vfs_name())

        self.output_box = tkinter.Text(self.window, height=20, width=80)
        self.output_box.pack()

        self.input_box = tkinter.Entry(self.window, width=80)
        self.input_box.pack()
        self.input_box.bind("<Return>", self.on_enter_pressed)

        self.load_vfs_if_needed()
        self.print_startup_params()

        if config.script_path is not None:
            self.run_script(config.script_path)

    def print_line(self, text):
        """Добавить строку текста в область вывода."""
        self.output_box.insert(tkinter.END, text + "\n")

    def load_vfs_if_needed(self):
        """Загрузить VFS в память, если задан путь к ней.

        При успешной загрузке заголовок окна меняется на имя VFS из
        XML-файла. Если загрузка не удалась, выводится сообщение об
        ошибке, а заголовок остаётся прежним.
        """
        if self.config.vfs_path is None:
            return

        try:
            vfs_name, vfs_root = load_vfs(self.config.vfs_path)
        except VfsError as error:
            self.print_line("ошибка: " + str(error))
            return

        self.vfs_name = vfs_name
        self.vfs_root = vfs_root
        self.window.title(vfs_name)

    def print_startup_params(self):
        """Вывести в окно все параметры, с которыми запущен эмулятор."""
        self.print_line("--- параметры запуска ---")
        params = self.config.as_dict()
        for key in params:
            self.print_line(key + "=" + params[key])
        self.print_line("-------------------------")

    def run_line(self, line):
        """Разобрать и выполнить одну строку команды."""
        try:
            tokens = parse_line(line)
        except ParserError as error:
            self.print_line("ошибка: " + str(error))
            return

        if len(tokens) == 0:
            return

        command, args = split_command(tokens)

        try:
            result = execute(command, args, self.config)
        except CommandError as error:
            self.print_line("ошибка: " + str(error))
            return

        if result == "exit":
            self.exit_requested = True
        else:
            self.print_line(result)

    def run_script(self, path):
        """Выполнить стартовый скрипт построчно, как диалог с пользователем.

        Для каждой строки сначала выводится ввод, затем результат.
        Ошибочные строки пропускаются, выполнение идёт дальше.
        Если сам файл скрипта прочитать нельзя, выводится сообщение об ошибке.
        """
        try:
            lines = read_script_lines(path)
        except ScriptError as error:
            self.print_line("ошибка: " + str(error))
            return

        for line in lines:
            self.print_line("$ " + line)
            self.run_line(line)
            if self.exit_requested:
                break

    def on_enter_pressed(self, event):
        """Обработать нажатие Enter: выполнить введённую команду."""
        line = self.input_box.get()
        self.input_box.delete(0, tkinter.END)

        self.print_line("$ " + line)
        self.run_line(line)

        if self.exit_requested:
            self.window.destroy()

    def run(self):
        """Запустить окно приложения."""
        if self.exit_requested:
            self.window.destroy()
        else:
            self.window.mainloop()