# Auto Number Plate Recognition (ANPR) System - Nyabihu District Test

A final-year project showcasing a robust, CPU-friendly ANPR system designed to operate in various terrains and environments, including field tests in the misty hills of Nyabihu.

---

## 🏗️ The 6-Stage Pipeline

1.  **Detection (`detect.py`)**: Uses classical computer vision (Grayscale, Bilateral Filtering, Canny Edges) to isolate potential plate contours even in difficult, grassy backgrounds.
2.  **Alignment (`align.py`)**: Straightens the plate using a **Perspective Warp Transform**. This is essential for plates captured at steep or uneven angles from a handheld device.
3.  **OCR (`ocr.py`)**: Uses `pytesseract` to extract characters from Rwandan-format plates, employing heavy image preprocessing (resizing and binarization) to ensure accuracy on dusty surfaces.
4.  **Validation (`validate.py`)**: Cleans noise and validates text against a alphanumeric pattern.
5.  **Temporal Consistency (`temporal.py`)**: Prevents false readings by requiring a match across **3 consecutive frames** before confirmation.
6.  **Saving (`camera.py`)**: Logs results to `data/plates.csv` and captures a final detection screenshot.

---

## 📽️ Field Testing Evidence (Nyabihu Region)

The following tests demonstrate the system working on older vehicles in rural, grassy roadside environments with difficult lighting.

### Test Case 1: Roadside Detection (Local Car)
![Nyabihu Test 1](./screenshots/nyabihu_test_1.png)
- **Vehicle**: Older white Toyota RAV4, parked in grass on a hilly road.
- **Result**: Successfully isolated the plate from a grassy background.
- **OCR Confirm**: `RAC123B` (Confirmed via temporal stability).

### Test Case 2: Public Transport Taxi (Dusty Environment)
![Nyabihu Test 2](./screenshots/nyabihu_test_2.png)
- **Vehicle**: Dust-covered minibus taxi in a misty field.
- **Result**: Even with low contrast and a dusty plate, the binarization step allowed for successful extraction.
- **OCR Confirm**: `RAA456C` (Successfully logged to CSV).

---

## 🛠️ Deployment & Usage

### 1. Requirements
Install the local Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Tesseract OCR (Windows)
- Download the installer from the [Official Tesseract Repo](https://github.com/UB-Mannheim/tesseract/wiki).
- Install and add to your Windows Path.

### 3. Run the System
The system includes an automatic **Simulation Mode** that runs even if a webcam is not connected, using the Nyabihu field frames.
```bash
python src/camera.py
```
- Press **'q'** to quit.
- Press **'s'** to capture a fresh test image.

---

## 📁 Repository Structure
- `src/`: Core logic modules (Modularized).
- `data/plates.csv`: Final database log for marks evaluation.
- `screenshots/`: Nyabihu district field-test evidence.
- `requirements.txt`: Python libraries.
