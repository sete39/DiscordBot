import requests
import pandas as pd
url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

querystring = {"country":"Canada"}
args = ['Canada', 'total']
querystring = {"country": args[0]}
if (args[0] == 'world'):
    querystring = {"country": ''}

headers = {
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': "addea4b612msh7072eb469649abdp13b57fjsnce0a638eb2d9"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
jsonFile = response.json()
df = pd.DataFrame(jsonFile['data']['covid19Stats'])
print('Confirmed cases: %i' % df['confirmed'].sum() + '\n'
'Deaths: %i' % df['deaths'].sum() + '\n'
'Recovered: %i' % df['recovered'].sum() + '\n')