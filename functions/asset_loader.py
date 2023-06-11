from fnmatch import fnmatch
import os


# currently not universal at all, files with same name in different folders will be overwritten
def get_path(folder, file):
    for root, dirs, files in os.walk(folder):
        return itterate(files, folder, file)


def itterate(file_list, folder, file):
    abs_path = os.path.abspath(os.getcwd())

    for name in file_list:
        if fnmatch(name, file):
            return os.path.join(abs_path, folder, name).replace('\\', '/')