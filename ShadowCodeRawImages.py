import cv2
import numpy as np
from random import * 
import pprint
from PIL import Image
path = "./"

#READ THE IMAGE
img = cv2.imread(path + "2020_08_04_06_03.jpg", cv2.IMREAD_COLOR)
cv2.imshow('original image', img)

#CONVERT THE IMAGE IN THE HSV SPACE
img_copy = img.copy()
hsv_image = cv2.cvtColor(img_copy,cv2.COLOR_BGR2HSV)
cv2.imshow('hsv image', hsv_image)
cv2.imwrite("./hsv_image.jpg", hsv_image)


#OBTAIN FIRTS MASK 
#FILTERING USING THE VALUE OF V THAT MEANS
#TO FILTER THE PIXEL THAT ARE MORE OR LESS BRIGTHER,
#LOW VALUE MEANS LESS BRIGHT AND VICEVERSA
lower_shadow = np.array([0, 0, 0])
upper_shadow = np.array([180, 255, 140])
mask = cv2.inRange(hsv_image, lower_shadow, upper_shadow)
cv2.imshow('Zone d\'ombra', mask)
cv2.imwrite("./first_binary_mask.jpg", mask)


#OBTAIN SECOND MASK
#HERE WE FILTER IN THE STARTING IMAGE(RGB) TO SELECT
#ONLY THE PIXELS THAT HAVE VALUE LIKE GREY AND WHITE,
#IN THIS WAY WE PROBABLY OBTAIN A MASK THAT IS 
#COMPLEMENTARY WITH THE PREVIOUS ALREADY GENERATED
# upload the image
img = Image.open("./2020_08_04_06_03.jpg")
# convert the image in grey scale
gray_img = img.convert('L')
# apply the threshold to pixels value
threshold = 200
binary_img = gray_img.point(lambda x: 255 if x > threshold else 0, '1')
# save the obtained mask
binary_img.save("second_binary_mask.jpg")

#AFTER OBTAINING THE MASK NOW WE DO THE AND BETWEEN
#THEM IN ORDER TO OBTAIN WHITE PIXELS ONLY FOR 
#THE PIXELS THAT ARE WHITE IN BOTH IMAGES, THAT
#WILL BE SUNNY PIXELS
#upload the two masks
img1 = Image.open("first_binary_mask.jpg").convert("1")
img2 = Image.open("second_binary_mask.jpg").convert("1")
#check that the dimensions are the same
if img1.size != img2.size:
    raise ValueError("Le due immagini devono avere le stesse dimensioni")
#create a new empty image
new_img = Image.new("1", img1.size)
#iterate over each pixels of the image
for x in range(img1.size[0]):
    for y in range(img1.size[1]):
        #if both images have white pixel set it as white also in the new image
        if img1.getpixel((x, y)) == 0 and img2.getpixel((x, y)) == 0:
            new_img.putpixel((x, y), 1)
#save resulting image
new_img.save("result_binary_image.jpg")


#ROTAZIONE E CROP LE AVEVAMO FATTE PER QUANDO NON SAPEVO CHE CI STAVA GIA L'ALTRA VE
# #EFFETTUIAMO ROTAZIONE E CROP
img = cv2.imread('result_binary_image.jpg')
copy_img = img.copy()
blk_wht = cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('binary_image', blk_wht)
contours, hierarchy = cv2.findContours(blk_wht, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# Trova il contorno più grande
contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours] 
biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
# Trova l'angolo di rotazione
rect = cv2.minAreaRect(biggest_contour) #this function returns: the center, the width and the height,and the angle of rotation or this rectangle
angle = rect[2] #angle of rotation
# Ruota l'immagine
(h, w) = blk_wht.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle-90, 1.0) #the third parameter is the scale
rotated_img = cv2.warpAffine(blk_wht, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
# Trova il rettangolo di delimitazione
x, y, w, h = cv2.boundingRect(biggest_contour)
# Applica il rettangolo di delimitazione all'immagine ruotata
cropped_img = rotated_img[y:y+h, x:x+w]


# #CROP ULTERIORE PER TOGLIERE PARTI SUPERFLUE
cropped_image = Image.fromarray(cropped_img)
cropped_image.save("rotate_and_crop.jpg")
def_cropped_array = np.asarray(cropped_img)
def_cropped_array = def_cropped_array[112:541,84:786]
def_cropped_img = Image.fromarray(def_cropped_array)
def_cropped_img.save("def_rotate_cropped_img.jpg")


#APPLICARE OPENING: EROSIONE+DILATAZIONE IN MODO DA ELIMINARE 
#I PIXELS BIANCHI CHE SONO IN PIU
def_cropped_img = cv2.imread('def_rotate_cropped_img.jpg')
morfological_kernel = np.ones((5,5), np.uint8)
opened_image = cv2.morphologyEx(def_cropped_img, cv2.MORPH_OPEN,morfological_kernel)
cv2.imshow('OPENED image', opened_image)
opened_img = Image.fromarray(opened_image)
opened_img.save("opened.jpg")

cv2.waitKey()
