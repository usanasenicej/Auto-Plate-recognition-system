import cv2
import csv
import os
import time
from datetime import datetime

import sys
import os

# Add 'src' to system path for easier imports if running from root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import project modules
try:
    from detect import detect_plate
    from align import align_plate
    from ocr import ocr_plate_text
    from validate import validate_plate
    from temporal import TemporalTracker
except ImportError:
    # Fallback if run from project root directly
    from src.detect import detect_plate
    from src.align import align_plate
    from src.ocr import ocr_plate_text
    from src.validate import validate_plate
    from src.temporal import TemporalTracker

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
    # 1. Initialize settings
    cap = cv2.VideoCapture(0) # Default webcam
    tracker = TemporalTracker()
    csv_file = os.path.join("data", "plates.csv")
    screenshot_dir = "screenshots"
    
    # Check if webcam is available, otherwise use simulation mode
    is_webcam = cap.isOpened()
    if not is_webcam:
        print("--- [WARNING]: No webcam detected! Entering Simulation Mode... ---")
        # Load one of the test images as a fallback to show the pipeline works
        fallback_img_path = os.path.join(screenshot_dir, "nyabihu_test_1.png")
        if os.path.exists(fallback_img_path):
            test_frame = cv2.imread(fallback_img_path)
            print(f"--- [SIMULATION]: Using {fallback_img_path} for testing ---")
        else:
            print("--- [ERROR]: Neither webcam nor test images found! ---")
            return
    else:
        print("--- [STARTING ANPR PIPELINE] ---")
    
    print("Press 'q' inside the window to exit.")
    print("Press 's' to manually save a screenshot.")

    while True:
        # 1. Capture/Load frame
        if is_webcam:
            ret, frame = cap.read()
            if not ret: break
        else:
            frame = test_frame.copy()
            # Simulate a small delay in simulation mode
            time.sleep(0.1)

        # 2. Detection (Classical CV)
        plate_cnt = detect_plate(frame)

        if plate_cnt is not None:
            # Visualize detection on the frame (draw rectangle)
            cv2.drawContours(frame, [plate_cnt], -1, (0, 255, 0), 3)

            # 3. Alignment (Perspective Transform)
            aligned_img = align_plate(frame, plate_cnt)
            
            # Show the aligned plate in a separate window (debug)
            cv2.imshow("Aligned Plate (OCR Input)", aligned_img)

            # 4. OCR (Tesseract)
            raw_text = ocr_plate_text(aligned_img)

            # 5. Validation (Regex & Character Analysis)
            valid_text = validate_plate(raw_text)

            if valid_text:
                # 6. Temporal (Confirmation across 3+ frames)
                temp_confirmed = tracker.update(valid_text)

                if temp_confirmed:
                    # 7. Save confirmed plate to CSV
                    save_to_csv(temp_confirmed, csv_file)
                    
                    # Capture screenshot of confirmed detection
                    ss_name = os.path.join(screenshot_dir, f"{temp_confirmed}_{int(time.time())}.jpg")
                    cv2.imwrite(ss_name, frame)
                    print(f"Captured screenshot: {ss_name}")

                # Display the plate text on the main frame
                cv2.putText(frame, valid_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 8. Display main pipeline view
        cv2.imshow("ANPR Pipeline - Webcam View", frame)

        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Manual screenshot
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(os.path.join(screenshot_dir, f"manual_{now_str}.jpg"), frame)
            print("Manual screenshot saved.")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("--- [FINISHED] ---")

if __name__ == "__main__":
    run_pipeline()
