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

    def test_get_logger_with_custom_level(self):
        """Test get_logger with custom logging level."""
        logger = get_logger("custom_level_logger", level=logging.WARNING)
        self.assertEqual(logger.level, logging.WARNING)

    def test_get_logger_no_duplicate_handlers(self):
        """Test that calling get_logger multiple times doesn't create duplicate handlers."""
        logger_name = "test_no_duplicate_handlers"
        
        # First call with INFO level
        logger1 = get_logger(logger_name, level=logging.INFO)
        self.assertEqual(len(logger1.handlers), 1)
        self.assertEqual(logger1.level, logging.INFO)
        
        # Second call with different level - should replace handler, not duplicate
        logger2 = get_logger(logger_name, level=logging.WARNING)
        self.assertEqual(len(logger2.handlers), 1)
        self.assertEqual(logger2.level, logging.WARNING)
        
        # Verify it's the same logger instance
        self.assertIs(logger1, logger2)
        
        # Third call with same level - still should have only one handler
        logger3 = get_logger(logger_name, level=logging.WARNING)
        self.assertEqual(len(logger3.handlers), 1)


if __name__ == '__main__':
    unittest.main()
