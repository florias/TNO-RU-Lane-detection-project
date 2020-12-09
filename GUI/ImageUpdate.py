from PyQt4 import QtCore
import cv2
import qimage2ndarray


class ImageUpdate(QtCore.QThread):

    image_signal = QtCore.pyqtSignal(object)

    def __init__(self, images_ready, queue, raw_or_lane, parent=None):
        """
        Creates the image updater thread and sets it up ready to be ran.   
        Args:
            images_ready: a python multiprocessing Event that will control
                when an image is ready to be updated.
            queue: a python multiprocessing Queue that allows the transfer 
                of images between threads.
            raw_or_lane: Bool that is True if this instance of the class is
                responsible for updating the raw or lane images, else False.
        """
        super(ImageUpdate, self).__init__(parent)
        self.image_lock = images_ready
        self.queue = queue
        self.raw_or_lane = raw_or_lane

    def run(self):
        """Always be checking and waiting for the next image to update"""
        while True:
            self.update_image()

    def update_image(self):
        """
        Waits for an image, when an image is set it converts it to a 
        qimage and sends it to be visualised. 
        Additionally if the image is a raw image from the bag or a
        post-lane-detection image then it is converted from BGR to RGB.
        """
        self.image_lock.wait()
        self.image_lock.clear()
        data = self.queue.get()
        if self.raw_or_lane:
            data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(data)
        self.image_signal.emit(image)