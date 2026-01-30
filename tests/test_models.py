import unittest
from unittest.mock import patch, MagicMock
import os
from agents.models import get_llm_model


class TestModels(unittest.TestCase):

    @patch.dict(os.environ, {'LLM_PROVIDER': 'openai', 'OPENAI_API_KEY': 'test-key-123', 'LLM_MODEL_NAME': 'gpt-4o'})
    @patch('agents.models.OpenAIModel')
    def test_get_llm_model_openai(self, mock_openai):
        """Test get_llm_model returns OpenAI model."""
        mock_model = MagicMock()
        mock_model.model_name = 'gpt-4o'
        mock_openai.return_value = mock_model
        
        model = get_llm_model()
        self.assertIsNotNone(model)
        mock_openai.assert_called_once()

    @patch.dict(os.environ, {'LLM_PROVIDER': 'openai', 'LLM_MODEL_NAME': 'gpt-3.5-turbo', 'OPENAI_API_KEY': 'test-key-123'})
    @patch('agents.models.OpenAIModel')
    def test_get_llm_model_openai_custom_model(self, mock_openai):
        """Test get_llm_model with custom OpenAI model."""
        mock_model = MagicMock()
        mock_model.model_name = 'gpt-3.5-turbo'
        mock_openai.return_value = mock_model
        
        model = get_llm_model()
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args[0]
        self.assertEqual(call_args[0], 'gpt-3.5-turbo')

    @patch.dict(os.environ, {'LLM_PROVIDER': 'openai'}, clear=True)
    def test_get_llm_model_openai_no_api_key(self):
        """Test get_llm_model raises error when OPENAI_API_KEY is missing."""
        with self.assertRaises(ValueError) as context:
            get_llm_model()
        self.assertIn("OPENAI_API_KEY not found", str(context.exception))

    @patch.dict(os.environ, {'LLM_PROVIDER': 'groq', 'GROQ_API_KEY': 'test-groq-key', 'LLM_MODEL_NAME': 'llama-3.3-70b-versatile'})
    @patch('agents.models.GroqModel')
    def test_get_llm_model_groq(self, mock_groq):
        """Test get_llm_model returns Groq model."""
        mock_model = MagicMock()
        mock_groq.return_value = mock_model
        
        model = get_llm_model()
        self.assertIsNotNone(model)
        mock_groq.assert_called_once()

    @patch.dict(os.environ, {'LLM_PROVIDER': 'groq', 'LLM_MODEL_NAME': 'gpt-4o'}, clear=True)
    @patch('agents.models.load_dotenv')
    def test_get_llm_model_groq_no_api_key(self, mock_dotenv):
        """Test get_llm_model raises error when GROQ_API_KEY is missing."""
        with self.assertRaises(ValueError) as context:
            get_llm_model()
        self.assertIn("GROQ_API_KEY not found", str(context.exception))

    @patch.dict(os.environ, {'LLM_PROVIDER': 'invalid_provider'})
    def test_get_llm_model_invalid_provider(self):
        """Test get_llm_model raises error for invalid provider."""
        with self.assertRaises(ValueError) as context:
            get_llm_model()
        self.assertIn("Invalid LLM_PROVIDER", str(context.exception))

    @patch.dict(os.environ, {}, clear=True)
    @patch('agents.models.load_dotenv')
    def test_get_llm_model_default_provider(self, mock_dotenv):
        """Test get_llm_model defaults to openai when no provider set."""
        with self.assertRaises(ValueError) as context:
            get_llm_model()
        self.assertIn("OPENAI_API_KEY not found", str(context.exception))


if __name__ == '__main__':
    unittest.main()
