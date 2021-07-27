# importing numpy
import numpy as np


# importing io from skimage
from skimage import io
import cv2


try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

import PIL.ImageOps
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# define imshow ; shows array as image
def imshow(array):
    io.imshow(array)
    io.show()


# define ridopac ; get rid of opacity layer in image, if there is
def ridopac(array):
    if np.shape(array)[2] == 3:
        pass
    else:
        mask_array = 255*(1-np.ceil(array[:, :, 3]/255)).astype(int)
        null_array = np.dstack((mask_array, mask_array, mask_array))
        array = array[:, :, 0:3] - null_array

    array[array < 0] = 0
    return array


# define flip ; flips the image on a horizontal axis
def hflip(array):
    flipped_array = np.flip(array, 0)
    return flipped_array


# define get_top_corner ; gets the left-most top corner of the non-blank part of an image
def get_top_corner(array):
    nz_array = np.nonzero(array)
    top_corner = [np.amin(nz_array[:][0]), np.amin(nz_array[:][1])]
    # print("rant")
    return top_corner


# define get_bottom_corner ; gets the right-most bottom corner of the non-blank part of an image
def get_bottom_corner(array):
    nz_array = np.nonzero(array)
    bot_corner = [np.amax(nz_array[:][0]), np.amax(nz_array[:][1])]
    # print("ranb")
    return bot_corner


# define crop ; crops an image given the top-left corner and bottom-right corner
def crop(array, top_corner, bottom_corner):
    result = array[top_corner[0]:bottom_corner[0], top_corner[1]:bottom_corner[1]]
    return result


def grayscale(array):
    return 0.299*array[:, :, 0] + 0.587*array[:, :, 1] + 0.114*array[:, :, 2]
