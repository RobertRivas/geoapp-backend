import os
from dotenv import load_dotenv

# Get the environment file from Docker (or default to .env)
env_file = os.getenv("ENV_FILE", ".env")

print(f"Loading environment from {env_file}")
load_dotenv(env_file)


# Load environment variables
DEBUG = os.getenv("DEBUG", "False") == "True"
DATABASE_URL = os.getenv("DATABASE_URL", "HIDDEN" if not DEBUG else None)
print(DATABASE_URL)
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
