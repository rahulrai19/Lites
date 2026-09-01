# Lites SDK & CLI

Official Python SDK and CLI for **Lites** - The lightning-fast AI optimization proxy.

## Usage

```python
from lites import Client

client = Client(api_key="YOUR_API_KEY")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    lites_context="code" # Optional optimization profile
)
```
