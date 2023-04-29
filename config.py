import os
from dotenv import load_dotenv

# Load the environment variables from the creds.env file
load_dotenv(dotenv_path='creds.env')

# Set your bot token and API key from the environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
