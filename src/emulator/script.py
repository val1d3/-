"""Чтение стартового скрипта эмулятора."""


class ScriptError(Exception):
    """Ошибка чтения файла стартового скрипта."""
    pass


def read_script_lines(path):
    """Прочитать файл скрипта и вернуть список непустых строк.

    Пустые строки пропускаются. Если файл нельзя открыть или прочитать,
    выбрасывается ScriptError.
    """
    try:
        with open(path, "r", encoding="utf-8") as script_file:
            all_lines = script_file.readlines()
    except (OSError, UnicodeDecodeError) as error:
        raise ScriptError(
            "не удалось прочитать скрипт " + path + ": " + str(error)
        )

    lines = []
    for raw_line in all_lines:
        line = raw_line.strip()
        if line != "":
            lines.append(line)

    return lines