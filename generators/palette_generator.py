# Taken and modified from: https://github.com/sw385/Palette-Generator/blob/master/palette_generator.py
import os
from PIL import Image, ImageDraw, ImageFont
from numpy import array
from scipy.cluster.vq import kmeans
import numpy
from generators.web_info import WebColors

INPUT_DIR = 'images'
MAX_COLORS = 5  # 6 colors in a palette is plenty, no need for more.

def dirs_to_process():
    '''Return a list of paths of directories in INPUT_DIR that do not exist in OUTPUT_DIR.
        Do NOT create the corresponding output directories yet.'''
    input_dirs = os.listdir(INPUT_DIR)
    new_dirs = [f for f in input_dirs]
    return new_dirs
    
def images_to_process(directory):
    '''Given a path to a directory, return a list of paths of images in that directory.'''
    contents = os.listdir(os.path.join(INPUT_DIR, directory))
    images = []
    for file in contents:
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            images.append(os.path.join(INPUT_DIR, directory, file))
    return images
    
def images_to_array(full_image_paths):
    '''Given a list of full image paths (dir + filename),
        resize it and return it as an array.'''
    temp = []
    for image_path in full_image_paths:
      im = Image.open(image_path)
      RESIZE_WIDTH = 128  # 256 makes the program run really slow and doesn't really seem all that necessary anyway.
      im = im.resize((RESIZE_WIDTH, RESIZE_WIDTH))

      for y in range(0 , im.size[1]):
          for x in range(0 , im.size[0]):
              color = im.getpixel((x, y))
              temp.append([color[0], color[1], color[2]])
    temp = array(temp)
    return temp
    
def generate_palette(array, centroids):
    '''Given an array and a number of centroids, returns a list of colors.'''
    palette = []
    result = kmeans(array.astype(float), centroids)
    for centroid in numpy.array(result[0]).tolist():
        centroid = (int(centroid[0]), int(centroid[1]), int(centroid[2]))
        palette.append(tuple(centroid))
    return palette

def generate_pallete_from_imgs():
    '''Given a path to a directory, process all the images in that directory.'''
    input_dirs = dirs_to_process()
    input_images = []
    for dir in input_dirs:
        input_images.extend(images_to_process(dir))
    if len(input_images) == 0:
        print("No images found")
        return [WebColors.get_random_value() for _ in range(5)]
    array = images_to_array(input_images)
    pallete = generate_palette(array, MAX_COLORS)
    return pallete