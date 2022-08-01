import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import json

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.environ['CONSUMER_KEY']
CLIENT_SECRET = os.environ['CONSUMER_SECRET']
PASSWORD = os.environ['PASSWORD']
DOMAIN_URL = 'https://growthspree-dev-ed.my.salesforce.com'

# Get access token
def get_access_token():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=password&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&username=dhruv@growth-spree.com&password={PASSWORD}'
    response = requests.post(f'{DOMAIN_URL}/services/oauth2/token', headers=headers, data=data)
    
    return eval(response.text)['access_token']

# Get user data using user_id
def get_user_data(user_id):
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(f'{DOMAIN_URL}/services/data/v55.0/sobjects/Contact/{user_id}', headers=headers)
    return json.dumps(json.loads(response.text), indent = 1)
    