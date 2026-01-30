from pydantic import BaseModel, Field
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from helpers.utils import get_prompt
from agents.models import LLM_MODEL

class QueryModerationResult(BaseModel):
    category: Literal[
        "valid_agricultural",
        "invalid_language",
        "invalid_non_agricultural",
        "invalid_external_reference",
        "invalid_compound_mixed",
        "unsafe_illegal",
        "political_controversial",
        "cultural_sensitive",
        "role_obfuscation"
        # ... add all categories relative to your prompt
    ]
    action: str

    def __str__(self):
        return f"[{self.category}] {self.action}"

moderation_agent = Agent(
    model=LLM_MODEL,
    name="Moderation Agent",
    system_prompt=get_prompt('moderation_system'),
    output_type=QueryModerationResult,
    model_settings=ModelSettings(temperature=0.0)
)