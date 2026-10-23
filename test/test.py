import requests

# Target URL (replace with your running server or test endpoint like httpbin.org)
url = "http://127.0.0.1:8000/"

# Data payload you want to send
payload = {
    "plate": "5//V.FD6G0",
}

# Send the POST request with JSON data
response = requests.post(url, json=payload)

# Print the server's response
print("Status Code:", response.status_code)
print("Response Body:", response.text)
