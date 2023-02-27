import requests

url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"

food = input("Enter food: ")

querystring = {"ingr":"1 " + food}

headers = {
	"X-RapidAPI-Key": "b9d9e48884mshcd3b1e80bcbbca0p1f65fajsn2999ad0fce27",
	"X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)