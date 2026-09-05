import pytest
from app.optimizer.decision import DecisionEngine, OptimizationAction

def test_skips_when_tokens_below_minimum():
    engine = DecisionEngine(min_tokens=50)
    result = engine.evaluate(10)
    
    assert result.action == OptimizationAction.SKIP
    assert "below the minimum threshold" in result.reason
    assert "10" in result.reason

def test_skips_when_tokens_exceed_maximum():
    engine = DecisionEngine(max_tokens=1000)
    result = engine.evaluate(2000)
    
    assert result.action == OptimizationAction.CONTEXT_COMPRESS
    assert "exceeds safe optimization threshold" in result.reason
    assert "2000" in result.reason

def test_applies_rule_optimize_within_thresholds():
    engine = DecisionEngine(min_tokens=50, max_tokens=1000)
    result = engine.evaluate(100)
    
    assert result.action == OptimizationAction.RULE_OPTIMIZE
    assert "within standard thresholds" in result.reason

def test_uses_environment_variables_by_default():
    # Because we mocked/imported the env singleton, 
    # the defaults should be 50 and 128000
    engine = DecisionEngine()
    
    # 49 should skip
    assert engine.evaluate(49).action == OptimizationAction.SKIP
    
    # 50 should rule optimize
    assert engine.evaluate(50).action == OptimizationAction.RULE_OPTIMIZE
    
    # 100000 should trigger AI optimize (since default AI threshold is 500)
    assert engine.evaluate(100000).action == OptimizationAction.AI_OPTIMIZE
    
    # 130000 should skip
    assert engine.evaluate(130000).action == OptimizationAction.CONTEXT_COMPRESS

def test_skips_when_no_expected_savings():
    engine = DecisionEngine()
    result = engine.evaluate(1000, expected_savings=0)
    
    assert result.action == OptimizationAction.SKIP
    assert "No expected savings" in result.reason
    
    result2 = engine.evaluate(1000, expected_savings=-50)
    assert result2.action == OptimizationAction.SKIP

def test_skips_when_ai_cost_exceeds_savings():
    engine = DecisionEngine(ai_threshold=500)
    
    # 1000 tokens triggers AI optimize usually
    # But if cost is 300 and expected savings is only 100
    result = engine.evaluate(1000, expected_savings=100, ai_cost=300)
    
    assert result.action == OptimizationAction.SKIP
    assert "AI optimization costs exceed expected savings" in result.reason
    
    # If cost is 100 and expected savings is 300, it should proceed
    result2 = engine.evaluate(1000, expected_savings=300, ai_cost=100)
    assert result2.action == OptimizationAction.AI_OPTIMIZE
