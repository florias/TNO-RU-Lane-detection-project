class Line(object):
    """Represents a line on the road, which consists of a list of coordinates.

    Attributes:
        line_id: an integer indicating which line this is.
        coordinates: a list of tuples indicating the coordinates on the line.
    """

    def __init__(self, line_id, coordinates):
        """Initializes the Line class."""
        self.line_id = line_id
        self.coordinates = coordinates

    def get_coordinates(self):
        """Returns the array of coordinates."""
        return self.coordinates

    def get_id(self):
        """Returns the line's id."""
        return self.line_id
