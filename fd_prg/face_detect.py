import os
import urllib
import numpy as np
import cv2


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # return the image
        return image
    except:
        print "Error reading from URL"
        return False


def find_faces_img(url, name):
    image = url_to_image(url)
    if type(image) != bool:
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite(name, image)
        except:
            print "Error finding faces"

i = 0
no_images = 100
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
input_folder_name = "vgg_face_dataset/files/"
fileList = os.listdir(input_folder_name)
output_folder_name = "./output/"
for file_name in fileList:
    if i > no_images:
        break
    i += 1
    print "Reading file" + file_name
    with open(input_folder_name + file_name) as f:
        content = f.readlines()
    k = 0
    for line in content:
        k += 1
        if k > 3:
            break
        i += 1
        link = str.split(line)
        if len(link) > 6:
            print "Getting image from URL::" + link[1]
            find_faces_img(link[1], output_folder_name + file_name + link[0] + ".jpg")
