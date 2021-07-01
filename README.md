# VGG16-Image-Detection-using-Flask

## Overview
A web application using Flask and the VGG16 deep learning model. It takes a video (max: 10Mb) and the user supplies the name of any object and the application using the VGG16
model and OpenCV to split the video into frames, analyses each frame and then returns all the frames that contain the object.

## Group Members
# Tapiwa Maguwu R178454A
# Thandolwenkosi Mhlanga R178451D

## Demonstration Video
https://drive.google.com/file/d/1HgUOFvZ0f53oQHJJoCqhaXmoznI3xGu_/view?usp=sharing

## VGG16 Training and Example (Colab File)
https://colab.research.google.com/drive/1YdMFlCCs3P2WJQ1C1dVVF-4i9Fc5TX8n#scrollTo=udhekJxOZxym

### How to Install
To install and run the application follow these steps:

#### 1. create virtual virtual environment
python -m venv flask_demo  

#### 2. activate virtual environment
flask_demo\Scripts\activate 

#### 3. install packages from requirements.txt
python -m pip install -r requirements.txt

#### 4. running application
flask run
