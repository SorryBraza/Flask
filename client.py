import requests


# response = requests.post(
#     "http://127.0.0.1:5000/ads/",
#     json={'header': 'header2', 'description': 'description3', 'owner': 'owner3'},
# )

# response = requests.get('http://127.0.0.1:5000/ads/10')
# response = requests.delete("http://127.0.0.1:5000/ads/10",)

print(response.status_code)
print(response.text)