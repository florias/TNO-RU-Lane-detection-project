class WorldModel(object):
    """Internal representation of the world.

    Representation of the road, the ego vehicle, targets, and the vehicle's field of view. It keeps track of all these
    objects and allows easy access to every instance currently available.

    Attributes:
        road: an instance of type Road representing the current road.
        egovehicle: The Ego Vehicle in which the system is situated.
        targets: list of type Vehicle containing all other cars on the road in
        range of the radar. fov: a polygon of the Ego car's field of view; type
        List<(Float, Float)>.
    """

    def __init__(self, egovehicle, fov):
        """Initializes the WorldModel class. There are no initial roads or
        targets until the processing has begun."""
        self.road = None
        self.egovehicle = egovehicle
        self.targets = None
        self.fov = fov

    def update_targets(self, targets_update):
        """Updates the list of targets."""
        self.targets = targets_update

    def update_road(self, road_update):
        """Updates the road."""
        self.road = road_update

    def get_road(self):
        """Retrieves the current road."""
        return self.road

    def get_egovehicle(self):
        """Retrieves the ego vehicle."""
        return self.egovehicle

    def get_targets(self):
        """Retrieves the list of targets."""
        return self.targets

    def get_fov(self):
        """Retrieves the field of view of the Ego vehicle."""
        return self.fov
