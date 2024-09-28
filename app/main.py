import requests, json

url = "https://api.fda.gov/drug/label.json?count=openfda.generic_name.exact&limit=1000"


response = requests.get(url)
for medicine in response.json()['results']:
  print(medicine['term'])
