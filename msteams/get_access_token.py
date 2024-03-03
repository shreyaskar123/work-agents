import requests

# Replace these with your app's values
tenant_id = "4685d189-f9dd-44e5-b654-d4a3bc6f919b"
client_id = "16cbe266-8d48-4069-a704-9bd9d7f379bd"
client_secret = "Fli8Q~gMbInfrCsoKRY5OnBRweln1c42liJYKbs~"
scope = "https://graph.microsoft.com/.default"

url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "client_id": client_id,
    "scope": scope,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

response = requests.post(url, headers=headers, data=data)
# Check for successful response
if response.status_code == 200:
    # Extract the access token from the response
    access_token = response.json().get("access_token")
    print(access_token)
else:
    # Print error details
    print("Error obtaining access token:", response.text)
