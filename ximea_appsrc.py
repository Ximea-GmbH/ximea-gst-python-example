import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from ximea import xiapi


class XimeaAppSrc:
    def __init__(self):
        # Initialize GStreamer
        Gst.init(None)

        # Initialize Ximea camera
        self.camera = xiapi.Camera()
        self.camera.open_device()

        # Configure camera settings
        self.camera.set_imgdataformat('XI_RGB24')
        self.camera.set_exposure(5000)  # 5ms exposure

        # Create appsrc element
        self.appsrc = Gst.ElementFactory.make('appsrc', 'ximea-source')
        self.configure_appsrc_caps()
        self.appsrc.set_property('format', Gst.Format.TIME)
        self.appsrc.set_property('is-live', True)
        
        # Flag to track acquisition state
        self.is_acquiring = False

    def configure_appsrc_caps(self):
        """Configure the appsrc caps based on current camera settings."""
        # Get current camera parameters
        width = self.camera.get_width()
        height = self.camera.get_height()
        
        # Set new caps on appsrc
        caps = Gst.Caps.from_string(
            f'video/x-raw,format=BGR,width={width},height={height},' +
            'framerate=30/1,bpp=24,depth=24'
        )
        self.appsrc.set_property('caps', caps)
        return width, height

    def start_acquisition(self):
        """Start image acquisition from the camera."""
        if not self.is_acquiring:
            # Start camera acquisition first
            self.camera.start_acquisition()
            self.is_acquiring = True
            
            # Now that acquisition has started, configure caps with actual frame size
            width, height = self.configure_appsrc_caps()
            print(f"Camera acquisition started with frame size: {width}x{height}")

    def stop_acquisition(self):
        """Stop image acquisition from the camera."""
        if self.is_acquiring:
            self.camera.stop_acquisition()
            self.is_acquiring = False

    def next_image(self):
        """Get the next image from the camera and push it to the GStreamer pipeline."""
        if not self.is_acquiring:
            return False
            
        # Get image data from camera
        img = xiapi.Image()
        self.camera.get_image(img)

        # Get raw image data as bytes
        raw_data = img.get_image_data_raw()
        
        # Create GStreamer buffer and push to pipeline
        gst_buffer = Gst.Buffer.new_wrapped(raw_data)
        self.appsrc.emit('push-buffer', gst_buffer)
        return True

    def cleanup(self):
        """Clean up resources and close the camera."""
        if self.is_acquiring:
            self.stop_acquisition()
        if hasattr(self, 'camera'):
            self.camera.close_device()

    def __del__(self):
        """Destructor to ensure proper cleanup."""
        self.cleanup()


