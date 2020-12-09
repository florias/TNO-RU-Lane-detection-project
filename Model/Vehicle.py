from abc import ABCMeta


class AbstractVehicle:
    """Class which represents a base vehicle.

    All vehicles are stored in this class and all are treated as cars with equal
    sizes. There are two types of children of this abstract class, EgoVehicle
    and TargetVehicle. The former is the owner's vehicle in which the radar and
    camera are positioned, and the latter is all other vehicles on the road.

    Attributes:
        x_pos: x position as float.
        y_pos: y position as float.
    """
    __metaclass__ = ABCMeta

    def __init__(self, x_pos, y_pos):
        """Initializes the vehicle."""
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_x(self):
        """Retrieves the x-coordinate of the vehicle."""
        return self.x_pos

    def get_y(self):
        """Retrieves the y-coordinate of the vehicle."""
        return self.y_pos
