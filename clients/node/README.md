# lites-sdk

Official Node.js SDK for **Lites** - The lightning-fast AI proxy.

## Installation

```bash
npm install lites-sdk
```

## Usage

```typescript
import LitesClient from 'lites-sdk';

const client = new LitesClient({
  apiKey: "YOUR_API_KEY",
  litesContext: "chat" // Optional optimization profile
});

async function run() {
  const response = await client.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(response.choices[0].message.content);
}

run();
```
