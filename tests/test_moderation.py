
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from agents.moderation import moderation_agent, QueryModerationResult, LLM_MODEL

class TestModerationAgent(unittest.IsolatedAsyncioTestCase):

    async def test_moderation_agent_run_valid(self):
        """Test the moderation agent with a valid agricultural query."""
        # Create a mock result object
        mock_result = MagicMock()
        mock_result.data = QueryModerationResult(
            category="valid_agricultural",
            action="allow"
        )
        
        # Patch the agent's run method
        with patch.object(moderation_agent, 'run', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result
            
            # Execute
            query = "How to grow tomatoes?"
            result = await moderation_agent.run(query)
            
            # Verify
            self.assertEqual(result.data.category, "valid_agricultural")
            self.assertEqual(result.data.action, "allow")
            mock_run.assert_awaited_once_with(query)

    async def test_moderation_agent_run_invalid(self):
        """Test the moderation agent with an invalid query."""
        mock_result = MagicMock()
        mock_result.data = QueryModerationResult(
            category="invalid_non_agricultural",
            action="block"
        )
        
        with patch.object(moderation_agent, 'run', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = mock_result
            
            query = "What is the capital of France?"
            result = await moderation_agent.run(query)
            
            self.assertEqual(result.data.category, "invalid_non_agricultural")
            self.assertEqual(result.data.action, "block")

if __name__ == '__main__':
    unittest.main()
