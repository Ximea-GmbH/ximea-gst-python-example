import signal
import sys
from gi.repository import GLib
from ximea_pipeline import XimeaPipeline


def main():
    """Main function to run the Ximea camera viewer."""
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    # Create and start pipeline
    pipeline = XimeaPipeline()
    pipeline.start()
    
    # Run GLib main loop
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.stop()


if __name__ == '__main__':
    main() 