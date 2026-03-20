import cv2
import numpy as np
from config import PLATE_ASPECT_RATIO_RANGE, MIN_PLATE_AREA, MAX_PLATE_AREA

def detect_plate(frame):
    """
    Detects potential license plate regions in a complex environment (e.g. grass).
    Uses morphological operations to clean up background noise.
    """
    # 1. Grayscale and Bilateral Filtering
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # 2. Add Morphological Opening to remove small noise (like grass blades)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)

    # 3. Edge detection
    edged = cv2.Canny(morph, 30, 200)

    # 4. Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort by area (descending) and take top 30
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    plate_cnt = None
    for c in contours:
        area = cv2.contourArea(c)
        if area < MIN_PLATE_AREA or area > MAX_PLATE_AREA:
            continue

        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # A license plate is a rectangle (4 corners)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            
            # Use configured aspect ratio range
            min_ar, max_ar = PLATE_ASPECT_RATIO_RANGE
            if min_ar <= aspect_ratio <= max_ar:
                plate_cnt = approx
                break

    return plate_cnt
