from pathlib import Path

def reduce_path_string(path):

    path = Path(path)
    parts: tuple = path.parts

    if len(parts) > 1:
        return str(Path(*parts[-2:]))
    else:
        return str(path)


# print(reduce_path_string("c:/test.txt"))
# print(reduce_path_string("c://bar//foo//test.txt"))
# print(reduce_path_string("c://map/foo//temp\\file.txt"))
    