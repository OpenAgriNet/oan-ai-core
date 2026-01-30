import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from main import app, ModerationRequest


class TestMainAPI(unittest.TestCase):

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    @patch('main.get_moderation_agent')
    def test_check_moderation_success(self, mock_get_agent):
        """Test successful moderation check."""
        mock_agent = MagicMock()
        mock_result = MagicMock()
        mock_result.data = {
            "category": "valid_agricultural",
            "action": "Proceed with the query"
        }
        mock_agent.run = AsyncMock(return_value=mock_result)
        mock_get_agent.return_value = mock_agent
        
        response = self.client.post("/moderate", json={"query": "How to grow tomatoes?"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "valid_agricultural")

    @patch('main.get_moderation_agent')
    def test_check_moderation_error(self, mock_get_agent):
        """Test moderation check with error."""
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(side_effect=Exception("Test error"))
        mock_get_agent.return_value = mock_agent
        
        response = self.client.post("/moderate", json={"query": "test query"})
        
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.json()["detail"])

    def test_check_moderation_empty_query(self):
        """Test moderation with empty query."""
        response = self.client.post("/moderate", json={"query": ""})
        
        self.assertEqual(response.status_code, 422)

    def test_check_moderation_too_long_query(self):
        """Test moderation with too long query."""
        long_query = "x" * 5001
        response = self.client.post("/moderate", json={"query": long_query})
        
        self.assertEqual(response.status_code, 422)

    def test_check_moderation_missing_query(self):
        """Test moderation with missing query field."""
        response = self.client.post("/moderate", json={})
        
        self.assertEqual(response.status_code, 422)

    def test_moderation_request_model_valid(self):
        """Test ModerationRequest model with valid data."""
        request = ModerationRequest(query="Test query")
        self.assertEqual(request.query, "Test query")

    def test_moderation_request_model_max_length(self):
        """Test ModerationRequest model at max length."""
        max_query = "x" * 5000
        request = ModerationRequest(query=max_query)
        self.assertEqual(len(request.query), 5000)


if __name__ == '__main__':
    unittest.main()
