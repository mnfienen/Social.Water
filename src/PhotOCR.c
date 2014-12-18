#include <opencv2/highgui/highgui.hpp>
#include <opencv2/text.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/features2d.hpp>
#include <string>
#include <iostream>

using namespace cv;
//TO COMPILE:=============================================
//g++ test.c -o ocrtest `pkg-config --cflags --libs opencv`
//========================================================
int main()
{
	Ptr<text::OCRTesseract> tess = text::OCRTesseract::create();
    Mat img = imread("edit.jpg", 0);
    Mat imgCopy = imread("edit.jpg", 0);
    adaptiveThreshold(img, imgCopy, 200.0, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 55, 15);

    std::string outputString;
    imshow("Image", imgCopy);
    tess->run(imgCopy, outputString);
	std::cout << outputString << "\n";
    waitKey(0);

    return 0;
}
