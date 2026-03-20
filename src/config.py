# ANPR Configuration Parameters

# 🎥 Camera & Simulation
CAMERA_INDEX = 0
SCREENSHOT_DIR = "screenshots"
DATA_CSV_PATH = "data/plates.csv"

# 🛡️ Detection Settings
# Aspect ratio for standard license plates (Width / Height)
PLATE_ASPECT_RATIO_RANGE = (2.0, 5.5)
MIN_PLATE_AREA = 500
MAX_PLATE_AREA = 100000

# 📏 Alignment Settings
ALIGNED_PLATE_WIDTH = 400
ALIGNED_PLATE_HEIGHT = 100

# 📝 OCR Settings
TESSERACT_CONFIG = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
OCR_RESIZE_FACTOR = 2.5

# ⏱️ Temporal Tracking
CONFIDENCE_THRESHOLD = 3
TIMEOUT_SECONDS = 5
