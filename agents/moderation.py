from pydantic import BaseModel, Field
from typing import Literal
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from helpers.utils import get_prompt
from agents.models import get_llm_model

class QueryModerationResult(BaseModel):
    category: Literal[
        "valid_agricultural",
        "invalid_language", 
        "invalid_non_agricultural",
        "invalid_external_reference",
        "unsafe_illegal",
        "political_controversial"
    ]
    action: str

    def __str__(self):
        return f"[{self.category}] {self.action}"

moderation_agent = Agent(
    model=get_llm_model(),
    name="Moderation Agent",
    system_prompt=get_prompt('moderation_system'),
    output_type=QueryModerationResult,
    model_settings=ModelSettings(temperature=0.0)
)