import cv2
import numpy as np

def detect_plate(frame):
    """
    Detects potential license plate regions in an image frame.
    Returns the contour of the plate if found, otherwise None.
    """
    # 1. Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Noise reduction (Bilateral filter preserves edges)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # 3. Edge detection
    edged = cv2.Canny(gray, 30, 200)

    # 4. Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort by area (descending) and take top 30
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    plate_cnt = None
    for c in contours:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # A license plate is a rectangle (4 corners)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            
            # Typical plate aspect ratio is around 2 to 5
            if 2.0 <= aspect_ratio <= 5.5:
                plate_cnt = approx
                break

    return plate_cnt
