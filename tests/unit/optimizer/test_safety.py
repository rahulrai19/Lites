import pytest
from app.optimizer.engine import RuleOptimizerEngine
from app.tokenizer.openai_tokenizer import OpenAITokenizer

@pytest.fixture
def engine():
    tokenizer = OpenAITokenizer()
    return RuleOptimizerEngine(tokenizer)

# --- 1. Negative Instructions ---
@pytest.mark.asyncio
async def test_safety_negative_instructions(engine):
    prompts = [
        "Do not delete the database.",
        "Never remove authentication.",
        "Do not expose the API key.",
        "Do not modify the production server.",
        "Do not disable validation."
    ]
    for prompt in prompts:
        optimized, metadata = await engine.optimize(prompt, "gpt-4o")
        # Assert NO-OP
        assert optimized == prompt
        assert metadata.tokens_saved == 0

# --- 2. Conditional Instructions ---
@pytest.mark.asyncio
async def test_safety_conditional_instructions(engine):
    prompts = [
        "If the request fails, retry it.",
        "Only delete the file if it is temporary.",
        "Do not deploy unless tests pass."
    ]
    for prompt in prompts:
        optimized, metadata = await engine.optimize(prompt, "gpt-4o")
        assert optimized == prompt

# --- 3. Technical Content ---
@pytest.mark.asyncio
async def test_safety_technical_content(engine):
    # JSON
    json_prompt = '{"config": {"please": "do not remove"}, "retries": 3}'
    assert (await engine.optimize(json_prompt, "gpt-4o"))[0] == json_prompt

    # YAML
    yaml_prompt = "server:\n  port: 8080\n  host: localhost"
    assert (await engine.optimize(yaml_prompt, "gpt-4o"))[0] == yaml_prompt

    # Code / SQL
    sql_prompt = "SELECT * FROM users WHERE status = 'active';"
    assert (await engine.optimize(sql_prompt, "gpt-4o"))[0] == sql_prompt
    
    code_prompt = "def hello():\n    print('please')\n"
    optimized_code = (await engine.optimize(code_prompt, "gpt-4o"))[0]
    assert optimized_code == code_prompt
    # Regex
    regex_prompt = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    assert (await engine.optimize(regex_prompt, "gpt-4o"))[0] == regex_prompt

# --- 4. Similar Words ---
@pytest.mark.asyncio
async def test_safety_similar_words(engine):
    # "Please" is a filler word, but if used as a verb it shouldn't be touched.
    # The current regex looks for "Please" at the start of the string.
    # Let's test if "Please the customer" is improperly modified.
    prompt = "Please the customer by providing a refund."
    optimized = (await engine.optimize(prompt, "gpt-4o"))[0]
    # Because our regex blindly matches "Please" at the start, it might strip it.
    # Let's assert it shouldn't strip it.
    assert optimized == prompt
