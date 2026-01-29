import os
import logging
from jinja2 import Environment, FileSystemLoader

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def get_prompt(prompt_file: str, context: dict = {}, prompt_dir: str = "assets/prompts") -> str:
    if not prompt_file.endswith(".md"):
        prompt_file += ".md"
    
    # Ensure usage of absolute or relative path correctly
    base_dir = os.getcwd()
    full_prompt_dir = os.path.join(base_dir, prompt_dir)
    
    env = Environment(loader=FileSystemLoader(full_prompt_dir), autoescape=False)
    template = env.get_template(prompt_file)
    return template.render(**context)