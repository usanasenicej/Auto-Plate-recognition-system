import cv2
import pytesseract
import shutil
from config import TESSERACT_CONFIG, OCR_RESIZE_FACTOR

def check_tesseract():
    """Checks if Tesseract is installed and reachable."""
    if shutil.which("tesseract") is None:
        # If not in path, you can set it manually here for the user
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        return False
    return True

def ocr_plate_text(aligned_plate):
    """
    Extracts text from the aligned plate image using Tesseract OCR.
    Input:
        aligned_plate: Straightened grayscale image
    Returns:
        Extracted raw string
    """
    if not check_tesseract():
        return "TESSERACT_NOT_FOUND"

    # 1. Resize for better OCR (increase size)
    resized = cv2.resize(aligned_plate, None, fx=OCR_RESIZE_FACTOR, fy=OCR_RESIZE_FACTOR, interpolation=cv2.INTER_CUBIC)

    # 2. Denoising
    denoised = cv2.GaussianBlur(resized, (5, 5), 0)

    # 3. Thresholding (Otsu's binarization)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 4. Tesseract configuration
    # --psm 7: Treat as single line of text
    # --oem 3: Default OCR Engine (LSTM)
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    # Extracted text
    text = pytesseract.image_to_string(thresh, config=custom_config)

    # Basic cleanup (whitespace, newline)
    return text.strip()
