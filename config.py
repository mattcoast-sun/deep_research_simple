import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file (absolute path for reliability)
env_path = (Path(__file__).resolve().parent / '.env')
load_dotenv(dotenv_path=env_path)

# Optional fallback: try to import from apikey.py if present
try:
    from apikey import openai_api_key as fallback_openai_api_key  # type: ignore
except Exception:
    fallback_openai_api_key = None

def get_openai_api_key() -> str:
    """
    Get OpenAI API key from environment variable or apikey.py fallback.
    
    Priority:
    1. OPENAI_API_KEY environment variable (loaded from .env file or system)
    2. apikey.py file (for local development fallback)
    
    Returns:
        str: The OpenAI API key
        
    Raises:
        ValueError: If no API key is found
    """
    # Try environment variable first (this will include .env file variables)
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        return api_key
    
    # Fallback to apikey.py for local development
    if fallback_openai_api_key:
        return fallback_openai_api_key

    raise ValueError(
        f"No OpenAI API key found. Expected OPENAI_API_KEY in {env_path} or environment. "
        "Alternatively, create apikey.py with openai_api_key='...'."
    )

# For backward compatibility
openai_api_key = get_openai_api_key()
