import gi

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

class Camera():
    def __init__(self, name, index, host, port):
        Gst.init(None)
        self.index = str(index)
        self.name = name
        _pipeline = "v4l2src device=/dev/video" + self.index + " ! video/x-raw,width=640,height=480,framerate=30/1 ! " \
                  + "jpegenc ! rtpjpegpay ! udpsink host=" + str(host) + " port=" + str(port)
        self.pipeline = Gst.parse_launch(_pipeline)
        self.start()

    def start(self):
        try:
            ret = self.pipeline.set_state(Gst.State.PLAYING)
            if ret == Gst.StateChangeReturn.FAILURE:
                raise Exception("Error starting the pipeline")
            self.running = True
            print(self.name + " of index " + self.index + " started")
        except :
            print(self.name + " index " + self.index + " is not Connected")
            self.running = False
            return

    def pause(self):
        self.pipeline.set_state(Gst.State.PAUSED)
        self.running = False
        print(self.name + " of index " + self.index + " paused")
    
    def close(self):
        self.running = False
        self.pipeline.set_state(Gst.State.NULL)
        print(self.name + " of index " + self.index + " stopped")

    def is_running(self):
        return self.running

    def info(self):
        return self.name, self.index