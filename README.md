# Ximea GStreamer Integration

Python application for real-time video streaming from Ximea cameras using GStreamer pipelines.

## Features
- Live video streaming with GStreamer integration
- Configurable camera settings (exposure, downsampling)

## Requirements

### Hardware
- Ximea camera (any model)
- NVIDIA Jetson or other compatible system

### Software
1. XIMEA Software Package (XiAPI)
2. GStreamer and its plugins
3. Python 3.x
4. Required Python packages (see requirements.txt)

## Installation

1. Install the XIMEA Software Package for your platform:
   ```bash
   # Download and install from https://www.ximea.com/support/documents/4
   ```

2. Install system dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
       libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev \
       gir1.2-gstreamer-1.0 gstreamer1.0-tools gstreamer1.0-plugins-base \
       gstreamer1.0-plugins-good
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the viewer application:
```bash
python3 ximea_viewer.py
```

Press Ctrl+C to stop the application.

## Code Structure

- `ximea_viewer.py`: Main application entry point
- `ximea_pipeline.py`: GStreamer pipeline implementation
- `ximea_appsrc.py`: Camera interface and GStreamer source element
- `requirements.txt`: Python package dependencies

## License

This project is licensed under the MIT License - see the LICENSE file for details. 