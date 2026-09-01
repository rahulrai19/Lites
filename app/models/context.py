from enum import Enum
from pydantic import BaseModel
from typing import List

class ContextProfile(str, Enum):
    DEFAULT = "default"
    CODE = "code"
    LEGAL = "legal"
    CHAT = "chat"

class OptimizationContext(BaseModel):
    profile: ContextProfile
    # A list of rule function names that are disabled for this context
    disabled_rules: List[str]

# Define the global profiles mapping
CONTEXT_PROFILES = {
    ContextProfile.DEFAULT: OptimizationContext(
        profile=ContextProfile.DEFAULT,
        disabled_rules=[]
    ),
    ContextProfile.CODE: OptimizationContext(
        profile=ContextProfile.CODE,
        disabled_rules=["normalize_whitespace"]
    ),
    ContextProfile.LEGAL: OptimizationContext(
        profile=ContextProfile.LEGAL,
        disabled_rules=["remove_fillers"]
    ),
    ContextProfile.CHAT: OptimizationContext(
        profile=ContextProfile.CHAT,
        disabled_rules=[]
    )
}
