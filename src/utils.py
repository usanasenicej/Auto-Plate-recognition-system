import cv2

def draw_plate_overlay(frame, plate_text, x, y, w, h):
    """
    Draws a green bounding box around the plate and places
    a high-visibility label at the top.
    """
    # 1. Draw Green Rectangle
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # 2. Add Label with Background for better visibility
    label = f"PLATE: {plate_text}"
    (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    
    # Position label above the box if there's enough space, otherwise inside
    label_y = max(y, label_height + 10)
    
    # Draw Background Rectangle (Blue)
    cv2.rectangle(frame, (x, label_y - label_height - 10), (x + label_width + 10, label_y), (255, 0, 0), -1)
    
    # Put text onto background (White)
    cv2.putText(frame, label, (x + 5, label_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    return frame
