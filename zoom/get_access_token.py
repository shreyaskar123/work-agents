import requests
import base64

# Replace these variables with your actual data
CLIENT_ID = 'TaLF7Yl4T0SltGJhrNUpPA'
CLIENT_SECRET = '0E1AXOODpbeRPK4GMtMgBt6JM9wyMtDV'
ACCOUNT_ID = 'IZPpvA0xQ1-kE840ErFQxA'
def fetch_bearer_token():
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ACCOUNT_ID}"
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(token_url, headers=headers)
    if response.status_code == 200:
        print(response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(f"Error fetching bearer token: {response.text}")
fetch_bearer_token()