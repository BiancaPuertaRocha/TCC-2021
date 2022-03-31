
import rpyc
import numpy as np
import cv2
import math
import time
import utils

import mask
from support_functions import Support
from numpy.polynomial import polynomial as P
from image_processing import ImagePrecessing
 
class ProcessingByImage(ImagePrecessing):

    def generate_panoramic(self,image):
        print("generating panoramic image...")
        with open("x.png","wb") as file:
            file.write(image)
        im = cv2.imread("x.png")
        img = utils.cortar_imagem_quadrada(im)
        return super().generate_panoramic(img)
   
    def use_mask(self,image):
        print("using mask...")
        with open("x.png","wb") as file:
            file.write(image)
        img = cv2.imread("x.png")
        return super().use_mask(img)
   
    def generate_birds_eye(self,image, distParams, angParams, centerCol,  centerLine):
        print("generating birds eye view...")
        with open("x.png","wb") as file:
            file.write(image)
        img = cv2.imread("x.png")
        return super().generate_birds_eye(img, distParams, angParams, centerCol,  centerLine)
   
    def get_image_with_boxes(self,im_bytes):
        print("detecting objects and returning boxes...")
        with open("x.png","wb") as file:
            file.write(im_bytes)
        image = cv2.imread("x.png")
        return super().get_image_with_boxes(image)

    def get_objects_list(self,im):
        print("returning objects list...")
        with open("x.png","wb") as file:
            file.write(im)
        image = cv2.imread("x.png")   
        return super().get_objects_list(image)

  


