import pytest
from app.optimizer.router import AdaptiveRouter
from app.models.context import ContextProfile
from app.config.env import env

@pytest.fixture
def router():
    # Make sure we have a dummy Gemini key to allow routing
    env.GEMINI_API_KEY = "dummy-test-key"
    return AdaptiveRouter()

def test_simple_request_routing(router):
    """
    Expected cheaper model when policy allows.
    A simple gpt-4o request (< 200 tokens) should route to Gemini.
    """
    decision = router.route("Hello world", "gpt-4o", token_count=50, context=ContextProfile.CHAT)
    
    assert decision.did_route is True
    assert decision.selected_model == "gemini-1.5-flash"
    assert "Prompt is simple" in decision.reason
    assert decision.estimated_cost_saved > 0.0
    assert decision.signals["token_count"] == 50
    assert decision.signals["is_expensive_target"] is True

def test_complex_request_routing(router):
    """
    Expected more capable model when policy requires it.
    A large request (> 200 tokens) should stay on the expensive model.
    """
    decision = router.route("A very long document...", "gpt-4o", token_count=500, context=ContextProfile.CHAT)
    
    assert decision.did_route is False
    assert decision.selected_model == "gpt-4o"
    assert "Prompt exceeds complexity threshold" in decision.reason
    assert decision.estimated_cost_saved == 0.0

def test_high_quality_requirement(router):
    """
    Verify routing policy respects quality configuration.
    CODE context should never route away from a capable model, even if simple.
    """
    decision = router.route("def foo(): pass", "gpt-4-turbo", token_count=30, context=ContextProfile.CODE)
    
    assert decision.did_route is False
    assert decision.selected_model == "gpt-4-turbo"
    assert "Quality requirement too high" in decision.reason
    assert "CODE" in decision.reason

def test_provider_unavailable(router):
    """
    Verify fallback behavior if supported.
    If GEMINI_API_KEY is missing, routing should instantly disable.
    """
    env.GEMINI_API_KEY = None  # Simulate missing provider
    
    decision = router.route("Hello", "gpt-4", token_count=10, context=ContextProfile.CHAT)
    
    assert decision.did_route is False
    assert decision.selected_model == "gpt-4"
    assert "Routing disabled: GEMINI_API_KEY not configured" in decision.reason
    assert decision.signals["provider_available"] is False

def test_explainability_fields(router):
    """
    Every routing decision should expose:
    * selected model
    * reason
    * relevant signals
    * estimated cost
    """
    decision = router.route("Summarize", "gpt-4o", token_count=100, context=ContextProfile.CHAT)
    
    # Assert explainability interfaces
    assert hasattr(decision, 'selected_model')
    assert hasattr(decision, 'reason')
    assert hasattr(decision, 'signals')
    assert hasattr(decision, 'estimated_cost_saved')
    
    # Assert signals contains required introspection data
    assert "token_count" in decision.signals
    assert "context_profile" in decision.signals
    assert "original_estimated_cost" in decision.signals
    assert "new_estimated_cost" in decision.signals
