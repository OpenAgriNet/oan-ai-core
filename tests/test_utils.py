import unittest
import os
import logging
import tempfile
from helpers.utils import get_logger, get_prompt


class TestUtils(unittest.TestCase):

    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test_logger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")
        self.assertTrue(logger.hasHandlers())

    def test_get_prompt_with_context(self):
        """Test get_prompt with context variables."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_prompt_dir = os.path.join(tmpdir, "test_prompts")
            os.makedirs(test_prompt_dir)
            
            test_template = os.path.join(test_prompt_dir, "test_template.md")
            with open(test_template, 'w') as f:
                f.write("Hello {{ name }}, you are {{ age }} years old.")
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            relative_path = os.path.relpath(test_prompt_dir, project_root)
            
            prompt = get_prompt("test_template", context={"name": "John", "age": 30}, prompt_dir=relative_path)
            self.assertEqual(prompt, "Hello John, you are 30 years old.")

    def test_get_prompt_missing_file(self):
        """Test get_prompt with non-existent file."""
        with self.assertRaises(FileNotFoundError) as exc_context:
            get_prompt("nonexistent_file")
        self.assertIn("not found", str(exc_context.exception))

    def test_get_prompt_missing_directory(self):
        """Test get_prompt with non-existent directory."""
        with self.assertRaises(FileNotFoundError) as exc_context:
            get_prompt("test", prompt_dir="nonexistent_dir")
        self.assertIn("Prompt directory not found", str(exc_context.exception))

if __name__ == '__main__':
    unittest.main()
