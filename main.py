import numpy as np
import random
import os
import shutil
import touch
from source import Data

path = "/home/nikita/Изображения/Mask"  # папочка с исходными данными(картинки)
path_of_output = "/home/nikita/Изображения/Results"  # папочка, куда будут закидываться результаты
if not os.path.exists(path_of_output):
    os.mkdir(path_of_output)
a = []
for root, dirs, files in os.walk(path):
    for file in files:
        try:
            a.append(os.path.join(root, file))
        except:
            continue
print("The size of batch:")
m = int(input())
last = ""
while last != 'Y' and last != 'y' and last != 'N' and last != 'n':
    print("Forsake last batch [y/n]?")
    last = input()
rez = Data(arr=a, k=m, incomp=(last == 'Y' or last == 'y'))
number_of_batch = 0
for batch in rez:
    # какая-то обработка (я просто закидываю в результирующую папку с характерным переименованием)
    number_of_batch += 1
    number_of_image = 0
    for image in batch:
        number_of_image += 1
        new_address = os.path.join(path_of_output, str(number_of_batch) + "." + str(number_of_image) + ".jpg")
        shutil.copy(image, new_address)
