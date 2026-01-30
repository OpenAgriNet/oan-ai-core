import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Track loggers that have been configured to prevent duplicate handlers
_configured_loggers = set()

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
    
    # Only add handler if this logger hasn't been configured yet
    if name not in _configured_loggers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        ch.setLevel(level)
        logger.addHandler(ch)
        _configured_loggers.add(name)
    
    # Always update the logger level (allows level changes after initial config)
    logger.setLevel(level)
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