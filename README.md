# Air-Canvas

Computer Vision Project implemented using OpenCV

Ever wondered that you can draw on by just waiving your finger. In this project we will learn to build an Air Canvas which can draw anything on it by just capturing the motion of a coloured marker with camera. I have used a Pen Cap(of any colour) as the maker.

We will be using OpenCV to build this project. My preffered language is python but understanding the basics it can be implemented in any OpenCV supported language.

Here Colour Detection and tracking is used in order to achieve the objective. The colour marker(Pen Cap) is detected and a mask is produced. It includes the further steps of morphological operations on the mask produced which are Erosion and Dilation. Erosion reduces the impurities present in the mask and dilation further restores the eroded main mask.

# Requirements
PYTHON, NUMPY, OPENCV
