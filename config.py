import os
from dotenv import load_dotenv

# Determine the environment (default: local)
APP_ENV = os.getenv("APP_ENV", "local")

# Choose the correct .env file
env_file = f".env.docker.{APP_ENV}" if "docker" in APP_ENV else ".env.local"
load_dotenv(env_file)

# Load environment variables
DEBUG = os.getenv("DEBUG", "False") == "True"
DATABASE_URL = os.getenv("DATABASE_URL", "HIDDEN" if not DEBUG else None)
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))
