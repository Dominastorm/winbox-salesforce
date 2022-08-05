import time
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
import json
import datetime

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

# returns a list of user_ids of all contacts
def get_all_contact_ids():
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(f'{DOMAIN_URL}/services/data/v55.0/query/?q=SELECT+Id+FROM+Contact', headers=headers)
    contacts = json.loads(response.text)['records']
    return [ contact['Id'] for contact in contacts ]

# returns the details of all the contacts
def get_all_contact_details():
    for i in get_all_contact_ids():
        print(get_user_data(i))

# updates the contact details using user_id and a dictionary containing the new field name : field value pairs
def update_field_values(user_id, updates):
    access_token = get_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = updates
    response = requests.patch(f'{DOMAIN_URL}/services/data/v55.0/sobjects/Contact/{user_id}', headers=headers, data=json.dumps(data))
    return response.text

# reads events.json and gets creates/updated emails from it
def get_updated_emails():
    events = open('EMP-Connector\events.json', 'r').read().splitlines()
    events = [json.loads(event) for event in events]
    emails = []

    for event in events:
        change_type = event['payload']['ChangeEventHeader']['changeType']
        if change_type == 'CREATE':
            if 'Email' in event['payload']:
                emails.append(event['payload']['Email'])
            else:
                # no email field
                break

        elif change_type == 'UPDATE':
            if 'Email' in event['payload']['ChangeEventHeader']['changedFields']:
                # get their user id and print email
                user_id = event['payload']['ChangeEventHeader']['recordIds'][0]
                emails.append(json.loads(get_user_data(user_id))['Email'])
            else:
                # did not change email
                break
    return emails

# checks if events.json has been modified since last time. Calls get_updated_emails if it has
def check_events_file():
    last_modified_file = Path('.') / 'lastModified'
    if last_modified_file.exists():
        last_modified_time = datetime.datetime.strptime(last_modified_file.read_text(), '%Y-%m-%d %H:%M:%S.%f').timestamp()
        if last_modified_time > os.stat('EMP-Connector\events.json').st_mtime:
            return None
    emails = get_updated_emails()
    # write current time into lastModified file
    last_modified_file.touch()
    last_modified_file.write_text(str(datetime.datetime.now()))
    return emails
