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
		self.exterior_isolated = None
		self.avg_inside = None
		self.slope_inside = None
		self.boxblank = None   ##mask we'll use to extract just the image inside the box.


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
			print "Error: Run find_contours first."
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
		###############################################
		## Isolate everything inside the largest box in the picture
		blank = np.zeros(self.img.shape, np.uint8)
		cv2.drawContours( blank, [contour], 0, (255,255,255) , -1 )
		#show_img(blank)
		self.img[:,:,1] = 0
		self.maskedimg = cv2.bitwise_and(self.img, blank )

		self.boxblank = cv2.cvtColor(self.maskedimg, cv.CV_RGB2GRAY) #we'll want to keep the mask at this point

		##show image, and get the mean value inside the box.
		#show_img(self.maskedimg)
		rect = cv2.boundingRect(contour)
		mean_inside = cv2.mean( self.maskedimg , self.boxblank )

		return self.maskedimg , mean_inside

		"""

		 ## get the mean values inside the box
		print "Interior: ", mean1
		
		##############################################
		## Now let's isolate everything BUT the box.
		invmaskedimg = np.zeros(self.img.shape, np.uint8) #blank canvas
		cv2.drawContours(invmaskedimg, [contour], 0, (255,255,255) , -1 ) #draw our shape.
		invmaskedimg = cv2.bitwise_not(invmaskedimg) #invert everything
		self.exterior_isolated = cv2.bitwise_and(self.img, invmaskedimg) 
		#  run an AND, removing only the interior of the box.

		
		invmaskedimg = cv2.cvtColor(invmaskedimg, cv.CV_RGB2GRAY) #convert the mask to 1 channel
		mean2 = cv2.mean( self.exterior_isolated , invmaskedimg )
		
		print "Exterior: " , mean2
		print mean1[0] - mean2[0] , mean1[1] - mean2[1] , mean1[2] - mean2[2]
	
		"""
		
	def get_min_max_loc(self):
		img = cv2.cvtColor( self.maskedimg, cv.CV_RGB2GRAY ) #temprarily convert to bw
		maximum, minimum, maxloc, minloc  = cv2.minMaxLoc(img , self.boxblank)
		print maximum, minimum
		show_img( self.boxblank )
		return maximum, minimum, maxloc, minloc



if __name__ == "__main__":
	p = PhotoHack(sys.argv[1])
	contours = p.find_contours()
	#for i in range(0,10):
		#print contours[-i]
		#cv2.drawContours(p.img, [contours[-i]], -1, (0, 0, 255), 1 )
	#show_img(p.img.copy()) 
	p.find_squares()
	large_square = p.find_largest_square()
	
	if large_square is not None:
		cv2.drawContours(p.img, [large_square], -1, (0, 255, 0), 3)
		#show_img(p.img)
		pass
	else: 
		print "No squares found :("

	p.maskedimg, p.avg_inside = p.snip_square(large_square)
	p.slope_inside = p.get_slope()


	
###So I have a method to maybe get the rectangle I want, the global max and global min of the internal area
## and the locations in pixels of the max and min location.
## From here I want to shift data around so that I can easily get a top to bottom measurement 
## of the slope with respect to the brightness at each interval along the meter.
## 
