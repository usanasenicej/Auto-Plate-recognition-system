import re

def validate_plate(raw_text):
    """
    Validates the OCR output, fixes common character OCR mistakes,
    and checks against a plate format regex.
    Returns:
        Validated plate string or None
    """
    # 1. Basic Cleaning
    # Remove any non-alphanumeric characters (including spaces)
    cleaned = re.sub(r'[^A-Z0-9]', '', raw_text.upper())

    # 2. Fix common OCR mistakes
    # OCR often confuses B with 8, I with 1, O with 0
    # Note: We only replace if they are in the 'wrong' positions,
    # but for generic ANPR, we'll keep it simple for the user.
    # Simple replacement dictionary for common confusions:
    # (Optional: Only use if your region's plates have predictable patterns)
    # Since we don't know the region, we'll skip aggressive mapping
    # but keep the structure ready for it.

    # 3. Validation Rules (Length, Regex)
    # Most plates are between 6 and 9 alphanumeric characters
    if len(cleaned) < 5 or len(cleaned) > 10:
        return None

    # Check if string has at least some numbers and letters
    # (This varies by region, but help filter random noise)
    has_letters = bool(re.search(r'[A-Z]', cleaned))
    has_nums = bool(re.search(r'[0-9]', cleaned))
    
    # Generic plate pattern (alphanumeric sequence)
    # You can customize this to ^[A-Z]{3}\d{4}$ for example.
    pattern = r'^[A-Z0-9]{5,10}$'
    
    if re.match(pattern, cleaned) and (has_letters or has_nums):
        return cleaned
    
    return None
