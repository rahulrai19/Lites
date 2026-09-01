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
    
    assert result.action == OptimizationAction.SKIP
    assert "exceeds the maximum threshold" in result.reason
    assert "2000" in result.reason

def test_applies_rule_optimize_within_thresholds():
    engine = DecisionEngine(min_tokens=50, max_tokens=1000)
    result = engine.evaluate(100)
    
    assert result.action == OptimizationAction.RULE_OPTIMIZE
    assert "within thresholds" in result.reason

def test_uses_environment_variables_by_default():
    # Because we mocked/imported the env singleton, 
    # the defaults should be 50 and 128000
    engine = DecisionEngine()
    
    # 49 should skip
    assert engine.evaluate(49).action == OptimizationAction.SKIP
    
    # 50 should rule optimize
    assert engine.evaluate(50).action == OptimizationAction.RULE_OPTIMIZE
    
    # 100000 should rule optimize
    assert engine.evaluate(100000).action == OptimizationAction.RULE_OPTIMIZE
    
    # 130000 should skip
    assert engine.evaluate(130000).action == OptimizationAction.SKIP
