import numpy as np
import cv2
import os
import math
import time
import utils
from numpy.polynomial import polynomial as P

class Support:
    # OTHERS

    def generate_mask(self):
        print('geraando mascara...')
        pasta = 'omni_images'
        croppeds = []
        for diretorio, subpastas, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                image = cv2.imread(os.path.join(diretorio, arquivo))
                h, w, _ = image.shape
                resized = cv2.resize(image, (int(w/2), int(h/2)), interpolation = cv2.INTER_AREA)
                croppeds.append(utils.retorna_escala_cinza(resized))
                
    
        matrix = np.array(croppeds)
        imagemDesvPad = np.std(matrix, axis=0)
        ma, mi = utils.get_max_min2(imagemDesvPad)
        imDesvPadNorm = np.array((imagemDesvPad-mi)/(ma-mi)*255, dtype=np.uint8)
        _, thresh = cv2.threshold(imDesvPadNorm,30, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((5,5), np.uint8) 
        img_dilation = cv2.dilate(thresh, kernel, iterations=7) 
        img_dilation = cv2.resize(img_dilation, (w, h), interpolation = cv2.INTER_AREA)
        cv2.imwrite('mask/mascara_calculada.png', img_dilation)

        return True


    def __load_image_points(self):
        dataset = open('calibration/ControleImagem.pto', 'r')
        x = []
        y = []
        c = []
        for line in dataset:
            line = line.strip()
            [ X, Y, C] = line.split('\t')
            x.append(float(X))
            y.append(float(Y))
            c.append(float(C))
        return x, y

    def carregarPontosTerreno(self):
        dataset = open('calibration/ControleTerreno.pto', 'r')
        x = []
        y = []

        for line in dataset:
            line = line.strip()
            [X, Y] = line.split('\t')
            x.append(float(X))
            y.append(float(Y))

        return x, y

    def calibrate(self,centroCol = 2094, centroLin = 1463):
    
        C, L = self.__load_image_points()
        Lcentral = []
        Ccentral = []

        for i in range(len(L)):
            Lcentral.append((L[i] - centroLin)*(-1))

        for i in range(len(C)):
            Ccentral.append(C[i] - centroCol)

        X, Y = self.carregarPontosTerreno()



        distanciaImagem, thetaImagem = utils.cart2polList(Ccentral, Lcentral)

        distanciaTerreno, thetaTerreno = utils.cart2polList(X,Y)

        distanciaparam, statusdist = P.polyfit(distanciaTerreno, distanciaImagem, 12, full=True)
        angparam, statusang = P.polyfit(thetaTerreno, thetaImagem, 18, full=True)
        print(angparam)
        return (utils.listToString(distanciaparam)+'\n'+utils.listToString(angparam)).encode()

            

