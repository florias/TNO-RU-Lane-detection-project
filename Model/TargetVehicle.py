from Model import Vehicle


class TargetVehicle(Vehicle.AbstractVehicle):
    """Class which represents other vehicles.

    Vehicle class for any vehicle that isn't the Ego vehicle which are detected
    by the radar.

    Attributes:
        car_id: the id of the car according to the radar data.
    """

    def __init__(self, x_pos, y_pos, car_id):
        """Initializes the TargetVehicle class by creating a base Vehicle."""
        super(TargetVehicle, self).__init__(x_pos, y_pos)
        self.car_id = car_id

    def get_car_id(self):
        """Retrieves the car identification number."""
        return self.car_id
