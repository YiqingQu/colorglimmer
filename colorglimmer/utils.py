from colorglimmer import settings
import cv2
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os
from colorglimmer import settings
import math

def calculate_RGB(image_path):
    # load the image
    image = cv2.imread(image_path)

    # Transform to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Extract R, G, B Channel
    red, green, blue = image_rgb[:, :, 0], image_rgb[:, :, 1], image_rgb[:, :, 2]
    return red, green, blue

def calculate_grayscale_histogram(image_path):
    # load the image
    image = cv2.imread(image_path)

    # transform the image into grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # calculate the grayscale histogram
    histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    return histogram.flatten()


def recolor_image(image_path, file_name, new_colors):
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size

    red_color = (255, 0, 0)
    green_color = (0, 255, 0)

    for x in range(width):
        for y in range(height):
            if is_close_to_color(pixels[x, y], red_color, threshold=150):
                pixels[x, y] = tuple(new_colors["red"])
            elif is_close_to_color(pixels[x, y], green_color, threshold=200):
                pixels[x, y] = tuple(new_colors["green"])



    file_name = "modified_" + file_name
    img.save(settings.MEDIA_ROOT + file_name)
    return settings.MEDIA_ROOT + file_name, file_name

def euclidean_distance(color1, color2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(color1, color2)]))

def is_close_to_color(pixel, target_color, threshold=1000):
    return euclidean_distance(pixel, target_color) < threshold


def simulate_deuteranopia(image_path, file_name):
    """
    Turn the image into color-weakness view
    Param:
            image_path: the path to the expected image
    """
    red, green, blue = calculate_RGB(image_path)

    # Simulation
    red_green_avg = 0.5 * red + 0.5 * green
    red[:] = red_green_avg
    green[:] = red_green_avg

    # Merge channels
    simulated_image = np.stack((red, green, blue), axis=-1)

    # Save the simulation image
    simulated_image_pil = Image.fromarray(simulated_image)
    file_name = "deuteranopia_" + file_name
    simulated_image_pil.save(settings.MEDIA_ROOT + file_name)
    return settings.MEDIA_ROOT + file_name, file_name




def calculate_histogram(image_path, bins=256):
    """
    Calculate the histogram using
    """
    image = cv2.imread(image_path)
    # Transform to HSV space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Calculate the histogram
    hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
    # Normalization
    hist = cv2.normalize(hist, hist).flatten()
    return hist


def compare_histograms(hist1, hist2, method=cv2.HISTCMP_CORREL):
    """
    Campare between histograms
    """
    return cv2.compareHist(hist1, hist2, method)


def calculate_ssim(image_path_1, image_path_2):
    """
    Calculate the ssim similarity
    """
    image1 = cv2.imread(image_path_1)
    image2 = cv2.imread(image_path_2)
    ssim_value = ssim(image1, image2, multichannel=True, win_size=3)
    return ssim_value