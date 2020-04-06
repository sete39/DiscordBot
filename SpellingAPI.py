import requests

url = "https://montanaflynn-spellcheck.p.rapidapi.com/check/"
word = "amazing"
querystring = {"text":word}

headers = {
    'x-rapidapi-host': "montanaflynn-spellcheck.p.rapidapi.com",
    'x-rapidapi-key': "addea4b612msh7072eb469649abdp13b57fjsnce0a638eb2d9"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
jsonFile = response.json()
print(response.text)
#print(response.json()['corrections'][querystring['text']])
if word in jsonFile['corrections']:
    print("Correction: " + jsonFile['suggestion'] + '\n'
    + 'Other possible corrections: ' + jsonFile['corrections'][word])
else:
    print('Correction: ' + jsonFile['suggestion'])