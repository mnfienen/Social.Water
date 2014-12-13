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
class PhotoRocker( ):
    def __init__( self, image ):
        call(["convert", "-normalize", "-auto-gamma", "-auto-level",  image, "edit.jpg" ])
        self.img = cv.LoadImage("edit.jpg")
        self.oimg = Image.open(image).filter(ImageFilter.SHARPEN)

        self.aimg = self.oimg.load() #we'll apply changes to this
        #a pixel access object for quick operations

if __name__ == "__main__":
    p= PhotoRocker("./attachments/img4.jpg")
    arr = p.oimg.getextrema()[0]
    gee = p.oimg.getextrema()[1]
    bee = p.oimg.getextrema()[2]
    print arr, gee, bee
    marginr = arr[0] + int( arr[1] * .3 )
    marging = gee[0] + int( gee[1] * .3 )
    marginb = bee[0] + int( bee[1] * .3 )
    print marginr, marging, marginb
    for x in xrange( p.oimg.size[0]):
        for y in xrange(p.oimg.size[1]):
            pix = p.aimg[x,y]

            if pix[0] > marginr and pix[1] > marging and pix[2] > marginb:
                p.aimg[x,y] = (255,255,255)
            else:
                p.aimg[x,y] = (0,0,0)
    #Threshold(p.img,p.aimg, level,255, 1)


    
    p.oimg.show()
    #p.aimg.save("./attachments/demo" + str( level)  + ".jpg" )
    #NamedWindow("OpenCv", flags=CV_WINDOW_AUTOSIZE)
    #ShowImage("OpenCv", p.img)

    print pytesseract.image_to_string(p.oimg,  config='-psm 6 ')
    WaitKey(0)
    DestroyAllWindows()
