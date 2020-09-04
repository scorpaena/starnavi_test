import requests

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk5MTY3MzcxLCJqdGkiOiJhYjJjZjM5MmU4MzU0ZWExOTk2OWMxMzM1NDk0ZDQ4ZiIsInVzZXJfaWQiOjF9.TXbpwkRldgoy2c7osv4MgK8V1dbhXDnoQOgdz8BLcY'
r = requests.get('http://127.0.0.1:8000/post/', headers = headers)
print(r.text)
