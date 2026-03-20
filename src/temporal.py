import time
from datetime import datetime

class TemporalTracker:
    """
    Keeps track of detected plates over time to ensure consistency.
    Only 'confirms' a plate if seen multiple times.
    """
    def __init__(self, confidence_threshold=3, timeout_seconds=5):
        self.tracking_dict = {} # {plate_text: {"count": 1, "last_seen": timestamp}}
        self.confirmed_plates = set() # Set for session-level uniqueness
        self.confidence_threshold = confidence_threshold
        self.timeout_seconds = timeout_seconds

    def update(self, plate_text):
        """
        Updates tracking dictionary with a new detection.
        Returns the plate_text if it crosses the 'confirmed' threshold, otherwise None.
        """
        now = time.time()
        
        # 1. Age out old records (plates that haven't been seen in 5+ seconds)
        expired_keys = [k for k, v in self.tracking_dict.items() if (now - v["last_seen"]) > self.timeout_seconds]
        for key in expired_keys:
            del self.tracking_dict[key]

        # 2. Add or update current detection
        if plate_text in self.tracking_dict:
            self.tracking_dict[plate_text]["count"] += 1
            self.tracking_dict[plate_text]["last_seen"] = now
        else:
            self.tracking_dict[plate_text] = {"count": 1, "last_seen": now}

        # 3. Check if confirmed (hit threshold)
        if self.tracking_dict[plate_text]["count"] >= self.confidence_threshold:
            # Check if we've already saved this recently to prevent duplicate logging
            if plate_text not in self.confirmed_plates:
                self.confirmed_plates.add(plate_text)
                return plate_text
        
        return None

    def reset_confirmed(self):
        """Clears session-level unique plates if needed."""
        self.confirmed_plates.clear()
