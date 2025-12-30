import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID") or 0)
    API_HASH = os.getenv("API_HASH")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    SESSION_NAME = os.getenv("SESSION_NAME", "teleagent_session")
    OWNER_ID = int(os.getenv("OWNER_ID") or 0)
