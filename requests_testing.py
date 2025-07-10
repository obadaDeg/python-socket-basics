import requests
import os

# r = requests.get('https://xkcd.com/353/')

# print(r)
# print(r.status_code)
# print(r.ok)
# print(r.headers)
# print(r.encoding)
# print(r.text)
# print(r.json())  # This will raise an error since the response is not JSON


# r = requests.get('https://imgs.xkcd.com/comics/python.png')

# print(r.status_code)
# # print(r.content)

# with open('python.png', 'wb') as f:
#     f.write(r.content)

# r = requests.get('https://httpbin.org/get')
# print(r.status_code)
# print(r.json())

# r = requests.get('https://httpbin.org/get', params={'name': 'Obada', 'age': 20})
# print(r.status_code)
# print(r.json())

# r = requests.post('https://httpbin.org/post', data={'name': 'Obada', 'age': 20})
# print(r.status_code)
# print(r.json())

# r = requests.delete('https://httpbin.org/delete', data={'name': 'Obada', 'age': 20})
# print(r.status_code)
# print(r.text)

# r = requests.put('https://httpbin.org/put', data={'name': 'Obada', 'age': 20})
# print(r.status_code)
# print(r.text)

# print('=' * 20, 'HEAD Request', '=' * 20)
# r = requests.head('https://httpbin.org/get')
# print(r.status_code)
# print(r.headers)
# print(r.text)  # This will not contain the body of the response

# print('=' * 20, 'File Upload', '=' * 20)
# files = {'file': open('python.png', 'rb')}
# r = requests.post('https://httpbin.org/post', files=files)
# print(r.status_code)
# print(r.json())

# print('=' * 20, 'File Download', '=' * 20)
# url = 'https://imgs.xkcd.com/comics/python.png'
# response = requests.get(url)
# if response.status_code == 200:
#     file_path = os.path.join('downloaded_files', 'python.png')
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
#     with open(file_path, 'wb') as f:
#         f.write(response.content)
#     print(f"File downloaded successfully: {file_path}")
# else:
#     print(f"Failed to download file. Status code: {response.status_code}")


# print('=' * 20, 'Timeout Example', '=' * 20)
# try:
#     for i in range(1, 6, 4):
#         response = requests.get(f'https://httpbin.org/delay/{i}', timeout=2)
#         print(response.status_code)
# except requests.Timeout:
#     print("The request timed out. Please try again later.")

# print('=' * 20, 'Authentication', '=' * 20)

# username = 'Obada'
# password = '1234'
# for i in range(3):
#     r = requests.get('https://httpbin.org/basic-auth/Obada1/1234', auth=(username + str(i), password))
#     if r.status_code == 200:
#         print("Authentication successful!")
#         print(r.json())
#         break
#     else:
#         print(f"Authentication failed. Attempt {i + 1} of 3.")
#         if i == 2:
#             print("Max attempts reached. Please check your credentials.")


# print("=" * 20, "Bearer auth", "=" * 20)

# r = requests.get('https://httpbin.org/bearer', headers={'Authorization': 'Bearer jnqj1j3rnjnvanjkfnanekfk2'})
# print(r.status_code)
# if r.status_code == 200:
#     print("Bearer authentication successful!")
#     print(r.json())
# else:
#     print("Bearer authentication failed.")
#     print(r.text)

# print("=" * 20, "Digest auth", "=" * 20)

# what is digest auth?
# # Digest authentication is a more secure method of authentication than basic authentication.
# # It uses a challenge-response mechanism to authenticate the user.
# # The server sends a challenge to the client, which includes a nonce (a random number) and a realm (a string that identifies the protected area).
# # The client then responds with a hash of the username, password, nonce, realm, and the requested resource.
# # The server then checks the hash and responds with a 200 OK status code if the authentication is successful.

# from requests.auth import HTTPDigestAuth
# r = requests.get('https://httpbin.org/digest-auth/auth/Obada/1234', auth=HTTPDigestAuth('Obada', '1234'))
# print(r.status_code)
# if r.status_code == 200:
#     print("Digest authentication successful!")
#     print(r.json())
# else:
#     print("Digest authentication failed.")
#     print(r.text)

# print("=" * 20, "Status Codes", "=" * 20)

# codes = '200,201,202,204,301,302,303,304,307,308,400,401,403,404,405,408,409,410,500,501,502,503'
# r = requests.get(f'https://httpbin.org/status/{codes}')
# print(r.status_code)
# if r.ok:
#     print("Status codes retrieved successfully!")
#     print(r.json())
# else:
#     print("Failed to retrieve status codes.")
#     print(r.text)

# print("=" * 20, "Request & Response Inspection", "=" * 20)

# r = requests.get('https://httpbin.org/headers')
# print(r.status_code)
# print(r.text)

# r = requests.get('https://httpbin.org/ip')
# print(r.status_code)
# print(r.text)

# r = requests.get('https://httpbin.org/user-agent')
# print(r.status_code)
# print(r.text)


# r = requests.get('https://httpbin.org/cache')
# print(r.status_code)
# print(r.headers)
# print(r.text)

# r = requests.get('https://httpbin.org/cache/1')
# print(r.status_code)
# print(r.headers)
# print(r.text)



# print("=" * 20, "Custom Headers", "=" * 20)
# headers = {
#     'User-Agent': 'MyCustomClient/1.0',
#     'Accept': 'application/json',
#     'Authorization': 'Bearer my_token',
#     'X-Custom-Header': 'CustomValue'
# }
# r = requests.get('https://httpbin.org/headers', headers=headers)
# print(r.status_code)
# if r.ok:
#     print("Custom headers sent successfully!")
#     print(r.json())
# else:
#     print("Failed to send custom headers.")
#     print(r.text)
    

# print("=" * 20, "Session Management", "=" * 20)
# s = requests.Session()

# s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get('https://httpbin.org/cookies')

# print(r.text)

# s = requests.Session()
# s.auth = ('Obada', '1234')
# r = s.get('https://httpbin.org/basic-auth/Obada/1234')
# print(r.status_code)
# if r.status_code == 200:
#     print("Session authentication successful!")
#     print(r.json())
# else:
#     print("Session authentication failed.")
#     print(r.text)

# s = requests.Session()
# s.headers.update({
#     'User-Agent': 'MyCustomClient/1.0',
#     'Accept': 'application/json',
#     'Authorization': 'Bearer my_token',
#     'X-Custom-Header': 'CustomValue'
# })
# r = s.get('https://httpbin.org/headers')
# print(r.status_code)
# if r.ok:
#     print("Custom headers sent successfully!")
#     print(r.json())
# else:
#     print("Failed to send custom headers.")
#     print(r.text)


