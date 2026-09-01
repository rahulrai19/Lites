import re
from typing import Tuple

def normalize_whitespace(text: str) -> Tuple[str, bool]:
    """
    Normalizes multiple consecutive horizontal spaces into a single space.
    Does not modify newlines to avoid breaking code blocks or formatting.
    """
    new_text = re.sub(r'[ \t]+', ' ', text)
    return new_text, new_text != text

def normalize_line_endings(text: str) -> Tuple[str, bool]:
    """
    Normalizes Windows/Mac line endings to Unix \n.
    """
    new_text = text.replace('\r\n', '\n').replace('\r', '\n')
    return new_text, new_text != text

def remove_duplicate_sentences(text: str) -> Tuple[str, bool]:
    """
    Safely removes exactly repeated consecutive lines.
    Does not attempt complex NLP deduplication to preserve intent.
    """
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        # Keep empty lines or lines that differ from the previous
        if not new_lines or line.strip() == "" or new_lines[-1].strip() != line.strip():
            new_lines.append(line)
            
    new_text = '\n'.join(new_lines)
    return new_text, new_text != text

def remove_fillers(text: str) -> Tuple[str, bool]:
    """
    Removes common conversational filler phrases ONLY if they appear 
    at the very beginning of the prompt (to ensure safety and preserve intent).
    """
    safe_fillers = [
        r'(?i)^\s*(?:can you|would you|could you)\s+(?:please|kindly)?\s*',
        r'(?i)^\s*(?:please|kindly)\s+',
        r'(?i)^\s*i would like (?:you to )?\s*',
        r'(?i)^\s*i was wondering if you (?:could|can) \s*'
    ]
    
    new_text = text
    for pattern in safe_fillers:
        new_text = re.sub(pattern, '', new_text)
        
    # Capitalize the first letter if we stripped a prefix
    if new_text != text and len(new_text) > 0:
        new_text = new_text[0].upper() + new_text[1:]
        
    return new_text, new_text != text
