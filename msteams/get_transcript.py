import requests
import time

# Replace the placeholders with your actual values
access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6InNUWGI5bl9pbVEtdDZiNV92OWNxNnk4Ni0ySVVyWUdURE85RnIwNHNCTjgiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtXYmthYTZxczh3c1RuQndpaU5ZT2hIYm5BdyIsImtpZCI6ImtXYmthYTZxczh3c1RuQndpaU5ZT2hIYm5BdyJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC80Njg1ZDE4OS1mOWRkLTQ0ZTUtYjY1NC1kNGEzYmM2ZjkxOWIvIiwiaWF0IjoxNzA4MjgzMDU5LCJuYmYiOjE3MDgyODMwNTksImV4cCI6MTcwODI4Njk1OSwiYWlvIjoiRTJOZ1lHQ1VWWlRlMW52dW40K2kvbFUxbDF4NUFBPT0iLCJhcHBfZGlzcGxheW5hbWUiOiJ0ZWFtcy1hZ2VudCIsImFwcGlkIjoiMTZjYmUyNjYtOGQ0OC00MDY5LWE3MDQtOWJkOWQ3ZjM3OWJkIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNDY4NWQxODktZjlkZC00NGU1LWI2NTQtZDRhM2JjNmY5MTliLyIsImlkdHlwIjoiYXBwIiwib2lkIjoiNjQ3ZTgyY2UtYzY1Yi00NWZjLTgxZmItNmFlZjc1YjVmOTcyIiwicmgiOiIwLkFhZ0FpZEdGUnQzNTVVUzJWTlNqdkctUm13TUFBQUFBQUFBQXdBQUFBQUFBQUFEekFBQS4iLCJyb2xlcyI6WyJPbmxpbmVNZWV0aW5ncy5SZWFkV3JpdGUuQWxsIiwiVXNlci5SZWFkV3JpdGUuQWxsIiwiT25saW5lTWVldGluZ0FydGlmYWN0LlJlYWQuQWxsIiwiT25saW5lTWVldGluZ1JlY29yZGluZy5SZWFkLkFsbCIsIk9ubGluZU1lZXRpbmdUcmFuc2NyaXB0LlJlYWQuQWxsIl0sInN1YiI6IjY0N2U4MmNlLWM2NWItNDVmYy04MWZiLTZhZWY3NWI1Zjk3MiIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJOQSIsInRpZCI6IjQ2ODVkMTg5LWY5ZGQtNDRlNS1iNjU0LWQ0YTNiYzZmOTE5YiIsInV0aSI6ImZsZkVfTFhFblVHS1JKbmlsWEVTQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjA5OTdhMWQwLTBkMWQtNGFjYi1iNDA4LWQ1Y2E3MzEyMWU5MCJdLCJ4bXNfdGNkdCI6MTcwODE5NjkxNH0.Cc9KFkykn_c64MsFjn9QCyfXuGFBrXZZAuPqzrWCodHRIuKDLIBOpM1HFWADfndwBhWs5FX8-ljl9tAFp0M6dNJxO9Z2x1NA9zAR9wKVr1Jrm-aT3vqYguqEt__KgingndBioTKppkBj1iqFjBnuAbWAClv3vS1isip7IV2ECf-oqTqsMyZjT37tySvpbOh37_G8cbx4LtDJoSzeeRT7kXhIeVQcfRv4rejIeTKNxA8HpDZ32A2vKALSA5PGcGUHqbr36rM08KNaMahQWWnLJoX7GKoaodeVJfvs1VlArr1j3qffI_g1yuNxOLynf6_OTUVhQC0vn2nyrOin9cwZhg"
user_id = "065ecef0-c14f-41f5-b2e3-7fe4ac02de20"

def create_teams_meeting(access_token, user_id):
    endpoint = f"https://graph.microsoft.com/v1.0/users/{user_id}/onlineMeetings"
    print(endpoint)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    json_data = {
        "startDateTime": "2024-02-18T20:56:00Z",
        "endDateTime": "2024-02-18T21:56:00Z",
        "subject": "Test Meeting"
    }

    response = requests.post(endpoint, headers=headers, json=json_data)
    if response.status_code == 201:
        return response.json()
    else:
        print(response.text)
        return None

def wait_for_meeting_to_end(end_time):
    # Simplified wait logic based on end time
    # In a real scenario, you would check the actual meeting status or monitor activity
    current_time = time.time()
    while current_time < end_time:
        time.sleep(60)  # Check every minute (for example)
        current_time = time.time()
    print("Meeting has ended.")

def get_meeting_transcript(meeting_id):
    # Placeholder for obtaining transcript logic
    # Actual implementation would depend on where the meeting recording is stored
    print(f"Obtaining transcript for meeting ID: {meeting_id}")
    # Implement logic based on storage location (Microsoft Stream or OneDrive)
    # For Microsoft Stream, use Graph API to access the video and its transcript
    # For OneDrive, if no transcript, use speech-to-text services like Azure Speech Service
    return "Transcript placeholder"

# Create a Teams meeting
meeting_info = create_teams_meeting(access_token, user_id)
if meeting_info:
    print("Meeting created successfully.")
    meeting_id = meeting_info["id"]
    # Convert endDateTime to a timestamp and adjust logic accordingly
    # Simplification for example purposes
    end_time = time.mktime(time.strptime(meeting_info["endDateTime"], "%Y-%m-%dT%H:%M:%S.%fZ"))
    wait_for_meeting_to_end(end_time)
    transcript = get_meeting_transcript(meeting_id)
    print(transcript)
else:
    print("Failed to create meeting.")
