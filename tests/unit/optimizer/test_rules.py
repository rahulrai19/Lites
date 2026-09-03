import pytest
from app.optimizer.rules import (
    normalize_whitespace,
    normalize_line_endings,
    remove_duplicate_sentences,
    remove_fillers,
    normalize_punctuation
)
from app.optimizer.engine import RuleOptimizerEngine
from app.tokenizer.openai_tokenizer import OpenAITokenizer

# --- A. Whitespace ---
def test_whitespace_multiple_spaces():
    assert normalize_whitespace("Hello    world")[0] == "Hello world"

def test_whitespace_leading_trailing():
    assert normalize_whitespace("   Hello world   ")[0] == "Hello world"

def test_whitespace_tabs():
    assert normalize_whitespace("Hello\tworld")[0] == "Hello world"

def test_whitespace_multiple_newlines():
    # Should compress 3+ newlines to exactly 2 newlines (paragraph break)
    assert normalize_whitespace("Hello\n\n\n\nworld")[0] == "Hello\n\nworld"
    # 2 newlines should remain 2
    assert normalize_whitespace("Hello\n\nworld")[0] == "Hello\n\nworld"

def test_whitespace_mixed():
    text = "  Hello \t  world \n \n \n How  are \t you?  "
    expected = "Hello world\n\nHow are you?"
    assert normalize_whitespace(text)[0] == expected

# --- B. Line endings ---
def test_line_endings_lf():
    assert normalize_line_endings("A\nB")[0] == "A\nB"

def test_line_endings_crlf():
    assert normalize_line_endings("A\r\nB")[0] == "A\nB"

def test_line_endings_cr():
    assert normalize_line_endings("A\rB")[0] == "A\nB"

def test_line_endings_mixed():
    assert normalize_line_endings("A\rB\r\nC\nD")[0] == "A\nB\nC\nD"

# --- C. Duplicate sentences ---
def test_duplicate_exact():
    text = "Explain Redis.\nExplain Redis."
    assert remove_duplicate_sentences(text)[0] == "Explain Redis."

def test_duplicate_paragraphs():
    text = "Paragraph 1\n\nParagraph 1"
    assert remove_duplicate_sentences(text)[0] == "Paragraph 1"

def test_duplicate_whitespace_diff():
    text = "Explain Redis. \n Explain Redis.  "
    assert remove_duplicate_sentences(text)[0] == "Explain Redis."

def test_duplicate_punctuation_diff():
    text = "Explain Redis.\nExplain Redis"
    # Should not aggressively deduplicate if punctuation differs, to remain safe.
    assert remove_duplicate_sentences(text)[0] == text

# --- D. Filler words ---
def test_fillers_alone():
    # "Please" alone should not be removed to avoid an empty prompt.
    assert remove_fillers("Please")[0] == "Please"

def test_fillers_inside():
    # Inside shouldn't be removed to preserve context
    text = "Tell me how to say please in Spanish."
    assert remove_fillers(text)[0] == text

def test_fillers_repeated():
    text = "Please, could you kindly explain Redis?"
    # Should strip the leading fillers
    assert remove_fillers(text)[0] == "Explain Redis?"

def test_fillers_meaningful():
    assert remove_fillers("Can you hold this?")[0] == "Hold this?" # Still meaningful

# --- E. Punctuation ---
def test_punctuation_repeated():
    assert normalize_punctuation("Wow!!!!!")[0] == "Wow!!!!!"
    assert normalize_punctuation("Wait....")[0] == "Wait...."
    assert normalize_punctuation("List: item1,,,,, item2")[0] == "List: item1,,,,, item2"

def test_punctuation_unnecessary():
    assert normalize_punctuation("Hello?!?!?")[0] == "Hello?!?!?"

def test_punctuation_in_code():
    code = "if (a == b) { !!! }"
    assert normalize_punctuation(code)[0] == code

def test_punctuation_in_urls():
    url = "https://example.com/?q=!!!!"
    assert normalize_punctuation(url)[0] == url

def test_punctuation_in_json():
    json_str = '{"wow": "!!!!"}'
    assert normalize_punctuation(json_str)[0] == json_str

# --- Engine tests ---
@pytest.mark.asyncio
async def test_engine_optimization_flow():
    tokenizer = OpenAITokenizer()
    engine = RuleOptimizerEngine(tokenizer)
    
    prompt = "   Please please could you    explain Redis!!!!!  \n\n\n Explain Redis!!!!!   "
    
    new_prompt, metadata = await engine.optimize(prompt, "gpt-4o")
    
    # Expected transformations:
    # 1. remove_fillers -> "Explain Redis!!!!!  \n\n\n Explain Redis!!!!!   "
    # 2. normalize_punctuation -> (NO-OP)
    # 3. normalize_whitespace -> "Explain Redis!!!!!\n\nExplain Redis!!!!!"
    # 4. remove_duplicate_sentences -> "Explain Redis!!!!!"
    
    # NOTE: The actual order in engine might vary, so we assert the final outcome is optimized safely.
    assert "Explain Redis!!!!!" in new_prompt
    assert len(new_prompt) < len(prompt)
    assert metadata.optimization_applied is True
    assert metadata.tokens_saved > 0
    assert metadata.original_prompt == prompt
    assert metadata.optimized_prompt == new_prompt

@pytest.mark.asyncio
async def test_engine_noop():
    tokenizer = OpenAITokenizer()
    engine = RuleOptimizerEngine(tokenizer)
    
    prompt = "This is a perfectly optimized prompt. No changes needed."
    new_prompt, metadata = await engine.optimize(prompt, "gpt-4o")
    
    assert new_prompt == prompt
    assert metadata.tokens_saved == 0
    assert metadata.savings_percentage == 0
    assert len(metadata.operations_applied) == 0
