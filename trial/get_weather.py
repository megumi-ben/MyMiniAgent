import requests

url = "https://open-weather13.p.rapidapi.com/city"

querystring = {"city":"new york","lang":"EN"}

headers = {
	"x-rapidapi-key": "233ac3bb36mshcc33feefaa6dba5p1df36cjsn5ccbf45c3865",
	"x-rapidapi-host": "open-weather13.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())