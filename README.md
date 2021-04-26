# Air-Canvas

Computer Vision Project implemented using OpenCV

Ever wondered that you can draw on by just waiving your finger. In this project we will learn to build an Air Canvas which can draw anything on it by just capturing the motion of a coloured marker with camera. I have used a Pen Cap(of any colour) as the maker.

We will be using OpenCV to build this project. My preffered language is python but understanding the basics it can be implemented in any OpenCV supported language.

Here Colour Detection and tracking is used in order to achieve the objective. The colour marker(Pen Cap) is detected and a mask is produced. It includes the further steps of morphological operations on the mask produced which are Erosion and Dilation. Erosion reduces the impurities present in the mask and dilation further restores the eroded main mask.

![image](https://user-images.githubusercontent.com/66010219/116039343-3cc15b80-a688-11eb-99a4-d19f9b68dc30.png)      ![image](https://user-images.githubusercontent.com/66010219/116039374-4945b400-a688-11eb-8263-40506401db28.png)


# Requirements
PYTHON, NUMPY, OPENCV
