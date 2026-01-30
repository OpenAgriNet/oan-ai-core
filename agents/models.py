import os
from dotenv import load_dotenv

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider

load_dotenv()

def get_llm_model():
    """
    Lazily construct and return the configured LLM model.
    
    Returns:
        OpenAIModel | GroqModel: Configured LLM model instance
        
    Raises:
        ValueError: If LLM_PROVIDER is invalid or API key is missing
    """

    llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower()
    llm_model_name = os.getenv('LLM_MODEL_NAME', 'gpt-4o')

    if llm_provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        return OpenAIModel(
            llm_model_name,
            api_key=api_key
        )

    if llm_provider == 'groq':
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        return GroqModel(
            llm_model_name,
            provider=GroqProvider(api_key=api_key),
        )

    raise ValueError(
        f"Invalid LLM_PROVIDER: {llm_provider}. Must be one of: 'openai', 'groq'"
    )
