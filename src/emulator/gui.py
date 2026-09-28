"""Графическое окно эмулятора (REPL)."""

import tkinter

from emulator.parser import parse_line, split_command, ParserError
from emulator.commands import execute, CommandError
from emulator.script import read_script_lines, ScriptError


class EmulatorApp:
    """Главное окно эмулятора."""

    def __init__(self, config):
        self.config = config
        self.exit_requested = False

        self.window = tkinter.Tk()
        self.window.title(config.get_vfs_name())

        self.output_box = tkinter.Text(self.window, height=20, width=80)
        self.output_box.pack()

        self.input_box = tkinter.Entry(self.window, width=80)
        self.input_box.pack()
        self.input_box.bind("<Return>", self.on_enter_pressed)

        self.print_startup_params()

        if config.script_path is not None:
            self.run_script(config.script_path)

    def print_line(self, text):
        """Добавить строку текста в область вывода."""
        self.output_box.insert(tkinter.END, text + "\n")

    def print_startup_params(self):
        """Вывести в окно все параметры, с которыми запущен эмулятор."""
        self.print_line("--- параметры запуска ---")
        params = self.config.as_dict()
        for key in params:
            self.print_line(key + "=" + params[key])
        self.print_line("-------------------------")

    def run_line(self, line):
        """Разобрать и выполнить одну строку команды.

        Ошибки выводятся в окно, работа программы при этом не прерывается.
        Если выполнена команда exit, выставляется флаг exit_requested.
        """
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
        """Выполнить стартовый скрипт построчно, как будто команды ввели вручную.

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