import numpy as np


class Generator(object):
    """Generates mock-up data for lane positions.

    Generates a matrix consisting of lanes with 100 pairs of coordinates indicating the lanes' position. All lanes are
    straight and the purpose is to test the visualiser.

    Attributes:
        width: width of the lanes in m, taken as the average lane width.
        nr_lanes: number of lanes on the road.
        dots: matrix of all the positions.
    """

    def __init__(self, nr_lanes, nr_dots, width=3.7):
        """Initializes the Generator class, width is set at 3.7m."""
        self.width = width
        self.nr_lanes = nr_lanes
        self.nr_dots = nr_dots
        self.dots = np.empty((nr_lanes, nr_dots, 2, 2))

    def generate(self):
        """Generates mock-up data for nr_lanes amount of lanes.

        The starting position on the same y as the Ego vehicle, but
        50 meters back as the lane positions extend 50 meters ahead
        and backward from the Ego vehicle. All measurements are in cm.

        Returns the matrix of positions.
        """
        y = 0.0
        for i in range(self.nr_lanes):
            x = 0
            for j in range(self.nr_dots):
                self.dots[i, j] = [[x, y], [x, y+self.width]]
                x += 1
            y += self.width
        return self.dots
