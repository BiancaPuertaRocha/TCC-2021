import numpy as np
from PIL import Image
import cv2
import math
import utils
from numpy.polynomial import polynomial as P



#iniciando retificacao

id = "05d56b81-e8b0-4188-bcc2-80661b3e435e"
angParams = [3.79310166e+00, 1.58067432e+00, 1.18106053e+00, 6.58175186e-01,
       4.48094812e-01, 2.48544543e-01, 1.33856909e-01, 6.40032935e-02,
       3.09645448e-02, 1.30538454e-02, 6.10936393e-03, 2.19757495e-03,
       9.93563397e-04, 2.94086228e-04, 1.28579653e-04, 3.05232331e-05,
       1.29130129e-05, 2.16189631e-06, 8.73716953e-07]
distParams = [3.28687036e+00, 1.38177885e+00, 5.09456016e-01, 1.60378709e-01,
       4.24593841e-02, 9.87414053e-03, 1.81703939e-03, 2.73403409e-04,
       3.61479456e-05, 4.30988686e-06, 3.51117473e-07, 2.45403353e-08,
       1.13588807e-09]
centerLine = 1463
centerCol = 2094
pix_len = 0.1

print("gerando imagem de vista aerea...")
color_image = cv2.imread("images/"+id+".png")

image = utils.retorna_escala_cinza(color_image)

height, width = image.shape # y, x

if centerLine > height-centerLine:
    ladosub = float(height-centerLine)
else:
    ladosub = float(centerLine)
ladosub = 800


ret_image = utils.criar_imagem_vazia(int(ladosub)*2, int(ladosub)*2)
new = utils.criar_imagem_vazia(int(ladosub)*2, int(ladosub)*2)

print('gerando')
i=0
j=0
t_x = (i - float(ladosub))*pix_len
t_y = -(j - float(ladosub))*pix_len

dist, ang = utils.cart2pol(t_x, t_y)
dist_reti = P.polyval(dist, distParams)
ang_reti = P.polyval( ang, angParams)
print(ang_reti)
x,y = utils.pol2cart(dist_reti, ang_reti)
print(x,y)


m_col_orig = x + centerCol
m_lin_orig = -y + centerLine

print(m_col_orig, m_lin_orig)
if (m_col_orig>=0) and (m_col_orig<width) and (m_lin_orig>=0) and m_lin_orig<=height:
    print('af')
    linhaant = math.floor(m_lin_orig)
    linhapos = math.ceil(m_lin_orig)
    colant = math.floor(m_col_orig)
    colpos = math.ceil(m_col_orig)
    fracL = m_lin_orig - linhaant
    fracC = m_col_orig - colant
    corlinant = image[linhaant, colant]*(1-fracC)+image[linhaant, colpos]*fracC
    corlinpos = image[linhapos, colant]*(1-fracC)+image[linhapos, colpos]*fracC
    new[i, j] = image[m_col_orig,m_lin_orig]
    
    cor = corlinant*(1-fracL)+corlinpos*fracL
else:
    print("oi")
    cor = 0

ret_image[i, j] = cor
cv2.imwrite("im2.png", ret_image)
cv2.imwrite("new.png", new)

cv2.waitKey()