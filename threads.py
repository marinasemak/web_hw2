from pathlib import Path
import os
import shutil
import concurrent.futures
import logging
from collections import defaultdict


cwd = Path.cwd()


def list_files_walk(start_path="."):
    """
    Iterate through folders and subfolders and gets list of files
    """
    list_with_files = defaultdict(list)
    for root, dirs, files in os.walk(start_path):
        for file in files:
            file_to_copy = os.path.join(root, file)
            dir_name = Path(file).suffix.lstrip(".")
            list_with_files[dir_name].append(file_to_copy)
    return list_with_files


def copy_files(dir_name, files, dist_path="."):
    """
    Copy file from source to destination and sorting them by extensions
    """
    path_to_dir = cwd / dist_path / dir_name
    path_to_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        logging.debug(f"Copying file: {file}")
        shutil.copy(file, path_to_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    start_path = Path("picture")
    dist_path = Path("dist")

    # Get the list of all files
    list_with_files = list_files_walk(start_path)

    # Start copying files in thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:

        for key, values in list_with_files.items():
            executor.submit(copy_files, key, values, dist_path)
