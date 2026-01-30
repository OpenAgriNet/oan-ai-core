import unittest
import os
import tempfile
from helpers.utils import get_logger, get_prompt


class TestUtils(unittest.TestCase):

    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test_logger")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")
        self.assertTrue(logger.hasHandlers())

    def test_get_logger_returns_same_instance(self):
        """Test that get_logger returns the same logger instance for the same name."""
        logger1 = get_logger("same_logger")
        logger2 = get_logger("same_logger")
        self.assertIs(logger1, logger2)

    def test_get_prompt_without_md_extension(self):
        """Test get_prompt auto-adds .md extension and loads file."""
        prompt = get_prompt("moderation_system")
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

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


if __name__ == '__main__':
    unittest.main()
