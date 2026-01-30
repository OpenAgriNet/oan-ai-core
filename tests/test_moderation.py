
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from agents.moderation import get_moderation_agent, reset_moderation_agent, QueryModerationResult

class TestModerationAgent(unittest.IsolatedAsyncioTestCase):

    def tearDown(self):
        """Reset singleton state after each test."""
        reset_moderation_agent()

    @patch('agents.moderation.Agent')
    @patch('agents.moderation.get_llm_model')
    async def test_moderation_agent_run_valid(self, mock_get_llm, mock_agent_class):
        """Test the moderation agent with a valid agricultural query."""
        mock_model = MagicMock()
        mock_get_llm.return_value = mock_model
        
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        query = "How to grow tomatoes?"
        agent = get_moderation_agent()
        
        mock_result = MagicMock()
        mock_result.output = QueryModerationResult(
            category="valid_agricultural",
            action="Proceed with the query"
        )
        
        with patch.object(agent, 'run', new=AsyncMock(return_value=mock_result)):
            result = await agent.run(query)
        
        self.assertEqual(result.output.category, "valid_agricultural")
        self.assertIn("Proceed", result.output.action)

    @patch('agents.moderation.Agent')
    @patch('agents.moderation.get_llm_model')
    async def test_moderation_agent_run_invalid(self, mock_get_llm, mock_agent_class):
        """Test the moderation agent with an invalid query."""
        mock_model = MagicMock()
        mock_get_llm.return_value = mock_model
        
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        query = "What is the capital of France?"
        agent = get_moderation_agent()
        
        mock_result = MagicMock()
        mock_result.output = QueryModerationResult(
            category="invalid_non_agricultural",
            action="Decline the query"
        )
        
        with patch.object(agent, 'run', new=AsyncMock(return_value=mock_result)):
            result = await agent.run(query)
        
        self.assertEqual(result.output.category, "invalid_non_agricultural")
        self.assertIn("Decline", result.output.action)

    def test_query_moderation_result_str(self):
        """Test QueryModerationResult string representation."""
        result = QueryModerationResult(
            category="valid_agricultural",
            action="Proceed with the query"
        )
        str_repr = str(result)
        self.assertEqual(str_repr, "[valid_agricultural] Proceed with the query")

    @patch('agents.moderation.Agent')
    @patch('agents.moderation.get_llm_model')
    def test_get_moderation_agent_singleton(self, mock_get_llm, mock_agent_class):
        """Test that get_moderation_agent returns the same instance (singleton pattern)."""
        mock_model = MagicMock()
        mock_get_llm.return_value = mock_model
        
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent
        
        # First call creates the agent
        agent1 = get_moderation_agent()
        # Second call returns the same instance
        agent2 = get_moderation_agent()
        
        self.assertIs(agent1, agent2)
        # Verify the Agent class is only initialized once
        mock_agent_class.assert_called_once()

if __name__ == '__main__':
    unittest.main()
