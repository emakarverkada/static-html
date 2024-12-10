import os
import shutil

def cp_directory(from_path, dest_path):
    shutil.rmtree(dest_path)
    shutil.copytree(from_path, dest_path)