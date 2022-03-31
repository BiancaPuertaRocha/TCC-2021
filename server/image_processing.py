
import numpy as np
from PIL import Image
import cv2
import math
import time
import utils
import uuid
from numpy.polynomial import polynomial as P

class ImagePrecessing:

    def generate_panoramic(self,img):
        ini = time.time()
        altura, largura, _ = img.shape
        largura = altura

        altura_nova= int(altura/2)
        largura_nova = int(altura_nova * (2*math.pi))

        nova_imagem = np.zeros((altura_nova,largura_nova,3), np.uint8)
        nova_imagem[::] = (255,255,255)
        
        raio = largura/2
       
        for x in range(int(largura_nova)):
            for y in range(int(altura_nova)):
                x_real = x - (largura_nova/2)
                y_real = y - (altura_nova)
                
                h = ( raio * y_real)/altura_nova
                
                angulo = ((2*math.pi) * x_real)/largura_nova
                
                cat_oposto = math.sin(angulo)*h
                cat_adjacente = math.cos(angulo)*h

                x_om = int(cat_adjacente  +(largura/2) )
                y_om = int( cat_oposto  +(altura/2) )
                

                if(x_om<largura and int(x)<largura_nova and int(y)<altura_nova ):
                    azul = img.item( x_om, y_om, 0)
                    verde = img.item(x_om, y_om, 1)
                    vermelho = img.item(x_om, y_om, 2)
                    
                    nova_imagem[int(y), int(x)]=(azul, verde, vermelho)
                    
        fim = time.time()
        print("tempo servidor processamento: ",fim-ini )
        cv2.imwrite("processed_images/panoramic.png", nova_imagem)
        return cv2.imencode('.png',nova_imagem)[1].tobytes()

    def get_image_with_boxes(self,image):

        original = image.copy()

        ret, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 75, 255, cv2.THRESH_BINARY_INV)
        ROI_number = 0
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        altura, largura, canais = image.shape
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            if w>20 and h>20:
                cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
            ROI = original[y:y+h, x:x+w]
            ROI_number += 1

        return cv2.imencode('.png',image)[1].tobytes()

    def get_objects_list(self,image):

        original = image.copy()

        ret, thresh = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 75, 255, cv2.THRESH_BINARY_INV)
        ROI_number = 0
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        altura, largura, canais = image.shape
        pontos = ""
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            #escrever no arquivo
            if w>20 and h>20:
                pontos += f"{x};{y};{w};{h}\n"
            ROI = original[y:y+h, x:x+w]
            ROI_number += 1
            
        return pontos.encode()

    def use_mask(self,image):
        mascara = cv2.imread('mask/mascara_calculada.png')
        grey_image = image
        mascara_diminuida =  mascara
        altura_mask, largura_mask,_ = mascara.shape
        grey_image = utils.retorna_escala_cinza(grey_image)
        altura, largura = grey_image.shape

        for i in range(11, altura, 1):
            for j in range(1, largura, 1):
                if i < altura_mask and j <largura_mask:
                    #if check_raio(mascara_diminuida, i, j, 10) :
                    if np.array_equal(mascara_diminuida[i, j], [255,255,255]):
                        linhaini = i-10
                        tomCinza = np.mean(grey_image[linhaini:linhaini+6,j])
                        grey_image[i, j] = tomCinza


        for i in range(altura-11,  1, -1):
            for j in range(1, largura, 1):
                if i < altura_mask and j <largura_mask:
                    #if check_raio(mascara_diminuida, i, j, 10) :
                    if np.array_equal(mascara_diminuida[i, j], [255,255,255]):
                        linhaini = i+3
                        tomCinza = np.mean(grey_image[linhaini:linhaini+6,j])
                        grey_image[i, j] = tomCinza


        grey_image = utils.crop_image_circle(grey_image)
        cv2.imwrite("processed_images/masked.png", grey_image)
        return cv2.imencode('.png',grey_image)[1].tobytes()

    def generate_birds_eye(self,image, distParams, angParams, centerCol,  centerLine):

        image = utils.retorna_escala_cinza(image)

        height, width = image.shape # y, x
        print(height, width)
        if centerLine > height-centerLine:
            ladosub = float(height-centerLine)
        else:
            ladosub = float(centerLine)

        print(ladosub)
        pix_len = 30/ladosub

        ret_image = utils.criar_imagem_vazia(int(ladosub)*2, int(ladosub)*2)

        for i in range(int(ladosub)*2):
            for j in range(int(ladosub)*2):
                #print(i,j)
                t_x = (j - float(ladosub))*pix_len
                t_y = -(i - float(ladosub))*pix_len
                dist, ang = utils.cart2pol(t_x, t_y)
                dist_reti = P.polyval(dist, distParams)
                ang_reti = P.polyval(ang, angParams)
                x,y = utils.pol2cart(dist_reti, ang_reti)
                m_col_orig = x + centerCol
                m_lin_orig = centerLine - y
                if (m_col_orig>0) and (m_col_orig<width -1) and (m_lin_orig>0) and m_lin_orig<height-1:
                    linhaant = math.floor(m_lin_orig)
                    linhapos = math.ceil(m_lin_orig)
                    colant = math.floor(m_col_orig)
                    colpos = math.ceil(m_col_orig)
                    fracL = m_lin_orig - linhaant
                    fracC = m_col_orig - colant
                    corlinant = image[linhaant, colant]*(1-fracC)+image[linhaant, colpos]*fracC
                    corlinpos = image[linhapos, colant]*(1-fracC)+image[linhapos, colpos]*fracC
                
                    cor = corlinant*(1-fracL)+corlinpos*fracL
                else:
                    cor = 0
                
                ret_image[i, j] = cor

        cv2.imwrite("processed_images/birds_eye.png", ret_image)

        return cv2.imencode('.png',ret_image)[1].tobytes()

