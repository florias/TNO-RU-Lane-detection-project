
from types import NoneType
from ImageProcessing.PerspectiveWrapper import PerspectiveWrapper
from LaneDetectionOld.LaneDetectorCNN import LaneDetectorCNN
# from What import MakeDotProduct
from scipy.misc import imresize
import pickle
import rosbag
import os
from keras.models import load_model



# import the necessary packages
import numpy as np
import cv2
################## INit ###########################
bag_list = os.listdir('BagFiles')


image_topics = ['/prius1/camera_front_center/image_raw/compressed']  # Set the topic where the images are
model = load_model('Data/full_CNN_model.h5')
# initial testing bag
ob = LaneDetectorCNN()
pw = PerspectiveWrapper()


def extractDigits(lst):
    test = np.zeros(shape=(80, 160, 1))
    for c in range(lst.shape[0]):
        for d in range(lst.shape[1]):
            test[c][d][0] = lst[c][d]
    return test


############# Run the lane detection ######################

trainss = []
labels = []
counter = 0
for abl in bag_list:
    bag = rosbag.Bag("BagFiles/" + abl)
    counter += 1


    for topic, msg, t in bag.read_messages(topics=image_topics, raw=False):

        img_array = np.fromstring(msg.data, np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        q, line_img, a, yup = ob.detect_lanes(frame)

        # define range of white color in HSV
        # change it according to your need !

        lower_white = np.array([230, 230, 230], dtype=np.uint8)
        upper_white = np.array([255, 255, 255], dtype=np.uint8)
        blank_image = np.zeros(shape=[frame.shape[0], frame.shape[1], 3], dtype=np.uint8)
        # Threshold the HSV image to get only white colors
        mask = cv2.inRange(a, lower_white, upper_white)
        houghlines = cv2.HoughLinesP(mask, 0.98, np.pi / 180, 50, np.array([]), 6, 30)
        if type(houghlines) != NoneType:
            for b in houghlines:
                if -5 > np.arctan2(b[0][3] - b[0][1], b[0][2] - b[0][0]) * 180.0 / np.pi or 5 < np.arctan2(
                        b[0][3] - b[0][1], b[0][2] - b[0][
                            0]) * 180.0 / np.pi:
                    cv2.line(blank_image, (b[0][0], b[0][1]), (b[0][2], b[0][3]), (255, 255, 255), 1)

        yup = imresize(yup, (80, 160, 3))
        mask = imresize(mask, (80, 160, 1))
        tur = blank_image
        blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        blank_image = imresize(blank_image, (80, 160, 1))
        trainss.append(np.asarray(yup))

        blank_image = extractDigits(blank_image)
        labels.append(np.asarray(blank_image))

        if cv2.waitKey(10) != ord('q'):  # Display the images until q is pressed
            pass
        else:
            break

    # ---------------------------------------------------------------------------------------
    print (counter, "bag file done")
    bag.close()
    cv2.destroyAllWindows()


pickle.dump(trainss, open("newTrainData.pkl", "wb"), protocol=2)
pickle.dump(labels, open("newLabelData.pkl", "wb"), protocol=2)