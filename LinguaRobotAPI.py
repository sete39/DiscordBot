import requests

word = "idiotic"
key = "da236143-fa4b-4b34-b53e-72dedb0189d7"
url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s" %(word, key)


response = requests.get(url)
jsonFile = response.json()
print("%i. %s" % (i, s) for s, i in zip(jsonFile[0]['shortdef'], range(0, len(jsonFile[0]['shortdef']))))

for s, i in zip(jsonFile[0]['shortdef'], range(0, len(jsonFile[0]['shortdef']))):
    print("%i. %s" % (i+1, s))