import os
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

from dotenv import load_dotenv

load_dotenv()


# Simplified model selector
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai').lower()
LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'gpt-4o')

if LLM_PROVIDER == 'openai':
    LLM_MODEL = OpenAIModel(
        LLM_MODEL_NAME,
        api_key=os.getenv('OPENAI_API_KEY')
    )

elif LLM_PROVIDER == 'groq':
    LLM_MODEL = GroqModel(
        LLM_MODEL_NAME,
        provider=GroqProvider(
            api_key=os.getenv('GROQ_API_KEY'),
        ),
    )
else:
    raise ValueError(f"Invalid LLM_PROVIDER: {LLM_PROVIDER}. Must be one of: 'openai', 'groq'")
