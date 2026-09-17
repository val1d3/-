"""Графическое окно эмулятора (REPL)."""

import tkinter

from emulator.parser import parse_line, split_command, ParserError
from emulator.commands import execute, CommandError


class EmulatorApp:
    """Главное окно эмулятора."""

    def __init__(self, config):
        self.config = config

        self.window = tkinter.Tk()
        self.window.title(config.get_vfs_name())

        self.output_box = tkinter.Text(self.window, height=20, width=80)
        self.output_box.pack()

        self.input_box = tkinter.Entry(self.window, width=80)
        self.input_box.pack()
        self.input_box.bind("<Return>", self.on_enter_pressed)

    def print_line(self, text):
        """Добавить строку текста в область вывода."""
        self.output_box.insert(tkinter.END, text + "\n")

    def on_enter_pressed(self, event):
        """Обработать нажатие Enter: разобрать и выполнить команду."""
        line = self.input_box.get()
        self.input_box.delete(0, tkinter.END)

        self.print_line("$ " + line)

        try:
            tokens = parse_line(line)
        except ParserError as error:
            self.print_line("ошибка: " + str(error))
            return

        if len(tokens) == 0:
            return

        command, args = split_command(tokens)

        try:
            result = execute(command, args)
        except CommandError as error:
            self.print_line("ошибка: " + str(error))
            return

        if result == "exit":
            self.window.destroy()
        else:
            self.print_line(result)

    def run(self):
        """Запустить окно приложения."""
        self.window.mainloop()
