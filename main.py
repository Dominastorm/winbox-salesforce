import requests
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.environ['CONSUMER_KEY']
CLIENT_SECRET = os.environ['CONSUMER_SECRET']
PASSWORD = os.environ['PASSWORD']


def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=password&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&username=dhruv@growth-spree.com&password={PASSWORD}'
    response = requests.post('https://growthspree-dev-ed.my.salesforce.com/services/oauth2/token', headers=headers, data=data)
    
    return eval(response.text)['access_token']
