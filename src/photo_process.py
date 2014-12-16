import cv2
import cv
import os
import numpy as np
import Image
import matplotlib.pyplot as plt

CUR_DIR = os.getcwd()
TEMPLATE_DIR = CUR_DIR + "/templates/"


class TemplateSearcher():
	def __init__(self, image_file, template_images):
		"""Give this an image and an array of templates and this will search the image for each template.
		"""
		self.img = cv2.imread(image_file)
		self.templates = list()
		for image in template_images:
			pic = TEMPLATE_DIR + image
			self.templates.append( cv2.imread( pic , cv2.CV_LOAD_IMAGE_COLOR ) )
	def check_templates(self):
		all_scores = list()
		for template in self.templates:
			subscore = cv2.matchTemplate(self.img, template, method=cv2.TM_CCORR_NORMED )
			all_scores.append( subscore )
		return all_scores

if __name__ == "__main__":
	
	files_in_dir = os.listdir( TEMPLATE_DIR )
	image = CUR_DIR + "/attachments/img10.jpg"
	TempSearch = TemplateSearcher( image, files_in_dir )
	results = TempSearch.check_templates()
	for result in results:
		i = 0
		min_score, max_score, (min_x, min_y), (max_x, max_y) = cv2.minMaxLoc(result)
		corner_topL = (max_x, max_y)
		corner_botR = (corner_topL[0]+TempSearch.templates[i].shape[1], corner_topL[1]+TempSearch.templates[i].shape[0])
		scene_img_highlighted = TempSearch.img.copy()
		cv2.rectangle(scene_img_highlighted,  # image to add a rectangle to
              corner_topL,            # upper left corner of rectangle
              corner_botR,            # lower right corner of rectangle
              (0,255,0),              # rgb tuple for rectangle color
              10      )                # rectangle stroke thickness (in pixels)
		plt.imshow( scene_img_highlighted )
		plt.show( ) 
		i += 1


	