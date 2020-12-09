from __future__ import division

import time

from Model import Road
from Model import Lane
import numpy as np
import cv2 as cv
from types import NoneType
import numpy as np
import moviepy.editor as mpy
import matplotlib.pyplot as plt
from ImageProcessing.PerspectiveWrapper import PerspectiveWrapper
import tensorflow as tf

from PIL import Image
from glob import glob
from tqdm import tqdm

from get_labels import get_labels
from get_model import get_model
from detect_peaks import detect_peaks

import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
from keras import backend as K
K.set_learning_phase(0)

# Set Memory allocation in tf/keras to Growth
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.inter_op_parallelism_threads = 4
config.intra_op_parallelism_threads = 4
config.allow_soft_placement = True
config.graph_options.optimizer_options.global_jit_level = tf.OptimizerOptions.ON_1
sess = tf.compat.v1.Session(config=config)
K.set_session(sess)


class LaneDetectorCNN:
    def __init__(self):
        # General self.settings for network training and labels (do not change)
        self.settings = dict()
        self.settings['model'] = 'espnet'
        self.settings['shape'] = (640, 480)
        self.settings['random_flip'] = True
        self.settings['random_crop'] = True
        self.settings['epochs'] = 1000
        self.settings['batch_size'] = 1
        self.settings['learning_rate'] = 0.001
        self.settings['weight_decay'] = 0.001
        self.settings['labels'] = 'base'
        self.settings['labels'] = get_labels(self.settings)

        # self.settings for verbosity (with plots)
        self.settings['verbose'] = False
        # Setting to indicate whether to save input images one by one and create a movie afterwards
        self.settings['save'] = False

        # Load pretrained self.model
        _, self.model, _ = get_model(self.settings)
        print(os.getcwd())
        self.model.load_weights('LaneDetectionOld/espnet_base_0.7669_0.7630.hdf5', by_name=True)
        self.model._make_predict_function()
        self.weights = self.model.get_weights()
        weights_array = np.array(self.weights)
        for i in range(len(self.weights)):
            weights_array[i] = np.float16(weights_array[i])
        self.weights = weights_array.tolist()
        self.model.set_weights(self.weights)
        # sess = tf.Session()
        # sess.run(tf.global_variables_initializer())
        # self.default_graph = tf.get_default_graph()
        # self.default_graph.finalize()

    def get_road(self, img):
        lanes = self.get_lanes(img)
        road = Road(lanes)

        return road

    def get_lanes(self, img):
        return lanes

    def detect_lanes(self, img):
        image_w = img.shape[1]
        image_h = img.shape[0]

        # Load original image
        image = np.array(img).astype(np.float32) / 255

        # Resize it to network dimensions
        image_small = cv.resize(image, (640, 480), interpolation=cv.INTER_LINEAR)

        # with self.default_graph.as_default():
        # Predict
        image_pred_small = self.model.predict(np.expand_dims(image_small, axis=0), batch_size=len(image_small))[0]

        # Resize prediction back to original size
        image_pred = cv.resize(image_pred_small, (image_w, image_h), interpolation=cv.INTER_LINEAR)

        # Get RGB image from label predictions
        image_seg = y_label_to_rgb(self.settings, image_pred.argmax(axis=-1).astype(np.int))

        # Transform image to flat representation
        image_seg_flat = car_to_bird(image_seg)

        # Extract lane markings
        image_seg_flat_lane_markings = np.zeros((image_seg_flat.shape[:2]), dtype=np.uint8)
        image_seg_flat_lane_markings[np.where((image_seg_flat == [255, 255, 255]).all(axis=2))] = [255]

        # Extract road information
        image_seg_flat_lane_edge_road = np.copy(image_seg_flat_lane_markings)
        image_seg_flat_lane_edge_road[np.where((image_seg_flat == [128, 64, 128]).all(axis=2))] = [255]
        image_seg_flat_lane_edge_road[np.where((image_seg_flat == [244, 35, 232]).all(axis=2))] = [255]

        # Extract car/person information (in addition to road information)
        image_seg_flat_lane_edge_car = np.copy(image_seg_flat_lane_edge_road)
        image_seg_flat_lane_edge_car[np.where((image_seg_flat == [0, 0, 142]).all(axis=2))] = [255]
        image_seg_flat_lane_edge_car[np.where((image_seg_flat == [128, 64, 128]).all(axis=2))] = [255]

        # intersection edge detection between road-information and road-person-car information
        image_seg_flat_lane_edge = np.zeros((image_seg_flat.shape[:2]), dtype=np.uint8)
        image_seg_flat_lane_edge[(cv.Canny(image_seg_flat_lane_edge_road, 64, 192).astype(np.int) + cv.Canny(
            image_seg_flat_lane_edge_car, 64, 192).astype(np.int)) > 255] = 255

        # Combine intersection with extracted lane markings
        image_seg_flat_lane = np.zeros((image_seg_flat.shape[:2]), dtype=np.uint8)
        image_seg_flat_lane[image_seg_flat_lane_markings >= 255] = 255
        # Since line below is commented out, only lane markings are checked as lane lines, and not road-sidewalk edges
        # etc.
        # image_seg_flat_lane[image_seg_flat_lane_edge >= 255] = 255
        # Hough transformation to find straight lines in image_seg_flat_lane
        image_flat_lines = np.zeros((image_seg_flat.shape[:2]), dtype=np.uint8)
        lines = cv.HoughLinesP(image_seg_flat_lane, 6, np.pi / 130, 50, np.array([]), 10, 100)

        if type(lines) != NoneType:  # POOPOO ALERT
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv.line(image_flat_lines, (x1, y1), (x2, y2), 255, 1)




        # # Detect peaks in bottom part (all except first 160px) of picture
        # line_flat_peaks = (np.sum(image_flat_lines[0:, :], axis=0) / 255).astype(np.int32)
        # peaks = detect_peaks(line_flat_peaks, mph=20, mpd=40, show=False).astype(np.int)
        # # Find, for each peak, its lower/upper bound (based on when the line_flat_peaks returns 0)
        # peaks_lower = np.zeros(len(peaks), dtype=np.int)
        # peaks_upper = np.zeros(len(peaks), dtype=np.int)
        # for j in range(len(peaks)):
        #     pos_left = np.where(line_flat_peaks[:peaks[j]] == 0)[0]
        #     if len(pos_left) > 0:
        #         peaks_lower[j] = pos_left[-1]
        #     else:
        #         peaks_lower[j] = 0
        #     pos_right = np.where(line_flat_peaks[peaks[j]:] == 0)[0]
        #     if len(pos_right) > 0:
        #         peaks_upper[j] = peaks[j] + pos_right[0]
        #     else:
        #         peaks_upper[j] = 640
        # peaks = np.stack((peaks_lower, peaks, peaks_upper), axis=-1)
        #
        # # Split peaks in those lying left and right of the ego vehicle
        # left_indexes = np.where(peaks[:, 1] < 320)[0]
        # right_indexes = np.where(peaks[:, 1] >= 320)[0]
        # # For all possible lane combinations see if they actually are a lane.
        # lanes = []
        # if len(left_indexes) > 0 and len(right_indexes) > 0:
        #     # Left Lanes
        #     for j in left_indexes[:-1]:
        #         left = peaks[left_indexes[j]]
        #         right = peaks[left_indexes[j + 1]]
        #         if (left[2] - left[0]) < 60 and (right[2] - right[0]) < 60:
        #             lane = StraightLane(left, right, 'left')
        #             if lane.get_confidence(image_seg_flat, image_flat_lines)[0] > 0.1:
        #                 lanes.append(lane)
        #     # Center Lane
        #     left = peaks[left_indexes[-1]]
        #     right = peaks[right_indexes[0]]
        #     if (left[2] - left[0]) < 60 and (right[2] - right[0]) < 60:
        #         lane = StraightLane(left, right, 'center')
        #         if lane.get_confidence(image_seg_flat, image_flat_lines)[0] > 0.1:
        #             lanes.append(lane)
        #     # Right Lane
        #     for j in range(len(right_indexes[1:])):
        #         left = peaks[right_indexes[j]]
        #         right = peaks[right_indexes[j + 1]]
        #         if (left[2] - left[0]) < 60 and (right[2] - right[0]) < 60:
        #             lane = StraightLane(left, right, 'right')
        #             if lane.get_confidence(image_seg_flat, image_flat_lines)[0] > 0.1:
        #                 lanes.append(lane)
        #
        # # Fill top/bottom values of lanes surrounded by two 'larger' lanes
        # for j in range(1, len(lanes) - 1):
        #     top = (lanes[j - 1].top, lanes[j].top, lanes[j + 1].top)
        #     bottom = (lanes[j - 1].bottom, lanes[j].bottom, lanes[j + 1].bottom)
        #     if lanes[j - 1].right[1] == lanes[j].left[1] and lanes[j].right[1] == lanes[j + 1].left[1]:
        #         if np.max([lanes[j - 1].top, lanes[j + 1].top]) < lanes[j].top:
        #             lanes[j].top = np.max([lanes[j - 1].top, lanes[j + 1].top])
        #         if np.min([lanes[j - 1].bottom, lanes[j + 1].bottom]) > lanes[j].bottom:
        #             lanes[j].bottom = np.min([lanes[j - 1].bottom, lanes[j + 1].bottom])
        #
        # # Extract lane images (just for visualization - no further use)
        # image_final_extracted = np.zeros(image_seg_flat.shape, dtype=np.uint8)
        # image_final_created = np.zeros(image_seg_flat.shape, dtype=np.uint8)
        # for lane in lanes:
        #     image_final_extracted[lane.top:lane.bottom + 1, lane.left[1]:lane.right[1], :] = lane.extract_image(
        #         image_seg_flat, image_flat_lines)[lane.top:lane.bottom + 1, lane.left[1]:lane.right[1], :]
        #     image_final_created[lane.top:lane.bottom + 1, lane.left[1] - 2:lane.right[1] + 3,
        #     :] = lane.create_image(
        #         image_seg_flat, image_flat_lines)[lane.top:lane.bottom + 1, lane.left[1] - 2:lane.right[1] + 3, :]

        # Visualize results
        if self.settings['verbose']:
            plot_image(image, 1)
            plot_image(image_small, 2)
            plot_image(image_seg, 3)
            plot_image(image_seg_flat, 4)
            plot_image(image_seg_flat_lane_markings, 5)
            plot_image(image_seg_flat_lane_edge_road, 6)
            plot_image(image_seg_flat_lane_edge_car, 7)
            plot_image(image_seg_flat_lane_edge, 8)
            plot_image(image_seg_flat_lane, 9)
            plot_image(image_flat_lines, 10)
            plot_line(line_flat_peaks, 11)
            plot_image(image_final_extracted, 12)
            plot_image(image_final_created, 13)

        # Save image process from input to detected lanes
        if self.settings['save']:
            image_flat = (car_to_bird(image) * 255).astype(np.uint8)
            image = (image * 255).astype(np.uint8)
            image_flat_lines = np.stack((image_flat_lines, image_flat_lines, image_flat_lines), axis=-1)
            image_final = np.vstack((np.hstack((image, image_flat, image_flat_lines)),
                                    np.hstack((image_seg, image_seg_flat, image_final_created))))
            Image.fromarray(image_final).save(
                'results/{}/{}.png'.format(num, str(i).rjust(len(str(len(img_paths))), '0')))

        # # Create a clip with saved images
        # if self.settings['save']:
        #     clip = mpy.ImageSequenceClip('results/{}'.format(num), fps=10)
        #     clip.write_videofile('results/{}.mp4'.format(num))

        image_flat = (car_to_bird(image) * 255).astype(np.uint8)
        image = (image * 255).astype(np.uint8)
        image_flat_lines = np.stack((image_flat_lines, image_flat_lines, image_flat_lines), axis=-1)
        image_final = np.vstack((np.hstack((image, image_flat, image_flat_lines)),
                                 np.hstack((image_seg, image_seg_flat, image_flat_lines))))

        return image_final, image_flat_lines


# Class for a single straight lane.
class StraightLane:

    # Init
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name
        self.width = self.right[1] - self.left[1]

    # Calculate top/bottom range of lane and extract road information from segmented flat image
    def extract_image(self, full_image, line_image):
        self.extracted_image = np.zeros(full_image.shape, dtype=np.uint8)
        for rgb in [[128, 64, 128], [244, 35, 232], [255, 255, 255]]:
            x, y = np.where((full_image[:, self.left[1]:self.right[1]] == rgb).all(axis=2))
            self.extracted_image[x, y + self.left[1], :] = rgb
        line_image = np.stack((line_image, line_image, line_image), axis=-1)
        if 'left' in self.name:
            self.top = np.where(np.sum(np.sum(line_image[:, self.left[0]:self.left[2], :], axis=2), axis=1) > 0)[0][0]
            self.bottom = np.where(np.sum(np.sum(line_image[:, self.left[0]:self.left[2], :], axis=2), axis=1) > 0)[0][
                -1]
        elif 'right' in self.name:
            self.top = np.where(np.sum(np.sum(line_image[:, self.right[0]:self.right[2], :], axis=2), axis=1) > 0)[0][0]
            self.bottom = np.where(np.sum(np.sum(line_image[:, self.right[0]:self.right[2], :], axis=2), axis=1) > 0)[0][-1]
        else:
            self.top = np.where(np.sum(np.sum(line_image[:, self.left[0]:self.right[2], :], axis=2), axis=1) > 0)[0][0]
            self.bottom = np.where(np.sum(np.sum(line_image[:, self.left[0]:self.right[2], :], axis=2), axis=1) > 0)[0][
                -1]
        return self.extracted_image

    # Get type (road or sidewalk) and confidence value (how much of area of lane dimension is classified as
    # road/sidewalk?)
    def get_confidence(self, full_image, line_image):
        if not hasattr(self, 'extracted_image'):
            self.extract_image(full_image, line_image)
        road_num = len(
            np.where((full_image[self.top:self.bottom + 1, self.left[1]:self.right[1]] == [128, 64, 128]).all(axis=2))[
                0])
        sidewalk_num = len(
            np.where((full_image[self.top:self.bottom + 1, self.left[1]:self.right[1]] == [244, 35, 232]).all(axis=2))[
                0])
        total_num = len(np.ravel(full_image[self.top:self.bottom + 1, self.left[1]:self.right[1], 0]))
        if road_num >= sidewalk_num:
            self.confidence = np.float(road_num / total_num)
            self.confidence_name = 'road'
            self.confidence_rgb = [128, 64, 128]
        else:
            self.confidence = sidewalk_num / total_num
            self.confidence_name = 'sidewalk'
            self.confidence_rgb = [244, 35, 232]
        return (self.confidence, self.confidence_name, self.confidence_rgb)

    # Create a visualization of this Lane
    def create_image(self, full_image, line_image):
        if not hasattr(self, 'extracted_image'):
            self.extract_image(full_image, line_image)
        if not hasattr(self, 'confidence_rgb'):
            self.get_confidence(full_image, line_image)
        self.created_image = np.zeros(self.extracted_image.shape, dtype=np.uint8)
        self.created_image[self.top:self.bottom + 1, self.left[1]:self.right[1]] = self.confidence_rgb
        cv.line(self.created_image, (self.left[1], self.top), (self.left[1], self.bottom), (255, 255, 255), 3)
        cv.line(self.created_image, (self.right[1], self.top), (self.right[1], self.bottom), (255, 255, 255), 3)
        return self.created_image


# Sort image paths by first 'padding' them with '_' (so that '12' does not gets sorted in between '119' and '121' by making it '_12')
def sort_paths(input_img_paths):
    img_paths = []
    for img_path in input_img_paths:
        num = img_path.split('_')[-1].split('.')[0]
        img_path = img_path.replace(str(num) + '.png', str(num).rjust(8, '!') + '.png')
        img_paths.append(img_path)
    img_paths.sort()
    return img_paths


# Transform image from car to bird perspective
def car_to_bird(img):
    pw = PerspectiveWrapper()
    dst = pw.top_down(img)
    return dst


# Convert label predictions to an RGB image
def y_label_to_rgb(settings, y_label):
    y_rgb = np.zeros(y_label.shape + (3,), dtype=np.uint8)
    for i in range(len(settings['labels'][0])):
        name = tuple(settings['labels'][0].keys())[i]
        rgb = settings['labels'][0][name]['rgb']
        y_rgb[y_label == i + 1] = rgb
    return y_rgb


# Plot image
def plot_image(image, fig_num):
    plt.figure(fig_num)
    plt.clf()
    plt.imshow(image)
    plt.pause(0.001)


# Plot line
def plot_line(line, fig_num):
    plt.figure(fig_num)
    plt.clf()
    plt.plot(line)
    plt.pause(0.001)
