import os
import cv2
import cvzone
import time
import numpy as np
from ultralytics import YOLO
import torch
import datetime
import pickle
import zlib
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check device with fallback to CPU if CUDA has issues
def get_device():
    if torch.cuda.is_available():
        try:
            # Test CUDA with a simple operation
            torch.zeros(1).cuda()
            return 'cuda'
        except:
            logger.warning("CUDA available but not working, falling back to CPU")
    return 'cpu'

device = get_device()
logger.info(f'Using device: {device}')

class Color:
    """Optimized color management with direct attribute access"""
    def __init__(self):
        self.colors = {
            'boundingBox1': (0, 255, 0),
            'boundingBox2': (0, 255, 255),
            'text1': (255, 255, 255),
            'text2': (0, 0, 0),
            'area1': (255, 0, 0),
            'area2': (0, 0, 255),
            'point': (255, 0, 255),
            'center_point': (255, 255, 0),
            'rectangle': (0, 119, 255),
            'mask': (128, 128, 128)
        }

    def __getattr__(self, item):
        return lambda: self.colors[item]

color = Color()

class Detector:
    """Optimized detector with model warmup and better resource handling"""
    def __init__(self, model_path):
        self.model = YOLO(model_path).to(device)
        
        # Warmup the model
        self._warmup()
        self.model.eval()

    def _warmup(self, iterations=3):
        """Warmup GPU with dummy data"""
        dummy = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        for _ in range(iterations):
            self.model.predict(dummy, verbose=False)

    def detect(self, frame):
        """Optimized detection with better memory handling"""
        try:
            results = self.model.track(
                frame, 
                conf=0.4, 
                classes=[0], 
                persist=True, 
                tracker="bytetrack.yaml",
                verbose=False,
                half=True if device == 'cuda' else False  # Use half precision on GPU
            )

            detections = []
            for r in results:
                boxes = r.boxes
                masks = r.masks if hasattr(r, 'masks') else [None] * len(boxes)
                
                for mask_id, box in enumerate(boxes):
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    box_id = int(box.id.item()) if box.id is not None else -1
                    score = float(box.conf.item()) if box.conf is not None else 0.0
                    class_id = int(box.cls.item()) if box.cls is not None else -1
                    mask = np.array(masks[mask_id].xy, dtype=np.int32) if masks and masks[mask_id] else None
                    
                    detections.append([x1, y1, x2, y2, box_id, class_id, score, mask])
            
            return detections
        
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []

class Algorithm_Count:
    """Optimized counting algorithm with same interface"""
    def __init__(self, file_path, a1, a2, frame_size, coord_point=(0.5, 0.04)):
        self.file_path = file_path
        self.area1 = np.array(a1, np.int32)
        self.area2 = np.array(a2, np.int32)
        self.frame_size = frame_size
        self.coord_point = coord_point
        
        # Initialize detector once
        self.detector = Detector('yolo-Weights\yolo11n.pt')  # Using newer yolov8n
        
        # Tracking dictionaries
        self.peopleEntering = {}
        self.peopleExiting = {}
        self.entering = {}
        self.exiting = {}
        
        # State management
        self.paused = False
        self._running = True
        
        # Performance tracking
        self._fps_buffer = []
        self._last_time = time.time()

    def _calculate_fps(self):
        """Calculate and return current and average FPS"""
        now = time.time()
        current_fps = 1.0 / (now - self._last_time + 1e-6)  # Avoid division by zero
        self._last_time = now
        
        # Update FPS buffer
        self._fps_buffer.append(current_fps)
        if len(self._fps_buffer) > 30:  # Keep last 30 frames for average
            self._fps_buffer.pop(0)
        
        avg_fps = sum(self._fps_buffer) / len(self._fps_buffer) if self._fps_buffer else 0
        return current_fps, avg_fps

    def change_coord_point(self, x1, x2, y1, y2):
        """Optimized coordinate calculation"""
        x, y = self.coord_point
        return int(x1 + (x2 - x1) * x), int(y2 - (y2 - y1) * y)

    def register_movement(self, area_from, area_to, tracker_dict, action_dict, x1, y1, x2, y2, id, frame):
        """Optimized movement tracking with bounds checking"""
        cx, cy = self.change_coord_point(x1, x2, y1, y2)
        
        # Check if in source area
        if cv2.pointPolygonTest(area_from, (cx, cy), False) >= 0:
            if id not in tracker_dict:
                tracker_dict[id] = {'coords': (cx, cy), 'time': time.time()}

        # Check if reached destination area
        if id in tracker_dict and cv2.pointPolygonTest(area_to, (cx, cy), False) >= 0:
            if id not in action_dict:
                action_dict[id] = {
                    'time': datetime.datetime.now().isoformat(),
                    'duration': time.time() - tracker_dict[id]['time'],
                    'face_crops': self._safe_face_crop(x1, y1, x2, y2, frame)
                }

    def _safe_face_crop(self, x1, y1, x2, y2, frame):
        """Safe face crop with boundary checks"""
        try:
            if (0 <= y1 < y2 <= frame.shape[0] and 
                0 <= x1 < x2 <= frame.shape[1]):
                face_crop = frame[y1:y2, x1:x2]
                return zlib.compress(pickle.dumps(face_crop)) if face_crop.size > 0 else None
        except Exception as e:
            logger.warning(f"Face crop error: {e}")
        return None

    def person_bounding_boxes(self, frame, x1, y1, x2, y2, box_id, class_id, score, mask):
        """Optimized bounding box drawing"""
        if box_id != -1:
            cv2.rectangle(frame, (x1, y1), (x2, y2), color.rectangle(), 2)
            cvzone.putTextRect(
                frame, f"{class_id}:{box_id}:{score:.2f}", 
                (x1, y1 - 10), 1, 1, 
                color.text1(), color.text2()
            )
            cx, cy = self.change_coord_point(x1, x2, y1, y2)
            cv2.circle(frame, (cx, cy), 4, color.point(), -1)
            if mask is not None:
                cv2.polylines(frame, [mask], True, color.center_point(), 2)

    def draw_polylines(self, frame):
        """Optimized drawing with FPS display"""
        cv2.polylines(frame, [self.area1], True, color.area1(), 2)
        cv2.polylines(frame, [self.area2], True, color.area2(), 2)
        
        # Get FPS metrics
        current_fps, avg_fps = self._calculate_fps()
        
        # Display counters and FPS info
        cvzone.putTextRect(
            frame, f"Enter: {len(self.entering)}", 
            (20, 30), 1, 1, 
            color.text1(), color.text2()
        )
        cvzone.putTextRect(
            frame, f"FPS: {current_fps:.1f} | Avg: {avg_fps:.1f}", 
            (20, 60), 1, 1, 
            color.text1(), color.text2()
        )

    def counter(self, frame, detections_person):
        """Optimized counter loop"""
        for detect in detections_person:
            x1, y1, x2, y2, box_id, class_id, score, mask = detect
            self.person_bounding_boxes(frame, x1, y1, x2, y2, box_id, class_id, score, mask)
            self.register_movement(
                self.area2, self.area1, 
                self.peopleEntering, self.entering, 
                x1, y1, x2, y2, box_id, frame
            )
            self.register_movement(
                self.area1, self.area2, 
                self.peopleExiting, self.exiting, 
                x1, y1, x2, y2, box_id, frame
            )
        self.draw_polylines(frame)

    def main(self):
        """Main processing loop with same interface"""
        cap = cv2.VideoCapture(self.file_path)
        if not cap.isOpened():
            logger.error(f"Failed to open video: {self.file_path}")
            yield None, None
            return

        try:
            while self._running:
                if not self.paused:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame = cv2.resize(frame, self.frame_size)
                    detections = self.detector.detect(frame)
                    self.counter(frame, detections)
                    
                    result = {
                        'total_people_entering': len(self.entering),
                        'total_people_exiting': len(self.exiting),
                        'entering_details': self.entering,
                        'exiting_details': self.exiting,
                        'frame': frame
                    }
                    yield frame, result
                
                # Allow pause functionality
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self._running = False

        finally:
            cap.release()
            if self._fps_buffer:
                avg_fps = sum(self._fps_buffer)/len(self._fps_buffer)
                min_fps = min(self._fps_buffer)
                max_fps = max(self._fps_buffer)
                logger.info(
                    f"FPS Stats - Avg: {avg_fps:.1f}, Min: {min_fps:.1f}, Max: {max_fps:.1f}, "
                    f"Frames: {len(self._fps_buffer)}"
                )
            else:
                logger.info("No FPS data collected")

if __name__ == '__main__':
    area1 = [(359, 559), (400, 559), (667, 675), (632, 681)]
    area2 = [(346, 563), (313, 566), (579, 703), (624, 694)]
    video_path = os.getenv("VIDEO_PATH", "Sample Test File/test_video.mp4")
    frame_size = (1280, int(1280 / 16 * 9))
    
    counter = Algorithm_Count(video_path, area1, area2, frame_size)
    for frame, result in counter.main():
        if frame is not None:
            cv2.imshow('People Counting', frame)
    
    cv2.destroyAllWindows()