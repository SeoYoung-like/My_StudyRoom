import requests 

resp = requests.get("https://httpbin.org/get")
print(resp.text)