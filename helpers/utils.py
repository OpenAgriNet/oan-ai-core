import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Track handlers created by get_logger to avoid duplicates
_logger_handlers = {}

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get or create a logger with the specified name and level.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        level: Logging level (default: INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Remove and close only handlers created by this function
    if name in _logger_handlers:
        old_handler = _logger_handlers[name]
        logger.removeHandler(old_handler)
        old_handler.close()
    
    # Add a new handler with the specified level
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(level)
    logger.addHandler(ch)
    logger.setLevel(level)
    
    # Track the handler for future cleanup
    _logger_handlers[name] = ch
    
    return logger

def get_prompt(prompt_file: str, context: dict = None, prompt_dir: str = "assets/prompts") -> str:
    """
    Load and render a Jinja2 prompt template.
    
    Args:
        prompt_file: Name of the prompt file (with or without .md extension)
        context: Dictionary of variables to render in the template
        prompt_dir: Directory containing prompt templates (relative to project root)
        
    Returns:
        str: Rendered prompt content
        
    Raises:
        FileNotFoundError: If the prompt directory or template file is not found
        ValueError: If template rendering fails
    """
    if not prompt_file.endswith(".md"):
        prompt_file += ".md"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    full_prompt_dir = os.path.join(project_root, prompt_dir)
    
    if not os.path.exists(full_prompt_dir):
        raise FileNotFoundError(f"Prompt directory not found: {full_prompt_dir}")
    
    env = Environment(
        loader=FileSystemLoader(full_prompt_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    try:
        template = env.get_template(prompt_file)
    except Exception as e:
        raise FileNotFoundError(f"Prompt template '{prompt_file}' not found in {full_prompt_dir}") from e
    
    if context is None:
        context = {}
    
    try:
        return template.render(**context)
    except Exception as e:
        raise ValueError(f"Failed to render template '{prompt_file}': {e}") from e