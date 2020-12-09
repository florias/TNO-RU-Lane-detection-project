class Road(object):
    """Internal representation of a road, contains a list of lines.

    Attributes:
        lines: a list of type Line containing the lines of the road.
    """

    def __init__(self, lines):
        """Initializes the Road class."""
        self.lines = lines

    def get_lines(self):
        """Returns the lines."""
        return self.lines

    def get_nr_lines(self):
        """Returns the number of lines."""
        return len(self.lines)
