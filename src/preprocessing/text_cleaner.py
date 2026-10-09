import re

def clean_text(text: str) -> str:
    """
    Prepares text for machine-learning text classification by performing:
    - lowercase conversion
    - URL removal
    - HTML tag removal
    - removal of unnecessary special characters (retaining alphanumeric and apostrophes for negation)
    - whitespace normalization
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase conversion
    text = text.lower()
    
    # 2. URL removal
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # 3. HTML tag removal
    text = re.sub(r'<.*?>', '', text)
    
    # 4. Removal of unnecessary special characters
    # Retain a-z, 0-9, whitespace, and apostrophes (to keep words like "don't" or "can't")
    text = re.sub(r"[^a-z0-9\s']", ' ', text)
    
    # 5. Remove standalone apostrophes or obvious noise (optional, keeping basic here)
    text = re.sub(r" '+ ", ' ', text)
    text = re.sub(r" +' ", ' ', text)
    
    # 6. Whitespace normalization
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
