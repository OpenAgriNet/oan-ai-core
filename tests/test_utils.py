
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

from helpers.utils import get_logger, get_prompt

class TestUtils(unittest.TestCase):

    def test_get_logger(self):
        """Test that get_logger returns a logger with the correct name and level."""
        logger_name = "test_logger"
        logger = get_logger(logger_name)
        
        self.assertEqual(logger.name, logger_name)
        # Assuming DEBUG is the default level set in get_logger
        import logging
        self.assertEqual(logger.level, logging.DEBUG)
        self.assertGreater(len(logger.handlers), 0)

    @patch('helpers.utils.Environment')
    def test_get_prompt_logic(self, mock_env_cls):
        """Test the logic of get_prompt without actual file I/O using mocks."""
        
        # Setup mock environment and template
        mock_env_instance = MagicMock()
        mock_template = MagicMock()
        mock_env_cls.return_value = mock_env_instance
        mock_env_instance.get_template.return_value = mock_template
        mock_template.render.return_value = "Rendered Content"

        # Test inputs
        prompt_file = "test_prompt"
        context = {"key": "value"}
        
        # Execute
        result = get_prompt(prompt_file, context)

        # Verify
        self.assertEqual(result, "Rendered Content")
        
        # Verify Environment was called with autoescape
        call_args = mock_env_cls.call_args
        self.assertIsNotNone(call_args)
        # We can't easily check the autoescape value since it's a function from select_autoescape,
        # but we can verify it was passed.
        self.assertIn('autoescape', call_args[1])
        
        # Verify get_template was called with .md extension appended
        mock_env_instance.get_template.assert_called_with("test_prompt.md")
        
        # Verify render was called with context
        mock_template.render.assert_called_with(**context)

    def test_get_prompt_integration(self):
        """Integration test with a real temporary file."""
        import tempfile
        import shutil

        # Create a temporary directory for prompts
        test_dir = tempfile.mkdtemp()
        try:
            # Create a dummy prompt file
            prompt_content = "Hello {{ name }}!"
            prompt_filename = "hello_world.md"
            with open(os.path.join(test_dir, prompt_filename), 'w') as f:
                f.write(prompt_content)

            # Call get_prompt pointing to this directory
            # We need to calculate the relative path from project root or use the prompt_dir arg logic
            # Since get_prompt calculates full path based on project root, we might need to be careful.
            # However, get_prompt logic is:
            # current_dir = .../helpers
            # project_root = .../
            # full_prompt_dir = join(project_root, prompt_dir)
            
            # So if we pass an absolute path as prompt_dir, it might fail if join uses it as relative.
            # os.path.join(base, "/abs/path") returns "/abs/path" on Linux/Mac, and usually on Windows too if drive matches.
            # Let's try passing the absolute path of test_dir as prompt_dir.
            
            result = get_prompt("hello_world", {"name": "User"}, prompt_dir=test_dir)
            self.assertEqual(result, "Hello User!")
            
        finally:
            shutil.rmtree(test_dir)

if __name__ == '__main__':
    unittest.main()
