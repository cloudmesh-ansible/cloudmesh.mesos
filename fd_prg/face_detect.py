import os
import urllib2
import numpy as np
import cv2
import sys

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    try:
        resp = urllib2.urlopen(url, timeout=5)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # return the image
        return image
    except:
        print "Error reading from URL"
        return False


def write_cascade():
    try:
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        resp = urllib2.urlopen(url, timeout=5)
        face_cascade = resp.read()
        file = open("cascade.xml", 'w')
        file.write(face_cascade)
        file.close()
    except:
        print "Error reading cascade"


def find_faces_img(url, name):
    image = url_to_image(url)
    if not os.path.exists("cascade.xml"):
        print "Writing cascade"
        write_cascade()
    if type(image) != bool:
        try:
            face_cascade = cv2.CascadeClassifier("cascade.xml")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite(name, image)
            return True
        except:
            print "Error finding faces"
            return False
    else:
        return False

def main_func():
    i = 0
    itr = 0
    no_images = 10

    input_folder_name = "vgg_face_dataset/files/"
    fileList = os.listdir(input_folder_name)
    output_folder_name = "./output/"
    # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"

    #resp = urllib2.urlopen(url, timeout=5)
    #face_cascade = resp.read()
    # print face_cascade

    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
    for file_name in fileList:
        if i > no_images:
            break
        if itr > no_images:
            break
        itr += 1

        print "Reading file" + file_name
        with open(input_folder_name + file_name) as f:
            content = f.readlines()
        k = 0
        for line in content:
            k += 1
            if k > 3:
                break

            link = str.split(line)
            if len(link) > 6:
                print "Getting image from URL::" + link[1]
                if find_faces_img(link[1], output_folder_name + file_name + link[0] + ".jpg"):
                    i += 1
    print sys.path[0]

main_func()
