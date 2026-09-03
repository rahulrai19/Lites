import re
from typing import Tuple

def normalize_whitespace(text: str) -> Tuple[str, bool]:
    """
    Normalizes multiple consecutive horizontal spaces into a single space.
    Compresses multiple newlines to a maximum of two (paragraph break).
    Strips leading and trailing whitespace.
    """
    # 1. Replace tabs with spaces
    new_text = text.replace('\t', ' ')
    # 2. Trim trailing/leading spaces on every line so that empty lines become truly empty
    new_text = re.sub(r'^[ ]+|[ ]+$', '', new_text, flags=re.MULTILINE)
    # 3. Collapse multiple spaces into one
    new_text = re.sub(r'[ ]{2,}', ' ', new_text)
    # 4. Collapse 3+ newlines into 2
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)
    # 5. Global strip
    new_text = new_text.strip()
    
    return new_text, new_text != text

def normalize_line_endings(text: str) -> Tuple[str, bool]:
    """
    Normalizes Windows/Mac line endings to Unix \n.
    """
    new_text = text.replace('\r\n', '\n').replace('\r', '\n')
    return new_text, new_text != text

def remove_duplicate_sentences(text: str) -> Tuple[str, bool]:
    """
    Safely removes exactly repeated consecutive lines or paragraphs.
    Ignores empty lines when finding consecutive matches.
    """
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        if line.strip() == "":
            new_lines.append(line)
            continue
            
        # Find the last non-empty line to compare against
        last_non_empty = None
        for prev in reversed(new_lines):
            if prev.strip() != "":
                last_non_empty = prev
                break
                
        if last_non_empty is None or last_non_empty.strip() != line.strip():
            new_lines.append(line)
            
    new_text = '\n'.join(new_lines).strip()
    return new_text, new_text != text

def remove_fillers(text: str) -> Tuple[str, bool]:
    """
    Removes common conversational filler phrases ONLY if they appear 
    at the very beginning of the prompt (to ensure safety and preserve intent).
    """
    safe_fillers = [
        r'(?i)^\s*(?:can you|could you|would you|will you)\s+(?:please|kindly)?\s*',
        r'(?i)^\s*(?:please|kindly)\s*,?\s*',
        r'(?i)^\s*i would like (?:you to )?\s*',
        r'(?i)^\s*i was wondering if you (?:could|can) \s*'
    ]
    
    original_text = text
    
    # Keep stripping fillers from the start until no more match
    while True:
        matched_any = False
        for pattern in safe_fillers:
            new_text = re.sub(pattern, '', text)
            if new_text != text:
                text = new_text
                matched_any = True
        if not matched_any:
            break
            
    # Safety: If stripping fillers removes EVERYTHING (e.g. prompt was literally just "Please"), revert.
    if len(text.strip()) == 0:
        return original_text, False
        
    # Capitalize the first letter if we stripped a prefix
    if text != original_text and len(text) > 0:
        text = text[0].upper() + text[1:]
        
    return text, text != original_text

def normalize_punctuation(text: str) -> Tuple[str, bool]:
    """
    Safely normalizes excessive punctuation.
    Because detecting JSON and Code without markdown backticks is extremely error-prone,
    and changing meaning violates the core safety rule, this rule acts as a safe NO-OP.
    """
    return text, False
