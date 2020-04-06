import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import numpy as np
# from bs4 import BeautifulSoup

token = 'Njk0OTkyMDE5MTY4MTY2MDIx.XoTsQA.7I79yywDCsWN0SDaZS085OS6SoE'
prefix = ';'
client = commands.Bot(command_prefix=prefix)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--enable-javascript")
driver = webdriver.Chrome('c:\\chromedriver\\chromedriver.exe', options=chrome_options)

@client.command(name='move')
async def Move(context, *args):
    if (args[0] == 'all'):
        channelNameFrom = args[1]
        channelNameTo = args[2]
        channelFound = None
        channelFound = False
        print(channelNameFrom)
        print(channelNameTo)
        for channel in client.get_all_channels():
            if isinstance(channel, discord.VoiceChannel):
                if (channelNameFrom == channel.name and not channelFound):
                    channelFound = channel
                    channelFound = True
                    break

        for channel in client.get_all_channels():
            if isinstance(channel, discord.VoiceChannel):
                if (channelNameTo == channel.name and channelFound):
                    await context.message.channel.send(
                        'moving everyone from the channel %s to the channel ' % channelFound.name + channel.name)
                    for user in channelFound.members:
                        await user.move_to(channel)


def seperateCourse(args, argIndex):
    course = args[argIndex].upper()
    subject = course[0:3] # seperate subject from the course number
    courseNumber = course[3:6] 
    print('Recieved course ' + course)
    return subject, courseNumber


@client.command(name='course')
async def getCourses(context, *arg):
    url = 'https://banner.aus.edu/axp3b21h/owa/bwckschd.p_disp_dyn_sched'
    driver.get(url)  # go to banner on the headless browser
    # find the HTML element with name p_term which allows the browser to select the semester
    elem = driver.find_element_by_name('p_term')
    for option in elem.find_elements_by_tag_name('option'):
        if (option.get_attribute("value") == '202110'): 
            option.click()
    driver.find_element_by_xpath("//input[@type='submit']").click()  # find an input element with a type of submit
    elem = driver.find_element_by_id('subj_id')

    ###################### normal use ######################
    if (len(arg[0]) >= 6 and len(arg[0]) <= 9): # course codes are always at least 6 chars and less than 9
        subject, courseNumber = seperateCourse(arg, 0)
        subjectFound = False
        for option in elem.find_elements_by_tag_name('option'):
            if (option.get_attribute("value") == subject):
                option.click()
                subjectFound = True

        if (not subjectFound):
            await context.message.channel.send('Subject name not found.')
            return
        elem = driver.find_element_by_name('sel_crse')
        elem.send_keys(courseNumber)
        driver.find_element_by_xpath("//input[@type='submit']").click()
    # title argument ###########
    elif (arg[0] == 'title'):
        if (len(arg) < 2):
            await context.message.channel.send('Not enough arguments.')
            return
        courseTitle = ' '.join(arg[1:])
        print('Recieved title ' + courseTitle)

        for option in elem.find_elements_by_tag_name('option'):
            option.click()
        elem = driver.find_element_by_name('sel_title')
        elem.send_keys(courseTitle)
        driver.find_element_by_xpath("//input[@type='submit']").click()

    elif(arg[0] == 'req'):
        if (len(arg) < 2):
            await context.message.channel.send('Not enough arguments.')
            return
        subject, courseNumber = seperateCourse(arg, 1)
        subjectFound = False
        for option in elem.find_elements_by_tag_name('option'):
            if (option.get_attribute("value") == subject):
                option.click()
                subjectFound = True

        if (not subjectFound):
            await context.message.channel.send('Subject name not found.')
            return
        elem = driver.find_element_by_name('sel_crse')
        elem.send_keys(courseNumber)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        elem = driver.find_element_by_class_name('ddtitle')
        elem.find_element_by_tag_name('a').click()

        elem = driver.find_element_by_class_name(('ddlabel'))
        courseInfoList = elem.text.split(' - ')
        await context.message.channel.send('Requirments for the course %s (%s) are linked below' 
        % (courseInfoList[0], courseInfoList[2])
        )
        await context.message.channel.send(driver.current_url)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # spanTagList = soup.find_all('span')
        # for tag in spanTagList:
        #     if (tag.text == 'Corequisites: '):   
        # for elem in driver.find_element_by_class_name('fieldlabeltext'):
        #     if (elem.text)
        return
    ##### error in input #####
    else:
        await context.message.channel.send('incorrect arguments')
        return

    courseDict = {
        'Title': [],
        'Code': [],
        'CRN': [],
        'Section': []
    }
    elem = driver.find_elements_by_class_name('ddtitle')
    for element in elem:
        courseInfoList = element.text.split(' - ')
        courseDict['Title'].append(courseInfoList[0])
        courseDict['Code'].append(courseInfoList[2])
        courseDict['CRN'].append(courseInfoList[1])
        courseDict['Section'].append(courseInfoList[3])
    courseInfoDF = pd.DataFrame(courseDict)

    response = driver.page_source
    df = pd.read_html(response)
    try:
        df2 = pd.concat(df[3:-1])
        df2.reset_index(inplace=True)
        df2.drop(['index', 'Where', 'Date Range', 'Type'], axis=1, inplace=True)
        courseInfoDF = pd.concat([df2, courseInfoDF], axis=1)
        print(courseInfoDF)
        courseFullString = courseInfoDF.to_string()
        totalStrCount = 0
        while (totalStrCount < 6000 and totalStrCount < len(courseFullString)):
            totalStrCount += 2000
            await context.message.channel.send(courseFullString[(totalStrCount-2000):totalStrCount])
    except ValueError:
        await context.message.channel.send('No courses found.')

@client.command(name='prefix')
async def changePrefix(context, *args):
    global prefix
    if((len(args) > 1) or (len(args[0]) > 1)):
        prefix = (' '.join(args)) + ' '
    else:
        prefix = args[0]
    client.command_prefix = prefix
    await context.message.channel.send('prefix succesfully changed to ' + prefix)


@client.command(name='spellcheck')
async def spellcheck(context, *args):
    url = "https://montanaflynn-spellcheck.p.rapidapi.com/check/"
    word = args[0]
    querystring = {"text": word}

    headers = {
        'x-rapidapi-host': "montanaflynn-spellcheck.p.rapidapi.com",
        'x-rapidapi-key': "addea4b612msh7072eb469649abdp13b57fjsnce0a638eb2d9"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    jsonFile = response.json()
    print(response.text)
    # print(response.json()['corrections'][querystring['text']])
    if word in jsonFile['corrections']:
        await context.message.channel.send("Correction: " + ''.join(jsonFile['suggestion']) + '\n'
        + 'Other possible corrections: ' + ' '.join(jsonFile['corrections'][word]))
    else:
        await context.message.channel.send('Correction: ' + jsonFile['suggestion'])


@client.command(name='def')
async def getDefinition(context, *args):
    word = args[0]
    print(word)
    key = "da236143-fa4b-4b34-b53e-72dedb0189d7"
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/%s?key=%s" % (word, key)
    response = requests.get(url)
    jsonFile = response.json()

    fullString = ''
    for s, i in zip(jsonFile[0]['shortdef'], range(0, len(jsonFile[0]['shortdef']))):
        fullString = fullString + ("%i. %s" % (i+1, s))
        fullString = fullString + ('\n')
    await context.message.channel.send(fullString)


@client.command(name='randomgame')
async def chooseRandomGame(context):
    games = [
        'Overwatch', 'CS:GO', 'FFXIV', 'Rainbow Six Siege', 
        'Osu', 'CoD: Warzone', 'Fortnite', 'BL3',
        'Apex Legends', 'League of Legends', 'Jackbox Party Packs',
        'Super Smash Bros.', 'Animal Crossing'
    ]

    gameChosen = games[np.random.randint(len(games))]
    await context.message.channel.send('Game: ' + gameChosen)


@client.command(name='corona')
async def getCases(context, *args):
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

    querystring = {"country":"Canada"}
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
    await context.message.channel.send('Confirmed cases: %i' % df['confirmed'].sum() + '\n'
    'Deaths: %i' % df['deaths'].sum() + '\n'
    'Recovered: %i' % df['recovered'].sum() + '\n')


@client.command(name='sex')
async def changePrefix(context):
    await context.message.channel.send('yes please uwu')

client.run(token)
