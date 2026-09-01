import pytest
from app.models.context import ContextProfile
from app.optimizer.engine import RuleOptimizerEngine
from app.tokenizer.openai_tokenizer import OpenAITokenizer

@pytest.mark.asyncio
async def test_context_code_skips_whitespace():
    tokenizer = OpenAITokenizer()
    engine = RuleOptimizerEngine(tokenizer)
    
    # Python code with significant whitespace
    code_prompt = "def hello():\n    print('Hello')\n    print('World')"
    
    # Using CODE context should preserve the whitespace exactly
    new_prompt, metadata = await engine.optimize(code_prompt, context=ContextProfile.CODE)
    
    assert new_prompt == code_prompt
    assert "normalize_whitespace" not in metadata.operations_applied

@pytest.mark.asyncio
async def test_context_legal_skips_fillers():
    tokenizer = OpenAITokenizer()
    engine = RuleOptimizerEngine(tokenizer)
    
    legal_prompt = "Please kindly execute the aforementioned agreement."
    
    # Using LEGAL context should preserve the exact phrasing, meaning 'Please kindly' shouldn't be stripped
    new_prompt, metadata = await engine.optimize(legal_prompt, context=ContextProfile.LEGAL)
    
    assert new_prompt == legal_prompt
    assert "remove_fillers" not in metadata.operations_applied

@pytest.mark.asyncio
async def test_context_chat_applies_all():
    tokenizer = OpenAITokenizer()
    engine = RuleOptimizerEngine(tokenizer)
    
    chat_prompt = "Can you please    explain this to me?\nCan you please    explain this to me?"
    
    new_prompt, metadata = await engine.optimize(chat_prompt, context=ContextProfile.CHAT)
    
    assert new_prompt == "Explain this to me?"
    assert "normalize_whitespace" in metadata.operations_applied
    assert "remove_duplicate_sentences" in metadata.operations_applied
    assert "remove_fillers" in metadata.operations_applied
