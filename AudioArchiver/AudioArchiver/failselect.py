import os
from os.path import isfile, join, realpath


def enter_index(text, start=0, end=0):
    try:
        result = int(input(text))
        if result < start or end < result:
            raise IndexError(
                f"The selected input '{result}' was not in the given bounds!")
    except ValueError as e:
        print(e)
        result = enter_index("Please re-enter a valid input: ",
                             start=start,
                             end=end)
    except IndexError as e:
        print(e)
        result = enter_index("Please re-enter a valid input: ",
                             start=start,
                             end=end)

    return result


def select_file_in_path(path):
    if not os.path.isdir(path):
        raise NotADirectoryError(
            f"You did not supply a valid '{path=}' should be a directory!")

    files = [
        onefile for onefile in os.listdir(path) if isfile(join(path, onefile))
    ]

    for index, f in enumerate(files):
        print(f"[{index}] {f}")
    index = enter_index("Please enter the files number you want to select: ",
                        start=0,
                        end=len(files) - 1)

    return join(path, files[index])


def main():
    dir_path = os.path.dirname(realpath(__file__))

    result = select_file_in_path(dir_path)
    print(result)


if __name__ == "__main__":
    main()
