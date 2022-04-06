#!/usr/bin/env python
"""Compare two aligned images of the same size.

Usage: python compare.py first-image second-image
"""

import io
import os

# from io import imread
import sys

# from scipy.misc import imread
import scipy.misc

# from scipy.misc.pilutil import imread
import numpy as np
from scipy import misc
from skimage import data
import skimage
from scipy.linalg import norm
from scipy import sum, average

# import cv2
# image = cv2.imread('Sample.png')

# load and show an image with Pillow
from PIL import Image

# Open the image form working directory

## summarize some details about the image
# print(image.format)
# print(image.size)
# print(image.mode)
## show the image
# image.show()


def read2(filename, searched_variable_description):
    """Assumes you write:
    sender_email=<youremailaddress>
    password=<youremailpassword>
    """
    ffile = open(filename, "r").read()

    ini = ffile.find(searched_variable_description) + (
        len(searched_variable_description) + 1
    )
    rest = ffile[ini:]
    search_enter = rest.find("\n")
    result = rest[:search_enter]
    return result


def is_changed(filename1, filename2):
    if os.path.isfile(filename1) and os.path.isfile(filename2):
        m_norm, z_norm = compare(filename1, filename2)
        if m_norm == 0:
            return False
        else:
            return True
    else:
        return False


def compare(filename1, filename2):
    file1 = filename1
    file2 = filename2
    # read images as 2D arrays (convert to grayscale for simplicity)
    # image1 = io.imread(file1)
    image1 = Image.open("old_tickets.png")
    img1 = skimage.img_as_float(image1)
    # image2 = io.imread(file2)
    image2 = Image.open("tickets.png")
    img2 = skimage.img_as_float(image2)
    # img1 = to_grayscale(imread(file1).astype(float))
    # img2 = to_grayscale(imread(file2).astype(float))
    # compare
    n_m, n_0 = compare_images(img1, img2)
    print("Manhattan norm:", n_m, "/ per pixel:", n_m / img1.size)
    print("Zero norm:", n_0, "/ per pixel:", n_0 * 1.0 / img1.size)
    return n_m, n_0


def compare_images(img1, img2):
    # normalize to compensate for exposure difference
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)


def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr


def normalize(arr):
    rng = arr.max() - arr.min()
    amin = arr.min()
    return (arr - amin) * 255 / rng
