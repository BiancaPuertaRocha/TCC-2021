import cv2
from datetime import datetime 
import numpy as np
import os
import math

def dataHoraAtual():
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime("%d%m%Y-%H%M%S")
    return data_e_hora_em_texto

def criar_imagem_vazia(width, height, rgb_color=(0, 0, 0)):
    image = np.zeros((height, width, 3), np.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image

def cortar_imagem_quadrada(img):
    width, height = img.shape[1], img.shape[0]
    dim = (height,height)
    crop_width = dim[0] if dim[0]<img.shape[1] else img.shape[1]
    crop_height = dim[1] if dim[1]<img.shape[0] else img.shape[0] 
    mid_x, mid_y = int(width/2), int(height/2)
    cw2, ch2 = int(crop_width/2), int(crop_height/2) 
    crop_img = img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
    return crop_img

def retorna_escala_cinza(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def crop_image_circle(img):
	height,width = img.shape
	mask = np.zeros((height,width), np.uint8)
	i = int(width /2)
	j= int(height/2)
	circle_img = cv2.circle(mask,(i, j),j,(255,255,255),thickness=-1)
	masked_data = cv2.bitwise_and(img, img, mask=circle_img)

	return masked_data

def get_max_min2(matrix):
    vetor = []
    for i in matrix:
        for j in i:
            vetor.append(j)
    return max(vetor), min(vetor)

def removeOldestFile(path, max=20):
    list_of_files = os.listdir(path)
    full_path = [(path+"/{0}").format(x) for x in list_of_files]

    if len(list_of_files) == max:
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)

def cart2pol(x, y):
    rho = np.sqrt(pow(x,2) + pow(y,2))
    phi = math.atan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def feval(funcName, *args):
        return eval(funcName)(*args)

def cart2polList(x, y):
    distancia = []
    theta = []
    for i in range(len(x)):
        distancia.append(math.sqrt(math.pow(x[i], 2) + math.pow(y[i], 2)))
        theta.append( math.atan2(y[i], x[i]))
    return distancia, theta

def pol2cartList(distancia, theta):
    x = []
    y = []
    for i in range(len(theta)):
        x.append(distancia[i] * math.cos(theta[i]))
        y.append(distancia[i] * math.sin(theta[i]))
    return x,y

def listToString(list): 

    str1 = "" 

    for ele in list: 
        e = str(ele)
        str1 += e + ";"
    
    str1=str1[:-1]

    return str1 
