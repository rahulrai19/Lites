import asyncio
from typing import List
from app.api.models import ChatMessage
from app.tokenizer.types import TokenCounter

class ConversationContextManager:
    def __init__(self, tokenizer: TokenCounter):
        self.tokenizer = tokenizer

    async def process(self, messages: List[ChatMessage], model: str, max_tokens: int = 128000, max_messages: int = 50) -> str:
        """
        Applies a chronological sliding window to retain system prompts, the current request, 
        and the most recent contextual messages within bounded limits.
        """
        if not messages:
            return ""
            
        if len(messages) == 1:
            return messages[0].content

        # Count tokens for all messages concurrently for high performance
        async def count_msg(msg: ChatMessage) -> int:
            res = await self.tokenizer.count_tokens(msg.content, model)
            return res.token_count + 4 # 4 tokens overhead per message for chat markup

        token_counts = await asyncio.gather(*(count_msg(msg) for msg in messages))
        
        preserved_indices = set()
        total_tokens = 0
        
        # 1. Lock in System Prompt (Required Anchor)
        has_system = messages[0].role.lower() == "system"
        if has_system:
            preserved_indices.add(0)
            total_tokens += token_counts[0]
            
        # 2. Lock in Current Request / Last Message (Required Anchor)
        last_idx = len(messages) - 1
        if last_idx not in preserved_indices:
            preserved_indices.add(last_idx)
            total_tokens += token_counts[last_idx]
            
        # 3. Sliding Window backwards (newest context to oldest context)
        for i in range(last_idx - 1, -1, -1):
            if i in preserved_indices:
                continue
                
            if len(preserved_indices) >= max_messages:
                break
                
            if total_tokens + token_counts[i] > max_tokens:
                # Token budget exceeded, stop including older history
                break
                
            preserved_indices.add(i)
            total_tokens += token_counts[i]
            
        # 4. Chronological reconstruction
        sorted_indices = sorted(list(preserved_indices))
        return "\n".join([messages[i].content for i in sorted_indices])
