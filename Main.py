import numpy as np
from PIL import Image, ImageStat

CMYKSave = ["C","M","Y","K"]
RGBSave = ["R","G","B"]
AllSave = ["C","M","Y","K","R","G","B"]

imgRGB = Image.open("Fox.jpg").convert("RGB")
img_W, img_H = imgRGB.size
numElements = range(img_H * img_W)
split_RGB = Image.Image.split(imgRGB)

redChannel = np.resize(split_RGB[0],(img_H * img_W)).tolist()
greenChannel = np.resize(split_RGB[1],(img_H * img_W)).tolist()
blueChannel = np.resize(split_RGB[2],(img_H * img_W)).tolist()

def getScreen(color):
	List = []
	#Converts R,G, or B channels into colored images 
	if color == "R":
		for i in redChannel:
			List.append([i,0,0])
	elif color == "G":
		for i in greenChannel:
			List.append([0,i,0])
	elif color == "B":
		for i in blueChannel:
			List.append([0,0,i])
	else:
		keyList = []
		cyanList = []
		magentaList = []
		yellowList = []


		for i in numElements:
			#generates the Black values based on the RGB values of each pixel
			#converts RGB values from 0-255 to 0-1
			percentR = redChannel[i] / 255
			percentG = greenChannel[i] / 255
			percentB = blueChannel[i] / 255
			#Finds the highest of the three and appends it to key list
			key = 1 - max(percentR,percentG,percentB)
			keyList.append(key)

		#Convert RGB values to CMK values using key
		for i in numElements:
			percentR = redChannel[i] / 255
			cyan = 0
			if 1 - percentR - keyList[i] != 0:
				cyan = (1 - percentR - keyList[i]) / (1 - keyList[i])
			cyanList.append(cyan)

		for i in numElements:
			percentG = greenChannel[i] / 255
			magenta = 0
			if 1 - percentG - keyList[i] != 0:
				magenta = (1 - percentG - keyList[i]) / (1 - keyList[i])
			magentaList.append(magenta)

		for i in numElements:
			percentB = blueChannel[i] / 255
			yellow = 0
			if 1 - percentB - keyList[i] != 0:
				yellow = (1 - percentB - keyList[i]) / (1 - keyList[i])
			yellowList.append(yellow)

		#converts CMYK back to RGB and appends to List
		if color == "K":
			for i in numElements:
				k = 255 * (1- keyList[i])
				List.append([k,k,k])
		if color == "C":
			for i in numElements:
				c = 255 * (1 - cyanList[i])
				o = 255
				List.append([c,o,o])
		if color == "M":
			for i in numElements:
				c = 255 * (1 - magentaList[i])
				o = 255
				List.append([o,c,o])
		if color == "Y":
			for i in numElements:
				c = 255 * (1 - yellowList[i])
				o = 255
				List.append([o,o,c])

	Array = np.array(List,dtype=np.uint8)
	return Array

def saveImg(color):
	Img = Image.fromarray(np.resize(getScreen(color),(img_H,img_W,3)))
	Img.save("Images/" + color + ".png")

for i in CMYKSave:
	saveImg(i)
