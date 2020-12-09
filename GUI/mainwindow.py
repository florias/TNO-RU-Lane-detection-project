from PyQt4 import QtCore, QtGui
from gui import Ui_MainWindow
from ImageUpdate import ImageUpdate
from DataProcessing.Writer import Writer
from DataProcessing.Controller import Controller
from multiprocessing import Manager, Event, Queue
from subgui import Ui_Dialog
import sys
from subprocess import Popen, PIPE

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class MainWindow(QtGui.QMainWindow):
    """
    Main GUI class, creates the GUI, its buttons and output and ties them all 
    to the controller classes. The class inherits from a QT QMainwindow widget 
    which defines the specifications of the buttons, GUI and other aspects.
    """
    def __init__(self):
        """
        Creates the GUI itself and loads all of the sections needed for the 
        program to run properly.
        """
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.guiSetup()
        self.controller = None
        self.state = False
        self.live = False

        #Manager meant to manage the multiprocessed variables and prevents issues
        self.manager = Manager()
        self.file_available = self.manager.list()
        self.play_pause_list = self.manager.list()

        self.raw_images_ready, self.lane_images_ready, self.visual_images_ready = self.manager_event_creator()
        self.raw_q, self.lane_q, self.visual_q = self.manager_queue_creator()

        # Creates the image updaters which will update the image whenever the controller process sends a signal
        self.raw_image_updater = ImageUpdate(self.raw_images_ready, self.raw_q, True, self)
        self.lane_image_updater = ImageUpdate(self.lane_images_ready, self.lane_q, True, self)
        self.visual_image_updater = ImageUpdate(self.visual_images_ready, self.visual_q, False, self)
        self.image_updater()

        # Creates the writer and the list that the time and dots will be placed in.
        self.time_dots = []
        self.writer = Writer(self.time_dots)


    def guiSetup(self):
        """
        Sets up additional necessary parts of the GUI that could not be set natively in Qt
        """
        self.ui.playButton.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        self.setWindowTitle("Lane Detection")

    def image_updater(self):
        """
        Connects the signals with the functions that are to be called, also starts the image updater processes
        """
        self.raw_image_updater.image_signal.connect(self.set_raw_image)
        self.lane_image_updater.image_signal.connect(self.set_lane_image)
        self.visual_image_updater.image_signal.connect(self.set_visual_image)
        self.raw_image_updater.start()
        self.lane_image_updater.start()
        self.visual_image_updater.start()

    def manager_event_creator(self):
        """
        Creates the events that the image updater processes use to know when an image is ready to be displayed
        """
        raw_images_event = Event()
        lane_images_event = Event()
        visual_images_event = Event()
        return raw_images_event, lane_images_event, visual_images_event,

    def manager_queue_creator(self):
        """
        Creates a queue which houses the images to be displayed
        """
        raw_images_queue = Queue()
        lane_images_queue = Queue()
        visual_images_queue = Queue()
        return raw_images_queue, lane_images_queue, visual_images_queue

    def run(self):
        """
        Connect buttons and starts the multi-threaded processes
        """
        self.select_source()
        self.on_play_click()
        self.on_quit_click()
        self.on_writetobag_click()
        self.controller = Controller(self.ui.rosCoreWidget,
            self.ui.rosPlayWidget, self.file_available, self.raw_images_ready, 
            self.lane_images_ready, self.visual_images_ready, self.raw_q, self.lane_q, 
            self.visual_q, self.time_dots, self.play_pause_list)

    def select_source(self):
        window = SubWindow(self)
        window.run()
        window.show()
        window.exec_()

    def on_writetobag_click(self):
        """
        Connects the write to bag button to the Writer write_dots 
        function.
        """
        self.ui.saveMenuButton.triggered.connect(self.write_to_bag)

    def write_to_bag(self):
        """
        Calls the write dots function in the Writer to write the processed
        lanes into the specified bag file
        """
        self.controller.kill_terminals()
        self.writer.write_lanes(path = self.file_available[0])
        self.quit_program()

    def on_play_click(self):
        """
        Connect the play button to its function
        """
        self.ui.playButton.clicked.connect(self.play_file)

    def on_quit_click(self):
        """
        Connect the quit button in the menu to its function
        """
        self.ui.quitMenuButton.triggered.connect(self.quit_program)

    def set_visual_image(self, image):
        """
        Sets the given image to its corresponding UI element
        """
        self.ui.visualisedVideo.setPixmap(QtGui.QPixmap.fromImage(image))

    def set_lane_image(self, image):
        """
        Sets the given image to its corresponding UI element
        """
        self.ui.processedVideo.setPixmap(QtGui.QPixmap.fromImage(image))

    def set_raw_image(self, image):
        """
        Sets the given image to its corresponding UI element
        """
        self.ui.rawVideo.setPixmap(QtGui.QPixmap.fromImage(image))

    def quit_program(self):
        """
        Closes PyQt in an elegant way, destroys sub-windows
        """
        self.controller.kill_terminals()
        self.close()

    def play_file(self):
        """
        Plays the file, will be updated once the GUI works with other things
        """
        if len(self.file_available) > 0:
            p = Popen(['xdotool', 'search', '--pid', str(self.play_pause_list[0])], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b'Xdotool output')
            p.wait()
            Popen(['xdotool', 'key', '--window', str(output), 'space'])
            if self.state:
                self.ui.playButton.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
                self.state = False
            else:
                self.ui.playButton.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPause))
                self.state = True


class SubWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        """
        Sub-window designed to allow the user to select their source for the neural network
        """
        super(SubWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def run(self):
        self.ui.liveSource.clicked.connect(self.live)
        self.ui.loadBag.clicked.connect(self.bag)

    def live(self):
        self.parent().live = True
        self.close()

    def bag(self):
        """
        Used when a file is selected, asserts whether the item is a bag file or not.
        Sets its parent window value to the file's name
        """
        file_opener = QtGui.QFileDialog
        file = file_opener.getOpenFileName(self, "Please select a bag file", filter="bag(*.bag)")
        assert(str(file).endswith(".bag"))
        self.parent().file_available.append(file)
        self.close()
