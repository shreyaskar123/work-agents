import jwt  # PyJWT library
import json

# Function to decode the JWT token and extract the scopes
def decode_token_and_get_scopes(access_token):
    # JWT tokens are composed of three parts separated by dots
    # Split the token to get payload part
    payload_segment = access_token.split('.')[1]
    
    # Base64 decode the payload segment
    padding = '=' * (4 - (len(payload_segment) % 4))
    payload_segment += padding
    decoded_payload = jwt.utils.base64url_decode(payload_segment)
    
    # Convert payload segment from bytes to string
    decoded_payload_str = decoded_payload.decode('utf-8')
    
    # Convert the payload string to a JSON object
    payload_json = json.loads(decoded_payload_str)
    print(payload_json)
    # Extract the scopes
    scopes = payload_json.get('scp', 'No scopes present')
    return scopes

# Replace 'your_access_token_here' with your actual access token
access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ik1XbjIzTW5xN1pFUFdCOGROR2tNdE5xWWJLellHQlZGajllTE9OemhtcHMiLCJhbGciOiJSUzI1NiIsIng1dCI6ImtXYmthYTZxczh3c1RuQndpaU5ZT2hIYm5BdyIsImtpZCI6ImtXYmthYTZxczh3c1RuQndpaU5ZT2hIYm5BdyJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC80Njg1ZDE4OS1mOWRkLTQ0ZTUtYjY1NC1kNGEzYmM2ZjkxOWIvIiwiaWF0IjoxNzA4MjgyNzMyLCJuYmYiOjE3MDgyODI3MzIsImV4cCI6MTcwODI4NjYzMiwiYWlvIjoiRTJOZ1lGalh2MEJyMXF1YUcwTHY1NnFMRnMzWkJ3QT0iLCJhcHBfZGlzcGxheW5hbWUiOiJ0ZWFtcy1hZ2VudCIsImFwcGlkIjoiMTZjYmUyNjYtOGQ0OC00MDY5LWE3MDQtOWJkOWQ3ZjM3OWJkIiwiYXBwaWRhY3IiOiIxIiwiaWRwIjoiaHR0cHM6Ly9zdHMud2luZG93cy5uZXQvNDY4NWQxODktZjlkZC00NGU1LWI2NTQtZDRhM2JjNmY5MTliLyIsImlkdHlwIjoiYXBwIiwib2lkIjoiNjQ3ZTgyY2UtYzY1Yi00NWZjLTgxZmItNmFlZjc1YjVmOTcyIiwicmgiOiIwLkFhZ0FpZEdGUnQzNTVVUzJWTlNqdkctUm13TUFBQUFBQUFBQXdBQUFBQUFBQUFEekFBQS4iLCJyb2xlcyI6WyJVc2VyLlJlYWRXcml0ZS5BbGwiXSwic3ViIjoiNjQ3ZTgyY2UtYzY1Yi00NWZjLTgxZmItNmFlZjc1YjVmOTcyIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6Ik5BIiwidGlkIjoiNDY4NWQxODktZjlkZC00NGU1LWI2NTQtZDRhM2JjNmY5MTliIiwidXRpIjoiMjJZQml5NExLRXlSUVJZSDVkc09BQSIsInZlciI6IjEuMCIsIndpZHMiOlsiMDk5N2ExZDAtMGQxZC00YWNiLWI0MDgtZDVjYTczMTIxZTkwIl0sInhtc190Y2R0IjoxNzA4MTk2OTE0fQ.gEjtw7q2L-QcaVk834af3lvLAKllYcYVuMgr8RKK7O4lNZ0H_bbuywB2BezC8XLnGIZ7i0aDAptUsvc3B3fhjNxxLEa1aJmLU2ydHMNP_RrRumee5zERhA9HGDYJthz8E6Cwe2-2VcOYXfcOirjAoscBbuJgK2_9McT1-qZRY79Dfpg3MvDB_9NyVz-9cS_cL9Y-xjF38r1eT0wf8sgzIuRj4xRSQ6FsTww-KNctHyPBjjzKy0K7oh-nDGyrFDQG1VWyJ29x2VzIXEGHt-aLIO7yoA0ZdACGxK5eTSd2_IrvA2mhnleoZ8wA3JdKvsFsEZ7WppA_Z3RlCAiX4twJFA"
# Decode the token and get the scopes
scopes = decode_token_and_get_scopes(access_token)
print('Scopes:', scopes)
