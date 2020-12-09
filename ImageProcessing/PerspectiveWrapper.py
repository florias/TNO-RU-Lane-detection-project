from __future__ import division
import numpy as np
import cv2


class PerspectiveWrapper(object):
    """Class which wraps the perspective to a bird's-eye view."""

    def __init__(self):
        pass

    @staticmethod
    def top_down(img):
        """Wraps an image of any size to a bird's-eye view using cv2."""
        image_w = img.shape[1]
        image_h = img.shape[0]
        multiplier_w = img.shape[1] / 640
        multiplier_h = img.shape[0] / 480
        multiplier_hsq = multiplier_h * multiplier_h

        pts1 = np.float32(
            [[0, image_h - 70], [image_w, image_h - 70],
             [0, (175 * multiplier_hsq)],
             [image_w, (175 * multiplier_hsq)]])
        pts2 = np.float32(
            [[(250 * multiplier_w), image_h], [(390 * multiplier_w), image_h],
             [(-300 * multiplier_w), (-300 * multiplier_hsq)],
             [image_w + (300 * multiplier_w), (-300 * multiplier_hsq)]])

        m, _ = cv2.findHomography(pts1, pts2)
        dst = cv2.warpPerspective(img, m, (image_w, image_h))
        return dst
