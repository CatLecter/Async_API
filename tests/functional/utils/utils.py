import os


def names_file(path: str):
    """Возвращает лист с названием файлов в папке."""

    files = os.walk(path)
    list_idx = []
    for idx in files:
        list_idx = idx[2]
    return [_.split(".")[0] for _ in list_idx]
