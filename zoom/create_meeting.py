import requests
import time

# Replace these variables with your actual data
access_token = "eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImVkYThhMzZjLTUxMjktNGNmMC04NjhmLWM1YzNiNDJhMmZmZCJ9.eyJhdWQiOiJodHRwczovL29hdXRoLnpvb20udXMiLCJ1aWQiOiJBQXVkbEEwY1RDQ3FkdVFRaEVkUmJnIiwidmVyIjo5LCJhdWlkIjoiZDZhZTIyZTlhMTg1NTNhYjRhZWI4NjE5ZTlhMzJjMTMiLCJuYmYiOjE3MDgzMTMzNDgsImNvZGUiOiJ3ZUpTMEdfWlRWaXBQYUltT3YwOWtncTZPTGp2NDBmbVUiLCJpc3MiOiJ6bTpjaWQ6VGFMRjdZbDRUMFNsdEdKaHJOVXBQQSIsImdubyI6MCwiZXhwIjoxNzA4MzE2OTQ4LCJ0eXBlIjozLCJpYXQiOjE3MDgzMTMzNDgsImFpZCI6IklaUHB2QTB4UTEta0U4NDBFckZReEEifQ.ZvnR8igPwvsRILp7fq6QcU2AKljwy1vVgz5WHC4NsG-l_cGbIibfdHk55qTfrIJxYUuTKLIAUDZXE16g6e0_Rw"
user_id = 'shreyas.kar@gmail.com'
meeting_details = {
    "topic": "My Meeting",
    "type": 2,
    "start_time": "2024-02-18T14:58:45",
    "duration": 30, # Duration in minutes
    "timezone": "America/New_York",
    "agenda": "Discuss project updates",
    "settings": {
        "auto_recording": "cloud" # Ensure meeting is recorded in the cloud for transcript
    }
}

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.post(f'https://api.zoom.us/v2/users/{user_id}/meetings', 
                         headers=headers, 
                         json=meeting_details)

if response.status_code == 201:
    meeting_info = response.json()
    print("Meeting Created:", meeting_info["start_url"])
else:
    print("Failed to create meeting:", response.text)
