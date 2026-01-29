
import sys
import os

# Add current directory to path so we can import helpers
sys.path.append(os.getcwd())

try:
    from helpers.utils import get_prompt
    # Use existing prompt file
    content = get_prompt("moderation_system")
    print("Successfully loaded prompt.")
    print("Content preview:")
    print(content[:50])
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
