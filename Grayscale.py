from PIL.Image import Image
from skimage import io, color
import os
import imghdr

source = r'/Users/machinegun/Downloads/Photos'
destination = r'/Users/machinegun/Downloads/Photos/Greyscale'
isExist = os.path.exists(destination)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(destination)
    print("The new directory is created!")

image_files = [os.path.join(root, filename)
               for root, dirs, files in os.walk(source)
               for filename in files
               if imghdr.what(os.path.join(root, filename))]

fileNumber = 0


def append_id(filename):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid="gray", ext=ext)


for fn in image_files:
    rgb = io.imread(fn)
    grey = color.rgb2gray(rgb)
    head, tail = os.path.split(fn)
    print(tail)
    grayName = append_id(tail)
    print("grayName: ", grayName)
    file_size = os.path.getsize(fn)
    print("File size is: ", file_size / 1000)
    if file_size / 1000 > 1500:
     io.imsave(os.path.join(destination, grayName), grey, quality=60)
    else:
        io.imsave(os.path.join(destination, grayName), grey, quality=70)


