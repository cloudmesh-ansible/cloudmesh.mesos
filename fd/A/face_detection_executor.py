#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import threading
import time
import os
import urllib2
import numpy as np
import cv2
import shutil
import zipfile

import mesos.interface
from mesos.interface import mesos_pb2
import mesos.native


class MyExecutor(mesos.interface.Executor):
    def launchTask(self, driver, task):
        # Create a thread to run the task. Tasks should always be run in new
        # threads or processes, rather than inside launchTask itself.
        def run_task():
            print "Running task %s" % task.task_id.value
            update = mesos_pb2.TaskStatus()
            update.task_id.value = task.task_id.value
            update.state = mesos_pb2.TASK_RUNNING
            update.data = 'data with a \0 byte'
            driver.sendStatusUpdate(update)

            # This is where one would perform the requested task.
            try:
                self.main_func(1)
            except:
                print "Error running face detection"

            print "Sending status update..."
            update = mesos_pb2.TaskStatus()
            update.task_id.value = task.task_id.value
            update.state = mesos_pb2.TASK_FINISHED
            update.data = 'data with a \0 byte'
            driver.sendStatusUpdate(update)
            print "Sent status update"

        thread = threading.Thread(target=run_task)
        thread.start()

    def frameworkMessage(self, driver, message):
        # Send it back to the scheduler.
        driver.sendFrameworkMessage(message)

    def url_to_image(self, url):
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

    def write_cascade(self, global_path, url):
        try:
            print "Downloading cascade file"

            resp = urllib2.urlopen(url, timeout=5)
            face_cascade = resp.read()
            print global_path + "cascade.xml"
            cascade_file = open(global_path + "cascade.xml", 'w')
            cascade_file.write(face_cascade)
            cascade_file.close()
            print "Downloaded cascade"
            return True
        except:
            print "Error downloading cascade"
            return False

    def find_faces_img(self, url, name, global_path):
        image = self.url_to_image(url)

        if type(image) != bool:
            try:
                face_cascade = cv2.CascadeClassifier(global_path + "cascade.xml")
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.imwrite(name, image)
                print len(faces)
                return [True, len(faces)]
            except:
                print "Error finding faces in image"
                return [False, 0]
        else:
            return [False, 0]

    def download_data_set(self, global_path, dataset, url):
        try:
            print "Downloading dataset"

            resp = urllib2.urlopen(url, timeout=10)
            downloaded_dataset = resp.read()
            dataset_file = open(global_path + dataset + ".zip", 'wb')
            dataset_file.write(downloaded_dataset)
            dataset_file.close()
            print "Dataset downloaded"
            return True
        except:
            print "Error downloading dataset"
            return False

    def unzip_data(self, global_path, dataset):
        try:
            print "Unzipping dataset"
            zip_ref = zipfile.ZipFile(global_path + dataset + '.zip', 'r')
            zip_ref.extractall(global_path)
            zip_ref.close()
            os.remove(global_path + dataset + '.zip')
            print "Unzipping complete"
            return True
        except:
            print "Error unzipping data"
            return False

    def main_func(self, start_file):
        start_time = time.time()
        print "Start Time::" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        dataset = "vgg_face_dataset"
        global_path = ("/home/cc/fd/")
        dataset_url = "https://github.com/anurag2301/cloudmesh.mesos/raw/master/vgg_face_dataset.zip"
        cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        no_images_per_file = 5
        no_files = 10

        if not os.path.exists(global_path):
            os.makedirs(global_path)
        itr = 1

        result = ""
        if self.download_data_set(global_path, dataset, dataset_url):
            if not self.unzip_data(global_path, dataset):
                return False

        if not os.path.exists(global_path + "cascade.xml"):
            if not self.write_cascade(global_path, cascade_url):
                return False
        input_folder_name = global_path + dataset + "/files/"
        file_list = os.listdir(input_folder_name)
        output_folder_name = global_path + "output/"
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
        for file_name in file_list:
            if start_file > 1:
                start_file -= 1
                continue
            if itr > no_files:
                break
            itr += 1
            print "Reading file::" + file_name
            with open(input_folder_name + file_name) as f:
                content = f.readlines()
                f.close()
            img_no = 1
            for line in content:
                if img_no > no_images_per_file:
                    break
                link = str.split(line)
                if len(link) > 6:
                    print "Getting image from URL::" + link[1]
                    head_count = self.find_faces_img(link[1], output_folder_name + file_name + link[0] + ".jpg",
                                                     global_path)
                    if head_count[0]:
                        img_no += 1
                        result += file_name + link[0] + " " + link[1] + " " + str(head_count[1]) + "\r\n"

        end_time = time.time()
        result = str(end_time - start_time) + "\r\n" + result
        print "Writing results"
        if os.path.exists(global_path + "output/results.txt"):
            with open(global_path + "output/results.txt") as f:
                content = f.readlines()
                f.close()
                result += "\r\n"
                for line in content:
                    result += line
            os.remove(global_path + "output/results.txt")
        result_file = open(global_path + "output/results.txt", 'w')
        result_file.write(result)
        result_file.close()

        # Removing dataset
        print "Deleting dataset"
        shutil.rmtree(global_path + dataset)
        print "Deleting cascade file"
        os.remove(global_path + "cascade.xml")
        end_time = time.time()
        print "End Time::" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        print "Total Time::" + str(end_time - start_time)

if __name__ == "__main__":
    print "Starting executor"
    driver = mesos.native.MesosExecutorDriver(MyExecutor())
    sys.exit(0 if driver.run() == mesos_pb2.DRIVER_STOPPED else 1)



