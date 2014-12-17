import cv2
import cv
import os
import numpy as np
import Image
import matplotlib.pyplot as plt
"""
Another garbagey, figure it out attempt with opencv. This one also probably won't get used.


@Author Matthew G. McGovern
@email matthewgmcgovern@gmail.com
"""


CUR_DIR = os.getcwd()
TEMPLATE_DIR = CUR_DIR + "/templates/"


class TemplateSearcher():
	def __init__(self, image_file, template_images):
		"""Give this an image and an array of templates and this will search the image for each template.
		"""
		self.img = cv2.imread(image_file)
		self.edgeimg = cv2.Canny(self.img, 100, 230)
		#plt.imshow(self.img)
		#plt.show()
		self.templates = list()
		for image in template_images:
			pic = TEMPLATE_DIR + image
			temp = cv2.imread( pic , cv2.CV_LOAD_IMAGE_COLOR )
			edges = cv2.Canny( temp , 120, 230 )
			#plt.imshow( edges )
			#plt.show()
			self.templates.append( edges )
	def check_templates(self):
		all_scores = list()
		for template in self.templates:
			subscore = cv2.matchTemplate(self.edgeimg, template, method=cv2.TM_CCOEFF )
			all_scores.append( subscore )
		return all_scores

if __name__ == "__main__":
	
	files_in_dir = os.listdir( TEMPLATE_DIR )
	image = CUR_DIR + "/attachments/img1.jpg"
	TempSearch = TemplateSearcher( image, files_in_dir )
	results = TempSearch.check_templates()
	scene_img_highlighted = TempSearch.img.copy()
	for result in results:
		i = 0
		min_score, max_score, (min_x, min_y), (max_x, max_y) = cv2.minMaxLoc(result)
		corner_topL = (max_x, max_y)
		corner_botR = (corner_topL[0]+TempSearch.templates[i].shape[1], corner_topL[1]+TempSearch.templates[i].shape[0])
		
		cv2.rectangle(scene_img_highlighted,  # image to add a rectangle to
              corner_topL,            # upper left corner of rectangle
              corner_botR,            # lower right corner of rectangle
              (0,255,0),              # rgb tuple for rectangle color
              10      )                # rectangle stroke thickness (in pixels)
		i += 1
	plt.imshow( scene_img_highlighted )
	plt.show( ) 


	