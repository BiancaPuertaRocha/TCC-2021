
import numpy as np
from PIL import Image
import cv2
import math
import time
import utils
import uuid
from numpy.polynomial import polynomial as P
from image_processing import ImagePrecessing


 
class ProcessingById(ImagePrecessing):

    def save_image_get_id(self,image):
        print("gerando id da imagem...")
        id = str(uuid.uuid4())
        with open("images/"+id+".png","wb") as file:
            file.write(image)

        imagem = cv2.imread("images/"+id+".png")
       
        cv2.imwrite("images/"+id+".png", imagem)

        print("removendo arquivos antigos...")
        utils.removeOldestFile("images", max=30)
        return id

    def generate_panoramic(self,id):
        print("generating panoramic image...")
        img = utils.cortar_imagem_quadrada(cv2.imread("images/"+id+".png"))
        return super().generate_panoramic(img)
    
    def get_image_with_boxes(self,id):
        print("detecting objects and returning boxes...")
        image = cv2.imread("images/"+id+".png")
        return super().get_image_with_boxes(image)

    def get_objects_list(self,id):
        print("detecting objects end returning list...")
        image = cv2.imread("images/"+id+".png")
        return super().get_objects_list(image)

    def use_mask(self,id):
        print("using mask...")
        image = cv2.imread("images/"+id+".png")
        return super().use_mask(image)

    def generate_birds_eye(self,id, distParams, angParams, centerCol,  centerLine):
        print("gerando imagem de vista aerea...")
        image = cv2.imread("images/"+id+".png")
        return super().generate_birds_eye(image, distParams, angParams, centerCol,  centerLine)
