import sys
import cv2

import os
import cv
import numpy as np
import matplotlib.pyplot as plt


def show_img(image):
		plt.imshow( image )
		plt.show()

class PhotoHack():
	"""Given a picture of the entire gauge, this will look for the top sign
	and then guess it's distance from the water.
	"""
	def __init__(self, image_file):
		self.img = cv2.imread( image_file )
		
		self.edgeimg = cv2.bilateralFilter(self.img, 25, 25, 25)
		self.edgeimg = cv2.Canny(self.edgeimg, 200, 25)

		#self.edgeimg = cv2.Canny(self.edgeimg, 25, 200)
		#show_img(self.edgeimg)
		self.contours = None

	def find_contours(self):
		(cnts, blah) = cv2.findContours(self.edgeimg.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted( cnts, key = cv2.contourArea )
		return contours


if __name__ == "__main__":
	p = PhotoHack(sys.argv[1])
	conts = p.find_contours()
	squares = list()
	for c in conts[10:]:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True, )
		
		if len(approx) == 4 :
			squares.append(approx)

	maxarea = 0	
	the_biggest_square = None
	for square in squares:
		squarea = cv2.contourArea(square)
		if squarea > maxarea:
			maxarea = squarea
			the_biggest_square = square

	cv2.drawContours(p.img, [the_biggest_square], -1, (0, 255, 0), 3)


	show_img(p.img)

