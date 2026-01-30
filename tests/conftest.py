import os

# Set dummy environment variables for CI/testing if not present
os.environ.setdefault("OPENAI_API_KEY", "dummy-key-for-testing")
