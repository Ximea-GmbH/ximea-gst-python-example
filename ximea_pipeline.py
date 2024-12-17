import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstApp', '1.0')
from gi.repository import Gst, GLib, GstApp
import sys
from ximea_appsrc import XimeaAppSrc


class XimeaPipeline:
    def __init__(self):
        # Initialize GStreamer
        Gst.init(None)

        # Create the Ximea source
        self.ximea = XimeaAppSrc()

        # Set downsampling
        self.ximea.camera.set_downsampling('XI_DWN_4x4')

        # Optimize for latency
        self.ximea.camera.enable_recent_frame()
        
        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline.new('ximea-pipeline')
        
        # Create elements
        self.videoconvert = Gst.ElementFactory.make('videoconvert', 'convert')
        self.videosink = Gst.ElementFactory.make('autovideosink', 'display')
        
        # Check if elements were created successfully
        elements = [self.ximea.appsrc, self.videoconvert, self.videosink]
        for element in elements:
            if not element:
                sys.stderr.write(f'Could not create element: {element.name}\n')
                sys.exit(1)
        
        # Add elements to pipeline
        self.pipeline.add(self.ximea.appsrc)
        self.pipeline.add(self.videoconvert)
        self.pipeline.add(self.videosink)
        
        # Link elements
        self.ximea.appsrc.link(self.videoconvert)
        self.videoconvert.link(self.videosink)
        
        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.on_bus_message)
        
    def start(self):
        """Start the pipeline and camera acquisition"""
        # Start playing
        ret = self.pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            sys.stderr.write('Unable to set the pipeline to the playing state\n')
            sys.exit(1)
            
        # Start camera acquisition
        self.ximea.start_acquisition()
        
        # Start pushing frames
        GLib.timeout_add(33, self.push_frame)  # ~30 fps
        
    def push_frame(self):
        """Push a new frame from the camera to the pipeline"""
        if not self.ximea.next_image():
            return False
        return True
        
    def stop(self):
        """Stop the pipeline and cleanup"""
        self.pipeline.set_state(Gst.State.NULL)
        self.ximea.cleanup()
        
    def on_bus_message(self, bus, message):
        """Handle pipeline messages"""
        t = message.type
        if t == Gst.MessageType.EOS:
            sys.stdout.write('End-of-stream\n')
            self.stop()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            sys.stderr.write(f'Error: {err}: {debug}\n')
            self.stop() 