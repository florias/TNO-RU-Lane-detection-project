import cv2
import numpy as np


class Visualiser(object):
    """Visualizes the world model for the GUI.

    Draws the targets, the ego, and the road, which are stored in a world
    model and given by the controller.

    Attributes:
        world_model: the instance of the world model class
        x: the width of the visualisation
        y: the height of the visualisation
    """

    def __init__(self, x, y, world_model):
        self.world_model = world_model
        self.x = x
        self.y = y

        self.x_scale_fac = 4
        self.y_scale_fac = 35

    def make_scene(self):
        """Makes a scene and draws the lines and targets on it."""
        scene = np.zeros(shape=[self.y, self.x, 3])
        scene += 30 # Making it a bit more pleasant to the eyes

        targets = self.world_model.get_targets()
        lines = self.world_model.get_road()
        self.draw_lines(scene, lines)
        self.draw_ego(scene)
        self.draw_scale(scene)
        self.draw_targets(scene, targets)
        return scene

    def draw_lines(self, scene, road):
        """Draws a list of lines on the scene."""
        for line in road.get_lines():
            cv2.polylines(scene, np.int32([line]), 0, [180, 180, 180], 2)
            for index, item in enumerate(line):
                if index == len(line) - 1:
                    break
                cv2.circle(scene, item, 5, [200, 200, 200])

    def draw_ego(self, scene):
        """Draws the ego vehicle on the scene."""
        cv2.circle(scene, (int(scene.shape[1] / 2), int(scene.shape[0] / 2)),
                   15, [255, 155, 0])

    def draw_scale(self, scene, range = 50, line_len = 5):
        """
        Draws a scale, based on x and y scaling factors
        """
        x = int(scene.shape[1])
        y = int(scene.shape[0])

        points = np.array([
            [(0, y/2),
            (line_len, y/2)],

            [(x-line_len, y/2),
            (x, y/2)],

            [(0, y/2 + self.x_scale_fac * range),
             (line_len, y/2 + self.x_scale_fac * range)],

            [(x - line_len, y/2 + self.x_scale_fac * range),
             (x, y/2 + self.x_scale_fac * range)],

            [(0, y/2 - self.x_scale_fac * range),
             (line_len, y/2 - self.x_scale_fac * range)],

            [(x - line_len, y/2 - self.x_scale_fac * range),
             (x, y/2 - self.x_scale_fac * range)],
        ])

        cv2.polylines(scene,
                      points,
                      color = [150, 150, 150],
                      thickness = 2,
                      isClosed=False)

        cv2.putText(scene, '0m', tuple(points[0][1]), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
                    color=(150, 150, 150))
        cv2.putText(scene, str(range) + 'm', tuple(points[2][1]), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
                    color=(150, 150, 150))
        cv2.putText(scene, str(range) + 'm', tuple(points[4][1]), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5,
                    color=(150, 150, 150))

    def draw_targets(self, scene, targets):
        """Draws the targets on the scene."""
        if targets is not None:
            for target in targets:
                cv2.circle(scene,
                           (int(scene.shape[1] / 2 - (
                                       target.y_pos * self.y_scale_fac)),
                            int(scene.shape[0] / 2 - (
                                        target.x_pos * self.x_scale_fac))),
                           15, [100, 100, 255])
