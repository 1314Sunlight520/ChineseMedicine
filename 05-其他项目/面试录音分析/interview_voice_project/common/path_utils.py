import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# print(root_dir)


def get_file_path(relative_path):
    return os.path.join(root_dir, relative_path)


def get_file_extension(file_path):
    # Get the file extension (suffix) from the file path
    _, extension = os.path.splitext(file_path)
    return extension


if __name__ == '__main__':
    print(get_file_extension('aa/test.py'))
