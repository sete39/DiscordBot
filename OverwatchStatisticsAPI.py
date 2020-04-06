import pandas as pd
import requests

region = 'eu'
player = 'M9BH-2163'
url = "http://owapi.io/profile/pc/%s/%s" % (region, player)

print(url)

response = requests.get(url)
if (response.status_code == 200):
    # print('Player level: %i' % response.json()['level'])
    # print('Quickplay play time: ' + str(response.json()['playtime']['quickplay']))
    # print('Current competitive play time: ' + str(response.json()['playtime']['competitive']))
    # print('Competitive win rate: ' + str(response.json()['games']['competitive']['win_rate']))
    # print('Competitive games won: ' + str(response.json()['games']['competitive']['won']))
    # print('Competitive ranks (tank, dps, support): %s %s %s' % (
    #     str(response.json()['competitive']['tank']['rank']), 
    #     str(response.json()['competitive']['damage']['rank']), 
    #     str(response.json()['competitive']['support']['rank'])
    #     ))
    
    print('Player level: %i' % response.json()['level'] + '\n'
    'Quickplay play time: ' + str(response.json()['playtime']['quickplay']) + '\n'
    'Current competitive play time: ' + str(response.json()['playtime']['competitive'])+ '\n'
    'Competitive win rate: ' + str(response.json()['games']['competitive']['win_rate']) + '\n'
    'Competitive games won: ' + str(response.json()['games']['competitive']['won']) + '\n'
    'Competitive ranks (tank, dps, support): %s %s %s' % (
        str(response.json()['competitive']['tank']['rank']), 
        str(response.json()['competitive']['damage']['rank']), 
        str(response.json()['competitive']['support']['rank'])
        ))
else:
    print(response.status_code)

# @client.command(name='overwatch')
# async def getOverwatchStats(context, *args):
#     region = args[0]
#     player = args[1]
#     url = "http://owapi.io/profile/pc/%s/%s" % (region, player)

#     print(url)

#     response = requests.get(url)
#     jsonFile = response.json()
#     if (response.status_code == 200):
#         await context.message.channel.send('Player level: %i' % jsonFile['level'] + '\n'
#         'Quickplay play time: ' + str(jsonFile['playtime']['quickplay']) + '\n'
#         'Current competitive play time: ' + str(jsonFile['playtime']['competitive'])+ '\n'
#         'Competitive win rate: ' + str(jsonFile['games']['competitive']['win_rate']) + '\n'
#         'Competitive games won: ' + str(jsonFile['games']['competitive']['won']) + '\n'
#         'Competitive ranks (tank, dps, support): %s %s %s' % (
#             str(jsonFile['competitive']['tank']['rank']), 
#             str(jsonFile['competitive']['damage']['rank']), 
#             str(jsonFile['competitive']['support']['rank'])
#             ))
#         print('Done')
#     else:
#         print(response.status_code)
