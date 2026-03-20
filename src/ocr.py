import cv2
import pytesseract

def ocr_plate_text(aligned_plate):
    """
    Extracts text from the aligned plate image using Tesseract OCR.
    Input:
        aligned_plate: Straightened grayscale image
    Returns:
        Extracted raw string
    """
    # 1. Resize for better OCR (increase size)
    resized = cv2.resize(aligned_plate, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

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
