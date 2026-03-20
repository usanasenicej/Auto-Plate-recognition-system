import cv2
import csv
import os
import time
from datetime import datetime
import sys

# Add 'src' to system path for easier imports if running from root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import project config & modules
from config import *
from detect import detect_plate
from align import align_plate
from ocr import ocr_plate_text
from validate import validate_plate
from temporal import TemporalTracker
from utils import draw_plate_overlay

def save_to_csv(plate_text, csv_path):
    """Saves the detected plate and timestamp to plates.csv."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, plate_text])
        print(f"--- [SAVED]: {plate_text} at {timestamp} ---")

def run_pipeline():
    """
    Main ANPR Pipeline:
    Camera (or Static Image Fallback) -> Detection -> Alignment -> OCR -> Validation -> Temporal -> Save
    """
    # 1. Initialize settings from Config
    cap = cv2.VideoCapture(CAMERA_INDEX)
    tracker = TemporalTracker(confidence_threshold=CONFIDENCE_THRESHOLD, timeout_seconds=TIMEOUT_SECONDS)
    csv_file = DATA_CSV_PATH
    screenshot_dir = SCREENSHOT_DIR
    
    # 2. Robust camera check (Simulation mode fallback)
    is_webcam = cap.isOpened()
    if not is_webcam:
        print("--- [WARNING]: No webcam detected! Entering Simulation Mode... ---")
        fallback_img_path = os.path.join(screenshot_dir, "nyabihu_test_1.png")
        if os.path.exists(fallback_img_path):
            test_frame = cv2.imread(fallback_img_path)
            print(f"--- [SIMULATION]: Using {fallback_img_path} for testing ---")
        else:
            print("--- [ERROR]: Neither webcam nor test images found! Check screenshots/ folder ---")
            return
    else:
        print("--- [STARTING ANPR PIPELINE] ---")
    
    print("Press 'q' inside the window to exit.")
    print("Press 's' to manually save a screenshot.")

    while True:
        # 3. Capture/Load frame
        if is_webcam:
            ret, frame = cap.read()
            if not ret: break
        else:
            frame = test_frame.copy()
            time.sleep(0.1)

        # 4. Detection (Morphological Enhanced)
        plate_cnt = detect_plate(frame)

        if plate_cnt is not None:
            # 5. Alignment (Perspective Transform)
            aligned_img = align_plate(frame, plate_cnt)
            cv2.imshow("Aligned Plate (OCR Input)", aligned_img)

            # 6. OCR (Tess Engine)
            raw_text = ocr_plate_text(aligned_img)

            # 7. Validation (Regex + Length)
            valid_text = validate_plate(raw_text)

            if valid_text:
                # 8. Visual Overlay (Using Utils)
                x, y, w, h = cv2.boundingRect(plate_cnt)
                frame = draw_plate_overlay(frame, valid_text, x, y, w, h)

                # 9. Temporal Tracking (Counter Check)
                temp_confirmed = tracker.update(valid_text)

                if temp_confirmed:
                    # 10. Save step (CSV + Logging)
                    save_to_csv(temp_confirmed, csv_file)
                    ss_name = os.path.join(screenshot_dir, f"confirmed_{temp_confirmed}_{int(time.time())}.jpg")
                    cv2.imwrite(ss_name, frame)

        # 11. Final display window
        cv2.imshow("ANPR Pipeline - Webcam View", frame)

        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(os.path.join(screenshot_dir, f"manual_{now_str}.jpg"), frame)
            print("Manual screenshot saved.")

    # Cleanup resources
    cap.release()
    cv2.destroyAllWindows()
    print("--- [EXITED ANPR PIPELINE] ---")

if __name__ == "__main__":
    run_pipeline()
