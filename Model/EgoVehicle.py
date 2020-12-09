from Model import Vehicle


class EgoVehicle(Vehicle.AbstractVehicle):
    """Class which represents your own car.

    Child of the abstract Vehicle class which represents the special
    Ego vehicle, which indicates this is the driver's vehicle. Has no special
    attributes as of yet, class instance is mainly used as identification.
    """

    def __init__(self, x_pos, y_pos):
        """Initializes the EgoVehicle class by creating a standard Vehicle
        class."""
        super(EgoVehicle, self).__init__(x_pos, y_pos)
