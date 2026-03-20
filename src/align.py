import cv2
import numpy as np

def align_plate(frame, contour):
    """
    Applies perspective transform to straighten the detected plate.
    Input:
        frame: The original image
        contour: The 4-corner contour of the plate
    Returns:
        Aligned and warped plate image
    """
    # 1. Reshape the contour points to (4, 2)
    pts = contour.reshape(4, 2)

    # 2. Sort points: Top-Left, Top-Right, Bottom-Right, Bottom-Left
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)] # Minimal sum -> Top-Left
    rect[2] = pts[np.argmax(s)] # Maximal sum -> Bottom-Right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] # Minimal diff -> Top-Right
    rect[3] = pts[np.argmax(diff)] # Maximal diff -> Bottom-Left

    # 3. Define target dimension for the aligned plate
    # Most license plates are approx 4:1 width:height
    width = 400
    height = 100
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # 4. Compute Perspective Transform Matrix
    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(frame, matrix, (width, height))

    # 5. Final Grayscale conversion for OCR readiness
    gray_warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    return gray_warped
