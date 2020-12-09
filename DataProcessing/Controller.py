from PyQt4 import QtCore, QtGui
import thread
import tensorflow as tf
from rospy import Time
from keras.models import load_model
from keras.backend import set_session

from Model.WorldModel import WorldModel
from Model.EgoVehicle import EgoVehicle
from Model.TargetVehicle import TargetVehicle
from Model.Road import Road
from ImageProcessing.Sampler import Sampler
from ImageProcessing.Extrapolation import Extrapolation
from ImageProcessing.Visualiser import Visualiser
from LaneDetection.LaneDetector import LaneDetector
import DataProcessing.Listeners.src.live_reader.scripts.listener as listener
import os, sys

class Controller(object):
    """Connects all other classes and controls the flow of the program.

    Regulates the input/output and connects the listeners to the visualiser
    and gui. The worldmodel is also initialised here to keep track of the 
    internal representation. The listeners pass the input which is stored
    in the worldmodel, which is then used to make a visualisation and pass
    to the gui for drawing.

    Attributes:
        core_terminal: QWidget that holds the roscore xterm
        play_terminal: QWidget that holds the rosbag play xterm
        lanes: neural network that detects the lanes from a given image
        visualiser: generates scenes to be visualised.
        world_model: stores in internal representation.
        sess: the tensorflow session, necessary for multitreaded functioning
        graph: the default tensorflow graph, also necessary
        model: the neural network model
        extrap: class that extrapolates the generated dots
        file: the path to the bag file we're working with
        raw_queue: multithreading Queue used to pass raw images to the GUI
        lane_queue: multithreading Queue used to pass lane images to the GUI
        visual_queue: multithreading Queue used to pass visualisation images 
            to the GUI
        raw_image_ready: python Event used to signal when a raw image is ready
        lane_image_ready: python Event used to signal when a lane image 
            is ready
        visual_image_ready: python Event used to signal when a visualisation 
            image is ready
        time_dots: the list of (time,dots) tuples that will be written to 
            the bag
    """


    def __init__(self, core_terminal, play_terminal, file, raw_image_ready,
                 lane_image_ready, visual_image_ready, raw_queue, lane_queue,
                 visual_queue, time_dots, play_pause):
        self.ld = LaneDetector()
        self.world_model = WorldModel(EgoVehicle(0, 0), None)
        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        set_session(self.sess)
        if getattr(sys, 'frozen', False):
            model_path = os.path.join(os.path.dirname(sys.executable), 'LaneDetection/full_CNN_model.h5')
        else:
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../LaneDetection/full_CNN_model.h5')
        self.model = load_model(model_path)
        self.extrap = Extrapolation()
        self.visualiser = Visualiser(640, 960, self.world_model)
        self.sampler = Sampler()
        self.file = file
        self.raw_queue = raw_queue
        self.lane_queue = lane_queue
        self.visual_queue = visual_queue
        self.raw_image_ready = raw_image_ready
        self.lane_image_ready = lane_image_ready
        self.visual_image_ready = visual_image_ready
        self.time_dots = time_dots
        self.search_process = QtCore.QProcess()
        self.core_terminal = core_terminal
        self.play_terminal = play_terminal
        self.core_process = QtCore.QProcess()
        self.play_process = QtCore.QProcess()
        self.play_pause_id = play_pause
        if len(self.file) > 0:
            self.start_playterminal()
        self.start_coreterminal()
        thread.start_new_thread(listener.listen, (self,))


    """
    The following update functions are used for both online and offline
    reading through the use of listeners. When the listeners receive new data
    they call the appropriate Controller function that then processes and
    updates the visualisation/gui.
    """

    def update_targets(self, targets):
        """Updates the targets when called by the listener and updates the 
        world_model.
        """
        position_targets = []
        for target in targets.targets:
            position_targets.append(TargetVehicle(target.kinodynamics.pose.x,
                                                  target.kinodynamics.pose.y,
                                                  target.id))
        self.world_model.update_targets(position_targets)

    def update_image(self, frame, time):
        """Updates the image when called by the listener, detects the lanes
        from the image and updates the world_model. Gets the scene from the 
        visualiser and draws it with the GUI."""
        self.raw_queue.put(frame)
        self.raw_image_ready.set()
        raw_plus_lanes, _, top_down_lanes = self.ld.get_road_lines(frame,
                                                                  self.model,
                                                                  self.graph,
                                                                  self.sess)
        self.lane_queue.put(raw_plus_lanes)
        self.lane_image_ready.set()
        dots = self.sampler.find_dots(top_down_lanes)
        self.time_dots.append((time, dots))
        self.world_model.update_road(Road(self.extrap.extrapolate_dots(dots)))
        scene = self.visualiser.make_scene()
        self.visual_queue.put(scene)
        self.visual_image_ready.set()

    def kill_terminals(self):
        """Kills both terminal processes"""
        self.play_process.terminate()
        self.core_process.terminate()

    def start_playterminal(self):
        """Starts the rosbag play terminal process"""
        self.play_process.start('xterm', ['-into',
                                          str(self.play_terminal.winId()),
                                          '-hold', '-e',
                                          'source /opt/ros/melodic/setup.bash'
                                          '; rosbag play --pause ' +
                                          self.file[0]])
        self.play_pause_id.append(self.play_process.pid())

    def start_coreterminal(self):
        """Starts the roscore terminal process"""
        self.core_process.start('xterm', ['-into',
                                          str(self.core_terminal.winId()),
                                          '-hold', '-e',
                                          'source /opt/ros/melodic/setup.bash'
                                          '; roscore'])