import os
import re
from os.path import isfile, join, realpath


def enter_index(text, start=0, end=0):
    try:
        result = int(input(text))
        if result < start or end < result:
            raise IndexError(
                f"The selected input '{result}' was not in the given bounds [{start}, {end}]!"
            )
    except ValueError as exc:
        print(exc)
        result = enter_index("Please re-enter a valid input: ",
                             start=start,
                             end=end)
    except IndexError as exc:
        print(exc)
        result = enter_index("Please re-enter a valid input: ",
                             start=start,
                             end=end)

    return result


def select_file_in_path(path, constraint_re=""):
    if not os.path.isdir(path):
        raise NotADirectoryError(
            f"You did not supply a valid '{path=}' should be a directory!")

    files = [
        onefile for onefile in os.listdir(path) if isfile(join(path, onefile))
    ]
    if len(files) == 0:
        raise FileNotFoundError(f"No files in the given path!\n{path=}")

    if constraint_re:
        files = [f for f in files if re.match(constraint_re, f)]
        if len(files) == 0:
            raise FileNotFoundError(
                f"No files left after applying your constraints!\n{constraint_re=}"
            )

    print("")
    for index, filename in enumerate(files):
        print(f"[{index}] -> {filename}")
    print("")

    index = enter_index("Please enter the file number you want to select: ",
                        start=0,
                        end=len(files) - 1)

    return join(path, files[index])


def main():
    dir_path = os.path.dirname(realpath(__name__))

    result = select_file_in_path(dir_path, constraint_re=r"(\w+).py$")
    print("You selected:", result)


if __name__ == "__main__":
    main()
