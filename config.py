import os
from dotenv import load_dotenv

# Load the environment variables from the creds.env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'creds.env'))


# Set your bot token and API key from the environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
