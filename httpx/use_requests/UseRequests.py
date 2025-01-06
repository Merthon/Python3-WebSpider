import requests

response = requests.get("http://books.toscrape.com/")
if response.ok:
    print(response.text)
else:
    print("Error:", response.status_code)
# print(response) #<Response [200]>
# print(response.status_code) #200