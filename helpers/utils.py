import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

def get_prompt(prompt_file: str, context: dict = None, prompt_dir: str = "assets/prompts") -> str:
    if not prompt_file.endswith(".md"):
        prompt_file += ".md"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    full_prompt_dir = os.path.join(project_root, prompt_dir)
    
    env = Environment(
        loader=FileSystemLoader(full_prompt_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template(prompt_file)
    if context is None:
        context = {}
    return template.render(**context)