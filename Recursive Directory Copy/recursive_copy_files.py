import os
import glob
import shutil

def recursive_copy_files(source_path, destination_path, override=False):
#
#Recursively copies files from source  to destination directory.
#:param source_path: source directory
#:param destination_path: destination directory
#:param override if True all files will be overwritten otherwise skip if file exist
#:return: count of copied files
#

    files_count = 0

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    items = glob.glob(source_path + '/*')

    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            if not os.path.exists(file) or override:
                #Copy file
                shutil.copyfile(item, file)
                files_count += 1
    return files_count

if __name__ == "__main__":
    recursive_copy_files("./test", "./replica_test_1", override = False)
    recursive_copy_files("./test", "./replica_test_2", override = False)
