import os
import shutil

#shutil.copy()

x = os.scandir(".")
for file in x:
    print(file.name)