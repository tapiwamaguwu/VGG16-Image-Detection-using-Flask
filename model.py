import os
from re import fullmatch
import cv2
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input,decode_predictions
import PIL
from PIL import Image
import glob



model=VGG16()


def load_video(video_filename):
    print("splitting into frames...\n")
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    count = 0

    while success:
      #resize every image to 224x224  
      image=cv2.resize(image,(224,224),interpolation = cv2.INTER_AREA)
      # save frame as JPEG file
      cv2.imwrite("static/frame%d.jpg" % count, image)           
      
      #getting every nth frame 
      sampling_rate=10
      i=0
      while i<sampling_rate:
        success,image = vidcap.read()
        i += 1

      count += 1
    
    print("Frames read: ",count-1)

def predict(video_filename):
    delete_files()
    load_video(video_filename)
    labels=[]
    print("Predicting frames...")
    for file in os.listdir('static'):
        #print(file+"\n")
        #constructing full path of each image
        full_path='static/'+file

        #loading the images
        image = load_img(full_path,target_size=(224,224))
        image = img_to_array(image)
        image=image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
        image=preprocess_input(image)
        y_pred=model.predict(image)
        label=decode_predictions(y_pred,top=1)
        img_prediction={"frame":file.replace(".jpg",""),"prediction":label[0][0][1],"certainity":label[0][0][2]}
        print(img_prediction)
        labels.append(img_prediction)
    print("Done: Predicting frames...")    
    return labels

#deleting frames from a previous analysis
def delete_files():
  for file in os.listdir('static'):
    full_path='static/'+file
    if os.path.exists(full_path):
      os.remove(full_path)
    else:
      print("The file does not exist")    