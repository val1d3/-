"""Разбор строк, введённых пользователем, на команду и аргументы."""

import shlex

class ParserError(Exception):
    pass

def parse_line(line):
    line = line.strip() #стирка ненужных пробелов по краям

    if line == "":
        return [] 
      
    try:
        fullslova = shlex.split(line)
    except ValueError:
        raise ParserError("не закрыта кавычка в команде")
    return fullslova

def split_command(fullslova):
    if len(fullslova) == 0:
        return "", []
    command = fullslova[0]
    args = []
    for i in range(1, len(fullslova)):
        args.append(fullslova[i])
    return command, args
