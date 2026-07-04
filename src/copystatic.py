import os
import shutil


def copy_files_recursive(source_dir_path: str, dest_dir_path: str) -> None:
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def copy_dir_tree(source_dir: str, dest_dir: str) -> None:
    shutil.rmtree(dest_dir, ignore_errors=True)

    if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
        raise Exception(f"{source_dir=} does not exist or is not a directory")

    copy_files_recursive(source_dir, dest_dir)


