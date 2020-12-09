import numpy as np
import copy


class Extrapolation:
    """Extrapolates dots to account for unknown data points behind the car.

    If there is no previous observation, the extrapolation output is the same as
    the observation. For all subsequent times the extrapolation is called, push
    down the previous observation's coordinates down by the standard vertical
    distance. Then, check whether a line is added or removed, if so, check what
    the index of the added or removed line is. Use these indices to either
    remove a line from the extrapolation process in the case of a line being
    removed, or in the case of a newly observed line, insert the newly observed
    line at the right index for the extrapolation process. Then the new
    observations are put in the intermediate list we use through this class, so
    that the the observation part of the extrapolated list is overwritten to
    have an up to date observation. Then, we would in principle have an output
    of extrapolated but we also do outlier checking, based on the standard
    deviation of the corresponding observation of a certain line, to make sure
    noise in the camera or lane detection doesn't result in line that cross
    multiple lanes and get extrapolated back.


    Attributes:
        max_list_length: Integer that represents the maximum length a list of
        coordinates can have.
        x_dist_between_dots: Integer that represents the standard vertical
        distance between coordinates in a line.
        observation: list of list of coordinates that the camera currently sees.
        resulting_dots: list of list of coordinates that the extrapolation outputs.
    """

    def __init__(self, max_list_length=40, x_dist_between_dots=31):
        """Initializes the Extrapolation class."""
        self.max_list_length = max_list_length
        self.x_dist_between_dots = x_dist_between_dots
        self.observation = []
        self.resulting_dots = []

    def extrapolate_dots(self, coordinates):
        """Update the internal states of the class."""
        assert (isinstance(coordinates, list)), \
            "The input to the extrapolation should be a list (of lists), " \
            "it is currently not a list"
        self.observation = coordinates
        self.check_list_lengths()
        if not self.resulting_dots:
            self.resulting_dots = copy.deepcopy(self.observation)
        else:
            self.resulting_dots = self.add_to_existing_list()
        clean_result = self.clean_up_list(self.resulting_dots)
        return clean_result

    def add_to_existing_list(self):
        """Update the intermediate list."""
        intermediate_list = self.resulting_dots
        intermediate_list = self.push_down_prev_observation(intermediate_list)
        # Adapt to changes in lines
        if len(self.observation) != len(self.resulting_dots):
            if len(self.observation) < len(self.resulting_dots):
                while len(self.observation) < len(self.resulting_dots):
                    index_removed_line = self.index_line_removed()
                    del intermediate_list[index_removed_line]
            if len(self.observation) > len(self.resulting_dots):
                while len(self.observation) > len(self.resulting_dots):
                    index_new_line = self.index_line_added()
                    intermediate_list.insert(index_new_line,
                                             self.observation[index_new_line])
        if self.observation:
            intermediate_list = self.update_obs_part(intermediate_list)
        intermediate_list = self.remove_outliers(intermediate_list)
        return intermediate_list

    def push_down_prev_observation(self, intermediate_list):
        """Push all observations down by the standard distance."""
        for l, line in enumerate(self.resulting_dots):
            for d, dot in enumerate(line):
                if dot:
                    current_dot = list(intermediate_list[l][d])
                    current_dot[1] = dot[1] + self.x_dist_between_dots
                    intermediate_list[l][d] = tuple(current_dot)
        for new_line in intermediate_list:
            new_line.insert(0, [])
        return intermediate_list

    def index_line_added(self):
        """Find the index of the line that is added."""
        last_dots = self.get_last_dots()
        min_distances = []
        for i, line in enumerate(self.observation):
            dist = []
            dots_x = 0
            for last_dot in reversed(line):
                if last_dot:
                    dots_x = last_dot[0]
                    break
            for j, prev_last_dot in enumerate(last_dots):
                prev_last_dot_x = prev_last_dot[0]
                dist.append(abs(prev_last_dot_x - dots_x))
            min_distances.append(min(dist))
        index_new_line = min_distances.index(max(min_distances))
        return index_new_line

    def index_line_removed(self):
        """Find the index of the line that is removed."""
        last_dots = self.get_last_dots()
        index_removed_line = 0
        min_distances = []
        for i, prev_last_dot in enumerate(last_dots):
            dist = []
            dots_x = 0
            prev_last_dot_x = prev_last_dot[0]
            for j, line in enumerate(self.observation):
                for last_dot in reversed(line):
                    if last_dot:
                        dots_x = last_dot[0]
                        break
                dist.append(abs(prev_last_dot_x - dots_x))
            if dist:
                min_distances.append(min(dist))
        if min_distances:
            index_removed_line = min_distances.index(max(min_distances))
        return index_removed_line

    def get_last_dots(self):
        """Return the last dots of the previous output of the class."""
        last_dots = []
        for i in range(len(self.resulting_dots)):
            for last_dot in reversed(self.resulting_dots[i]):
                if last_dot:
                    last_dots.append(last_dot)
                    break
        return last_dots

    def update_obs_part(self, intermediate_list):
        """The overlapping part of the observation and the extrapolated output
        should be updated to the observation."""
        for l, line in enumerate(self.observation):
            for d, dot in enumerate(line):
                if dot:
                    intermediate_list[l][d] = dot
        return intermediate_list

    def check_list_lengths(self):
        """Make sure the list doesn't exceed a certain length."""
        for l, line in enumerate(self.resulting_dots):
            if len(line) > self.max_list_length:
                self.resulting_dots[l] = line[:self.max_list_length]

    def remove_outliers(self, intermediate_list):
        """Remove lines that cross lanes to get rid of noise."""
        cleaned_list = self.clean_up_list(intermediate_list)
        for l, line in enumerate(intermediate_list):
            average = sum(dot[0] for dot in line if dot) / len(cleaned_list[l])
            list_of_xs = [dot[0] for dot in self.observation[l] if dot]
            deviation = 1.6 * np.std(list_of_xs)
            if line:
                for p, point in enumerate(line):
                    if point:
                        if point[0] < average - deviation or point[0] > \
                                average + deviation:
                            intermediate_list[l][p] = []
        return intermediate_list

    @staticmethod
    def clean_up_list(list_to_clean):
        """Return the same list but without the empty entries."""
        cleaned_list = []
        for i, lane in enumerate(list_to_clean):
            cleaned_list.append([x for x in lane if x != []])
        return cleaned_list
