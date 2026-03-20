import cv2
import numpy as np
import os

def crop_test_image(image_name, output_name):
    """
    Finds the green bounding box in the test image and crops
    the plate region to provide a 'clean' test sample.
    """
    img_path = os.path.join("screenshots", image_name)
    if not os.path.exists(img_path):
        print(f"File {img_path} not found.")
        return

    img = cv2.imread(img_path)
    
    # 1. Look for 'Green' (0, 255, 0) in the image
    # We use a color range for standard OpenCV Green
    lower_green = np.array([0, 200, 0])
    upper_green = np.array([50, 255, 50])
    
    mask = cv2.inRange(img, lower_green, upper_green)
    
    # 2. Find the bounding box of the green mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest green rectangle (our plate detection)
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        
        # 3. Add padding to show some of the car around it
        # (Crop a much larger area around the plate)
        padding_w = w * 2
        padding_h = h * 5
        
        y1 = max(0, y - padding_h)
        y2 = min(img.shape[0], y + h + padding_h)
        x1 = max(0, x - padding_w)
        x2 = min(img.shape[1], x + w + padding_w)
        
        cropped = img[y1:y2, x1:x2]
        
        # Save output
        out_path = os.path.join("screenshots", output_name)
        cv2.imwrite(out_path, cropped)
        print(f"Successfully cropped {image_name} -> {output_name}")
    else:
        print("Could not find detection box to crop.")

if __name__ == "__main__":
    crop_test_image("anpr_test_1.png", "final_nyabihu_1.png")
    crop_test_image("nyabihu_test_1.png", "final_nyabihu_2.png")
