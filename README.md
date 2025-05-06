# Visitor-Monitoring-System
A computer vision-based visitor monitoring system with face detection, tracking, and recognition capabilities.

### Overview
The Visitor Monitoring System is designed to monitor and track visitors through video camera feeds. It uses computer vision algorithms to detect and track faces, count entries/exits, and maintain a database of visitor records.

### Features
###### Camera Feed

- Real-time video processing
- Face detection and tracking
- Entry/exit counting through defined zones
- Video recording and export

### Face Capture (without recognition)
###### Face capture and storage

- Similarity comparison between faces
- Historical face matching
- Database Integration
- Automatic logging of visitors
- Date and time tracking
- Searchable logs with filtering options

### Database Integration
###### Automatic logging of visitors

- Date and time tracking
- Searchable logs with filtering options
- User Interface
- Modern sidebar navigation
- Dashboard with statistics
- Log viewing and searching
- Export capabilities
- Settings configuration

### Components
###### Main WindowMain Window [`CameraFeedWindow`]
- Image comparison functionality
- Face matching against existing database
- Visual comparison display

###### Popup Window [`PopupWindow`]
- Image comparison functionality
- Face matching against existing database
- Visual comparison display

###### Backend Processing
- Face detection algorithms
- Entry/exit counting logic
- Database management
- Image representation and comparison

### Usage
###### Camera Feed
1. Navigate to the Camera tab
2. Define entry/exit zones when prompted
3. Click Start to begin monitoring
4. Faces will be automatically detected and tracked
5. Click Stop to end the session and save recordings

###### Log Viewing
1. Navigate to the Logs tab
2. View all visitor entries in the table
3. Use the search box to filter entries
4. Right-click on an entry to search for similar faces

###### Settings
1. Navigate to the Settings tab
2. Adjust coordinate settings for the monitoring zones
3. Save configurations or restore defaults

###### Export
1. Navigate to the Export tab
2. Select the date to filter logs
3. Click Export to save as PDF

### Technical Implementation
The system uses multi-threading to handle camera feed processing without blocking the UI. Face crops are saved automatically and can be compared against historical data using facial recognition algorithms.

Database interactions are handled through a MySQL manager, which maintains logs of all visitor entries with timestamps and face images.

### Dependencies
###### Base Dependencies
- matplotlib (≥3.3.0) - Plotting library
- numpy (≥1.22.2) - Numerical computations
- opencv-python (≥4.6.0) - Computer vision
- pillow (≥7.1.2) - Image processing
- pyyaml (≥5.3.1) - YAML parsing and serialization
- requests (≥2.23.0) - HTTP requests
- scipy (≥1.4.1) - Scientific computations
- tqdm (≥4.64.0) - Progress bar utility

###### Plotting Dependencies
- pandas (≥1.1.4) - Data manipulation and analysis
- seaborn (≥0.11.0) - Statistical data visualization

###### System Utilities
- psutil - System utilization monitoring
- py-cpuinfo - CPU information display
- thop (≥0.1.1) - FLOPs computation

###### Human Tracking Dependencies
- cvzone - Computer vision utilities
- ultralytics - YOLO-based object detection
- deepface - Facial recognition and analysis
- retinaface - Face detection

###### UI and Database
- PyQt6 - GUI framework
- PySide6 - Alternative GUI framework
- pymysql - MySQL database connector

###### GPU Acceleration
- cuda-python (≥12.3.0) - CUDA Python for GPU acceleration
- torchaudio (>=2.5.0.dev20241002+cu124) - CUDA Python for GPU acceleration