import cv2 as cv
import numpy as np


class Sampler(object):
    """Class which extracts the line coordinates from an image.

    Given an image, grey, and white pixels are recognized and clustered together into separate points at certain steps, indicating
    the line's position. The image is first greyscaled and appropriate indices and steps are determined.
    """

    def find_dots(self, img):
        """
        The function find_dots takes an input image, grayscales it, makes sub images of the grayscaled image and runs the functions
        image_sample, find_line, get_valid_elements and line_merger in this order on all the sub images.
        Args:
            img: The output from the neural network

        Returns:
            all_lines: A list containing lists of coordinates of a single line.

        """
        grey_scale_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        amount_of_x_samples = 18
        dots_amount = 12
        x_index = 0
        x_step = (grey_scale_image.shape[1] - 1) / amount_of_x_samples
        y_index = (grey_scale_image.shape[0] - 1)
        y_step = (y_index) / (dots_amount)
        all_lines = []
        while x_index < grey_scale_image.shape[1] - 1:
            y_index, npimg = self.image_sample(grey_scale_image, x_index, x_step)
            line, y_index = self.find_line(y_index, npimg, grey_scale_image, y_step, x_index)
            elements = self.get_valid_elements(line)
            all_lines = self.line_merger(all_lines, line, elements)
            if elements > 3:
                all_lines.append(line)
            x_index = x_index + x_step
        return all_lines

    def image_sample(self, image, x_index, x_step):
        """
        image_samples takes an image and takes a sub image y size of image and x size of x_step starting from
        image at x coordinate x_index
        Args:
            image: GreyScaled original image
            x_index: Indicates the x value of the start of sub_image
            x_step: Sets the x size of the sub_image

        Returns:sub_image

        """
        roi = image[0:image.shape[0] - 1, x_index:  x_index + x_step]
        sub_image = np.asarray(roi)
        y_index = image.shape[0] - 1
        return y_index, sub_image

    def find_line(self, y_index, sub_image, image, y_step, x_index):
        """
        find_lines takes a smaller part of the original image and searches for a line in this part of the image.

        Args:
            y_index: At which part of the sub_image the function currently is looking for line coordinates
            sub_image: part of image divided by the x_index and x_step
            image: GreyScaled original image
            y_step: The y distance between the find_line functions searching for line coordinates
            x_index: Indicates the x value of the start of what sub_image is currently being searched for line values

        Returns: line, y_index

        """
        line = []
        while y_index >= y_step:
            indices = np.where(sub_image[(image.shape[0] - 1) - y_index, :] > 15)
            y_index = y_index - y_step
            if len(indices[0]) > 0:
                line.append(((sum(indices[0]) / len(indices[0])) + x_index, image.shape[0] - 1 - y_index))
            else:
                line.append([])
        return line, y_index

    def get_valid_elements(self, line):
        """
        get_valid_elements detects how many non-empty elements line has and
        returns this value.
        Args:
            line: Array containing the coordinates of last detected line

        Returns: elements_in_lines

        """
        elements_in_lines = 0
        for elements in line:
            if elements:
                elements_in_lines = elements_in_lines + 1
        return elements_in_lines

    def line_merger(self, all_lines, line, elements):
        """
        The liner_merger function merges a line with a previous detected line stored in coordinates
        if the average x coordinate is within a certain range, width_treshold.
        Args:
            all_lines: array containing all the lines detected up until this point
            line: Array containing the coordinates of last detected line
            elements: the amount of line coordinates detected for every y_step

        Returns: all_lines

        """
        width_treshold = 58
        last_saved_line = []
        if all_lines:
            last_saved_line = [x for x in all_lines[-1] if x]
        current_line_not_empty = [x for x in line if x]

        if all_lines and current_line_not_empty and elements > 3:
            if (sum([k for k, v in last_saved_line]) / len(last_saved_line)) > (
                    sum([k for k, v in current_line_not_empty]) / len(current_line_not_empty) - width_treshold):
                for i in range(len(line) - 1):
                    if all_lines[-1][i] and line[i]:
                        line[i] = ((all_lines[-1][i][0] + line[i][0]) / 2, line[i][1])
                    elif all_lines[-1][i]:
                        line[i] = all_lines[-1][i]
                    else:
                        pass
                del all_lines[-1]
        return all_lines