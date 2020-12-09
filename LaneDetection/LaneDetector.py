
"""
MIT License
Copyright (c) 2017 Michael Virgo
"""

import numpy as np
import cv2
from ImageProcessing.PerspectiveWrapper import PerspectiveWrapper as pw
from scipy.misc import imresize
from keras.backend import set_session


class LaneDetector:

    def __init__(self):
        self.recent_fit = []
        self.avg_fit = []

    def get_road_lines(self, image, model, graph, sess):
        """ Takes in a road image, re-sizes for the model,
        predicts the lane to be drawn from the model in G color,
        recreates an RGB image of a lane and merges with the
        original road image.
        """
        # Get image ready for feeding into model
        small_img = self.resize_image(image)

        # Make prediction with neural network (un-normalize value by multiplying
        # by 255)
        with graph.as_default():
            set_session(sess)
            prediction = model.predict(small_img)[0] * 255  # small_img

        lane_image = self.smoothen_lines(prediction, image)
        blanks = np.zeros_like(self.avg_fit).astype(np.uint8)
        # Merge the lane drawing onto the original image
        result = cv2.addWeighted(image, 1, lane_image, 1, 0)
        lane_drawn = np.dstack((blanks, prediction, blanks))

        return result, (imresize(lane_drawn, (
        image.shape[0], image.shape[1]))), pw.top_down(lane_image)

    def resize_image(self, image):
        """
        resizes the image to size that fits the neural network
        """
        resized_img = imresize(image, (80, 160, 3))
        resized_img = np.array(resized_img)
        resized_img = resized_img[None, :, :, :]
        return resized_img

    def smoothen_lines(self, prediction, image):
        """
        Uses previous model predictions to improve future predictions
        """
        # Add lane prediction to list for averaging
        self.recent_fit.append(prediction)

        # Only using last five for average
        if len(self.recent_fit) > 5:
            self.recent_fit = self.recent_fit[1:]

        # Calculate average detection
        self.avg_fit = np.mean(np.array([i for i in self.recent_fit]), axis=0)

        # Generate fake R & B color dimensions, stack with G
        blanks = np.zeros_like(self.avg_fit).astype(np.uint8)
        lane_drawn = np.dstack((blanks, self.avg_fit, blanks))
        # Re-size to match the original image
        lane_image = imresize(lane_drawn, image.shape)
        return lane_image
