from pydantic import BaseModel
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from helpers.utils import get_prompt
from agents.models import get_llm_model

class QueryModerationResult(BaseModel):
    """
    Result model for query moderation.
    
    Attributes:
        category: Classification category for the query
        action: Recommended action to take
    """
    category: Literal[
        "valid_agricultural",
        "invalid_language", 
        "invalid_non_agricultural",
        "invalid_external_reference",
        "invalid_compound_mixed",
        "cultural_sensitive",
        "unsafe_illegal",
        "political_controversial",
        "role_obfuscation",
    ]
    action: str

    def __str__(self):
        return f"[{self.category}] {self.action}"

_moderation_agent = None

def get_moderation_agent() -> Agent:
    """
    Get or create the moderation agent instance (lazy initialization).
    
    Returns:
        Agent: Configured moderation agent
        
    Raises:
        ValueError: If LLM configuration is invalid
        FileNotFoundError: If prompt template is not found
    """
    global _moderation_agent
    if _moderation_agent is None:
        _moderation_agent = Agent(
            model=get_llm_model(),
            name="Moderation Agent",
            system_prompt=get_prompt('moderation_system'),
            output_type=QueryModerationResult,
            model_settings=ModelSettings(temperature=0.0)
        )
    return _moderation_agent

def reset_moderation_agent() -> None:
    """
    Reset the moderation agent singleton. 
    Primarily used for testing to ensure clean state between tests.
    """
    global _moderation_agent
    _moderation_agent = None