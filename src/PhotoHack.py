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
	"""Given a picture of the entire gauge, this will look for a square in the image.
	"""
	def __init__(self, image_file):
		self.img = cv2.imread( image_file ) #read in the image file.
		self.edgeimg = cv2.bilateralFilter(self.img, 25, 25, 25) # Blur things slightly to reduce noise.
		self.edgeimg = cv2.Canny(self.edgeimg, 200, 25) #Run Canny edge detection.
		self.squares = list()
		#self.edgeimg = cv2.Canny(self.edgeimg, 25, 200) 
		#show_img(self.edgeimg) ## optional print
		self.contours = None
		self.maskedimg = None

	def find_contours(self):
		#takes in an image processed with edge detection and runs the function for finding contours.
		#returns a list of contours.
		(cnts, blah) = cv2.findContours(self.edgeimg.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted( cnts, key = cv2.contourArea )
		self.contours = contours
		return contours

	def find_squares(self):
		if self.contours:
			for c in self.contours:
				peri = cv2.arcLength(c, True)
				approx = cv2.approxPolyDP(c, 0.01 * peri, True, )
				if len(approx) == 4 :
					self.squares.append(approx)
		else:
			print "Error: Run find_countours first."
			return None
	def find_largest_square(self):
		maxarea = 0	
		the_biggest_square = None
		for square in self.squares:
			squarea = cv2.contourArea(square)
			if squarea > maxarea:
				maxarea = squarea
				the_biggest_square = square
		return the_biggest_square
	def snip_square(self, contour):
		"""Feed a contour, this will remove it and return just what is inside the contour.
		"""

		blank = np.zeros(self.img.shape, np.uint8)
		cv2.drawContours(blank, [contour], 0, (255,255,255) , -1 )

		#show_img(blank)
		self.maskedimg = cv2.bitwise_and(self.img, blank )
		blank = cv2.cvtColor(blank, cv.CV_RGB2GRAY)
		show_img(self.maskedimg)
		rect = cv2.boundingRect(contour)

		mean = cv2.mean(self.maskedimg , blank)
		print mean

if __name__ == "__main__":
	p = PhotoHack(sys.argv[1])
	p.find_contours()
	p.find_squares()
	large_square = p.find_largest_square()
	
	if large_square is not None:
		#cv2.drawContours(p.img, [large_square], -1, (0, 255, 0), 3)
		#show_img(p.img)
		pass
	else: 
		print "No squares found :("

	p.snip_square(large_square)



	

