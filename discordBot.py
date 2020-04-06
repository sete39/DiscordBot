import discord

client = discord.Client()
token = 'Njk0OTkyMDE5MTY4MTY2MDIx.XoTsQA.7I79yywDCsWN0SDaZS085OS6SoE'
prefix = ';'

@client.event
async def on_message(message):
    global prefix
    if message.author == client.user:
        return

    # moving all people command
    if message.content.startswith(prefix+'move all'):
        # voiceClient = client.connect()
        contentSplit = message.content.split("'")
        print(contentSplit)
        channelNameFrom = contentSplit[1]
        channelNameTo = contentSplit[3]
        channelFound = None
        channelHasBeenFound = False
        print(channelNameFrom)
        print(channelNameTo)
        
        for channel in client.get_all_channels():
            if isinstance(channel, discord.VoiceChannel):
                if (channelNameFrom == channel.name and not channelHasBeenFound):
                    channelFound = channel
                    channelHasBeenFound = True
                    break

        for channel in client.get_all_channels():
            if isinstance(channel, discord.VoiceChannel):
                if (channelNameTo == channel.name and channelHasBeenFound):
                    await message.channel.send('moving everyone from the channel %s to the channel ' % channelFound.name + channel.name)
                    for user in channelFound.members:
                        await user.move_to(channel)
                        
    elif message.content.startswith(prefix+'prefix'):
        contentSplit = message.content.split(" ")
        prefix = ' '.join(contentSplit[1:])
        await message.channel.send('prefix succesfully changed to ' + prefix)

    elif message.content.startswith('thank you khawaja!'):
        await message.channel.send("you're welcome %s!" % message.author.name)

    elif message.content.startswith(prefix):
        await message.channel.send('Add a correct command after %s' % prefix)

client.run(token)