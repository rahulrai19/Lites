import pytest
from app.core.context_manager import ConversationContextManager
from app.api.models import ChatMessage
from app.tokenizer.openai_tokenizer import OpenAITokenizer

@pytest.fixture
def manager():
    tokenizer = OpenAITokenizer()
    return ConversationContextManager(tokenizer)

@pytest.fixture
def model():
    return "gpt-4o"

@pytest.mark.asyncio
async def test_empty_conversation(manager, model):
    result = await manager.process([], model)
    assert result == ""

@pytest.mark.asyncio
async def test_single_message(manager, model):
    messages = [ChatMessage(role="user", content="Hello")]
    result = await manager.process(messages, model)
    assert result == "Hello"

@pytest.mark.asyncio
async def test_multiple_messages_within_limits(manager, model):
    messages = [
        ChatMessage(role="system", content="You are a bot."),
        ChatMessage(role="user", content="Hi"),
        ChatMessage(role="assistant", content="Hello!"),
        ChatMessage(role="user", content="How are you?")
    ]
    result = await manager.process(messages, model, max_messages=10)
    assert "You are a bot." in result
    assert "Hi" in result
    assert "Hello!" in result
    assert "How are you?" in result

@pytest.mark.asyncio
async def test_message_limit_exceeded(manager, model):
    # Create 5 messages
    messages = [
        ChatMessage(role="system", content="SYS"), # Index 0
        ChatMessage(role="user", content="MSG1"),  # Index 1
        ChatMessage(role="assistant", content="MSG2"), # Index 2
        ChatMessage(role="user", content="MSG3"),  # Index 3
        ChatMessage(role="assistant", content="MSG4")  # Index 4
    ]
    
    # We set max_messages = 3. 
    # Logic: 
    # Lock in 0 (SYS). Total=1
    # Lock in 4 (MSG4). Total=2
    # Slide back: i=3. Total=3 -> Add 3.
    # Slide back: i=2. Total=4 -> Exceeds max_messages(3). Break.
    
    result = await manager.process(messages, model, max_messages=3)
    
    # Assert SYS (0), MSG3 (3), and MSG4 (4) are kept.
    assert "SYS" in result
    assert "MSG4" in result
    assert "MSG3" in result
    assert "MSG2" not in result
    assert "MSG1" not in result

@pytest.mark.asyncio
async def test_token_limit_exceeded(manager, model):
    messages = [
        ChatMessage(role="system", content="SYS"), # System
        ChatMessage(role="user", content="Very long text to exceed the limit. " * 50), # Old user
        ChatMessage(role="assistant", content="Response that definitely pushes token count past the 20 token limit constraint we set."), # Old assistant
        ChatMessage(role="user", content="Final question.") # Latest request
    ]
    
    # We set max_tokens very low (e.g. 20 tokens)
    # The SYS and Final question alone will take ~10 tokens.
    # The long response will push it over 20.
    result = await manager.process(messages, model, max_tokens=20, max_messages=10)
    
    assert "SYS" in result
    assert "Final question." in result
    assert "Response that definitely pushes" not in result
    assert "Very long text" not in result

@pytest.mark.asyncio
async def test_both_limits_exceeded(manager, model):
    messages = [ChatMessage(role="user", content=f"M{i}") for i in range(10)]
    messages.insert(0, ChatMessage(role="system", content="SYS"))
    
    # Extremely low token and message limits
    result = await manager.process(messages, model, max_tokens=10, max_messages=2)
    
    assert "SYS" in result
    assert "M9" in result
    # M8 won't fit token or message budget
    assert "M8" not in result

@pytest.mark.asyncio
async def test_boundary_message_limit(manager, model):
    # 4 messages
    msgs = [ChatMessage(role="user", content=f"M{i}") for i in range(4)]
    
    # Limit - 1 (3 messages)
    res_minus_1 = await manager.process(msgs, model, max_messages=3)
    assert "M3" in res_minus_1
    assert "M2" in res_minus_1
    assert "M1" in res_minus_1
    assert "M0" not in res_minus_1
    
    # Limit (4 messages)
    res_exact = await manager.process(msgs, model, max_messages=4)
    for i in range(4):
        assert f"M{i}" in res_exact
        
    # Limit + 1 (5 messages)
    res_plus_1 = await manager.process(msgs, model, max_messages=5)
    for i in range(4):
        assert f"M{i}" in res_plus_1

@pytest.mark.asyncio
async def test_boundary_token_limit(manager, model):
    # Create single tokens approximately
    msgs = [
        ChatMessage(role="system", content="S"),
        ChatMessage(role="user", content="A"),
        ChatMessage(role="assistant", content="B"),
        ChatMessage(role="user", content="C")
    ]
    # Each message has overhead (~4 tokens) + 1 content token = ~5 tokens
    # Total for 4 messages is ~20 tokens.
    
    # Limit - 1 (e.g., 14 tokens) - enough for System + C + B (15 tokens total required) - B will fail.
    res_minus = await manager.process(msgs, model, max_tokens=14)
    assert "S" in res_minus
    assert "C" in res_minus
    assert "B" not in res_minus # B is dropped
    assert "A" not in res_minus
    
    # Limit (e.g., 16 tokens) - enough for System + C + B.
    res_exact = await manager.process(msgs, model, max_tokens=16)
    assert "S" in res_exact
    assert "C" in res_exact
    assert "B" in res_exact
    assert "A" not in res_exact
    
    # Limit + 1 (e.g., 22 tokens) - enough for all.
    res_plus = await manager.process(msgs, model, max_tokens=22)
    assert "S" in res_plus
    assert "A" in res_plus
    assert "B" in res_plus
    assert "C" in res_plus

@pytest.mark.asyncio
async def test_long_individual_message(manager, model):
    # A single message that alone exceeds the token budget
    msgs = [
        ChatMessage(role="user", content="Extremely long text. " * 5000)
    ]
    # Even if it exceeds max_tokens, it's the ONLY request and the LATEST request,
    # so the context manager MUST preserve it and let the LLM throw the error.
    result = await manager.process(msgs, model, max_tokens=10)
    assert "Extremely long text." in result
