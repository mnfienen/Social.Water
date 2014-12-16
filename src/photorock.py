"""==================================================================
PhotoRock!

This object will take a photo and attempt to extract some text
from it using Tesseract OCR, ImageMagick, and PIL.

@Author Matthew G. McGovern
@email matthewgmcgovern@gmail.com
=====================================================================
"""
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv
from subprocess import call
import pytesseract
import Image
import ImageFilter
import tools
import re
class PhotoRocker( ):
    def __init__( self, image ):
        call(["convert", "-normalize", "-auto-gamma", "-auto-level",  image, "edit.jpg" ])
        self.img = cv.LoadImage("edit.jpg", cv.CV_LOAD_IMAGE_GRAYSCALE)
        #cv.AdaptiveThreshold(self.img, self.img, 75, adaptive_method=cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv.CV_THRESH_BINARY, blockSize=33, param1=12)
        #cv.SaveImage("edit2.jpg", self.img)
        #self.img2 = Image.open("edit2.jpg")
        self.oimg = Image.open("edit.jpg").filter(ImageFilter.SHARPEN)
        self.aimg = self.oimg.load() #we'll apply changes to this
        #a pixel access object for quick operations

if __name__ == "__main__":
    floatpattern = re.compile(r'(?<![0-9])([0-9]\.[0-9][0-9])(?![0-9])')
    p= PhotoRocker("./attachments/img10.jpg")
    p.oimg = Image.open("edit.jpg").filter(ImageFilter.SHARPEN)

    arr = p.oimg.getextrema()[0]
    gee = p.oimg.getextrema()[1]
    bee = p.oimg.getextrema()[2]
    print arr, gee, bee
    test_pulled = None
    nums = dict()
    for i in xrange(0,30):
        p.oimg = Image.open("edit.jpg").filter(ImageFilter.SHARPEN)
        p.aimg = p.oimg.load() #we'll apply changes to this
        marginr = arr[0] + int( arr[1] * ( .05  + (i*.01)))
        marging = gee[0] + int( gee[1] * (.05 + (i*.01))  )
        marginb = bee[0] + int( bee[1] * (.05  + ( i*.01)))
        print marginr, marging, marginb
        for x in xrange( p.oimg.size[0]):
            for y in xrange(p.oimg.size[1]):
                pix = p.aimg[x,y]

                if pix[0] > marginr and pix[1] > marging and pix[2] > marginb:
                    p.aimg[x,y] = (255,255,255)
            #else:
            #    p.aimg[x,y] = (0,0,0)


    #p.oimg.show()
    #p.aimg.save("./attachments/demo" + str( level)  + ".jpg" )
    #cv.NamedWindow("OpenCv", flags=cv.CV_WINDOW_AUTOSIZE)
    #cv.ShowImage("OpenCv", p.img)

        text_pulled = pytesseract.image_to_string( p.oimg,  config='-psm 6 ')
        #print text_pulled
    	results = floatpattern.findall(text_pulled)
        if results:
            for result in results:
                if result not in nums:
                    nums[result] = 1
                else:
                    nums[result] += 1     
                print result,
        print " "
        text_pulled = pytesseract.image_to_string( p.oimg )
        results = floatpattern.findall(text_pulled)
        if results:
            for result in results :
                print result,
                if result not in nums:
                    nums[result] = 1
                else:
                    nums[result] += 1     
        print " "
    if nums:
        print min( nums.keys() ) 
    #cv.WaitKey(0)
    #cv.DestroyAllWindows()
