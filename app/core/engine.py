import time
import asyncio
from typing import Optional, Tuple
from datetime import datetime

from app.cache.provider import CacheProvider
from app.cache.models import CacheEntry
from app.cache.semantic import InMemorySemanticCache
from app.cache.embedder import Embedder
from app.cache.hasher import hash_prompt
from app.optimizer.decision import DecisionEngine, OptimizationAction
from app.optimizer.engine import RuleOptimizerEngine
from app.optimizer.ai_engine import AIOptimizerEngine
from app.models.context import ContextProfile
from app.tokenizer.types import TokenCounter
from app.core.client import LLMClient
from app.telemetry.tracker import TelemetryTracker

class LitesCoreEngine:
    def __init__(
        self,
        exact_cache: CacheProvider,
        semantic_cache: InMemorySemanticCache,
        embedder: Embedder,
        token_counter: TokenCounter,
        rule_engine: RuleOptimizerEngine,
        ai_engine: AIOptimizerEngine,
        decision_engine: DecisionEngine,
        llm_client: LLMClient,
        telemetry: Optional[TelemetryTracker] = None
    ):
        self.exact_cache = exact_cache
        self.semantic_cache = semantic_cache
        self.embedder = embedder
        self.token_counter = token_counter
        self.rule_engine = rule_engine
        self.ai_engine = ai_engine
        self.decision_engine = decision_engine
        self.llm_client = llm_client
        self.telemetry = telemetry

    async def execute(self, prompt: str, model: str, context: Optional[ContextProfile] = None) -> str:
        """
        The central Lites orchestration pipeline.
        1. Exact Cache Check
        2. Semantic Cache Check
        3. Token Counting & Optimization Decision
        4. Apply Optimization (Rule or AI)
        5. Execute via LLM Client
        6. Store Result in Cache
        """
        # --- 1. Exact Cache Check ---
        if self.telemetry:
            await self.telemetry.record_request()
            
        prompt_hash = hash_prompt(prompt, model)
        exact_hit = await self.exact_cache.get(prompt_hash)
        if exact_hit:
            if self.telemetry:
                await self.telemetry.record_exact_cache_hit()
            return exact_hit.response

        # --- 2. Semantic Cache Check ---
        embedding = await self.embedder.get_embedding(prompt)
        if embedding:
            semantic_hit = await self.semantic_cache.search(embedding, model)
            if semantic_hit:
                if self.telemetry:
                    await self.telemetry.record_semantic_cache_hit()
                return semantic_hit.response

        # --- 3. Token Counting & Decision ---
        count_result = await self.token_counter.count_tokens(prompt, model)
        token_count = count_result.token_count
        decision = self.decision_engine.evaluate(token_count)
        
        # --- 4. Optimization ---
        optimized_prompt = prompt
        
        start_opt_time = time.time()
        if decision.action == OptimizationAction.RULE_OPTIMIZE:
            optimized_prompt, metadata = await self.rule_engine.optimize(prompt, model, context)
            if self.telemetry:
                await self.telemetry.record_rule_savings(metadata.tokens_saved)
        elif decision.action == OptimizationAction.AI_OPTIMIZE:
            optimized_prompt, metadata = await self.ai_engine.optimize(prompt, model, context)
            if self.telemetry:
                await self.telemetry.record_ai_savings(metadata.tokens_saved)
                
        if self.telemetry and decision.action != OptimizationAction.SKIP:
            overhead_ms = int((time.time() - start_opt_time) * 1000)
            await self.telemetry.record_overhead(overhead_ms)
            
        # --- 5. Execute via LLM Client ---
        # Note: Lites signature metadata will be appended to the user prompt in the final proxy (Phase 9)
        # For now, we execute the optimized prompt.
        response_text = await self.llm_client.execute(optimized_prompt, model)
        
        # --- 6. Store Result in Cache (Fire-and-forget in real system, awaiting here for simplicity) ---
        new_entry = CacheEntry(
            response=response_text,
            model=model,
            timestamp=datetime.now()
        )
        await self.exact_cache.set(prompt_hash, new_entry)
        
        if embedding:
            await self.semantic_cache.store(embedding, model, new_entry)
            
        return response_text
