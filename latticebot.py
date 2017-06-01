import os
import discord
import asyncio
import creds
import yaml

roledict = {'i am 18+': '18+',
            'dyn': 'dynastic',
            'pxl': 'pxls',
            'bl': 'black spaces',
            'dg': 'dark greens',
            'lg': 'light greens',
            'minecraft': 'minecraft',
            'mobile': 'place_mobile'}
client = discord.Client()

def find_role_by_name(rolename, message):
    rolelist = []
    roleobj = None
    if message.server != None:
        rolelist = message.server.roles
        for item in rolelist:
            if roledict[rolename] == item.name.lower():
                roleobj = item
    return roleobj

@client.event
async def on_message(message):
    emojidict = {'grapu': 'grapu',
                 'graypu': 'graypu',
                 'greypu': 'graypu',
                 'gaypu': 'gaypu',
                 'cherru': 'cherru',
                 'voidpu': 'voidpu',
                 'screwu': 'screwu',
                 'owo': 'owo'}

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if os.path.isfile('emoji.yml'):
        with open('emoji.yml', 'r') as emojifile:
            emojidict = yaml.load(emojifile.read())

    for item in emojidict:
        if item in message.content.lower():
            emojilist = []
            emojiobj = None
            if message.server != None:
                emojilist = message.server.emojis
                for emoji in emojilist:
                    if emoji.name == emojidict[item]:
                        emojiobj = emoji
            if emojiobj != None:
                await client.add_reaction(message, emojiobj)

    if message.content.lower() == 'ayy':
        await client.send_message(message.channel, 'lmao')

    if message.content.lower().startswith('!emoji '):
        userroles = message.author.roles
        roleobj = ''
        rolelist = message.server.roles
        userin = message.content.lower().replace('!emoji ', '')
        messagelist = userin.split()
        if len(messagelist) == 2:
            part1 = messagelist[0]
            part2 = messagelist[1]
        else:
            await client.send_message(message.channel, 'Invalid number of arguments')
        for item in rolelist:
            if 'admin' == item.name.lower():
                roleobj = item
        if roleobj != '':
            if roleobj in userroles:
                with open('emoji.yml', 'a') as writefile:
                    writefile.write('\'' + part1 + '\': \'' + part2 + '\'\n')
                sendmsg = 'Saying ' + part1 + ' will now cause latticebot to react with ' + part2
                await client.send_message(message.channel, sendmsg)
            else:
                await client.send_message(message.channel, 'You do not have permission to use this command')

    elif message.content.lower().startswith('!role '):
        addlist = []
        rmlist = []
        addname = []
        rmname = []
        userroles = message.author.roles
        if 'admin' in message.content.lower():
            await client.send_message(message.channel, 'LOL DID YOU THINK YOU\'D GET ADMIN FROM THIS? C\'MON DUDE, THINK NEXT TIME.')
            return
        for item in roledict:
            if item in message.content.lower():
                roleobj = find_role_by_name(item, message)
                if roleobj:
                    if roleobj in userroles:
                        rmlist.append(roleobj)
                        rmname.append(roledict[item])
                    else:
                        addlist.append(roleobj)
                        addname.append(roledict[item])
        if addlist and addname:
            await client.add_roles(message.author, *addlist)
            await client.send_message(message.channel, 'Assigning ' + ', '.join(addname) +' role(s)')
        if rmlist and rmname:
            await client.remove_roles(message.author, *rmlist)
            await client.send_message(message.channel, 'Removing ' + ', '.join(rmname) +' role(s)')
        if not addlist and not rmlist:
            await client.send_message(message.channel, 'You did not request any valid roles, please run !help for more info')

    elif message.content.lower() == ('!roles'):
        if message.server != None:
            rolelist = message.author.roles
            returnlist = []
            for item in rolelist:
                if 'everyone' not in item.name:
                    returnlist.append(item.name)
            returnstring = ', '.join(returnlist)
            await client.send_message(message.channel, 'Your roles are: ' + returnstring)

    elif '!coords ' in message.content.lower():
        stillgood = True
        if 'pxls' in str(message.channel).lower() or 'bot_testing' in str(message.channel).lower():
            xval = 0
            yval = 0
            msgsplit = message.content.lower().split()
            for index, item in enumerate(msgsplit):
                if '!coords' in item:
                    try:
                        nextitem = msgsplit[int(index) + 1]
                    except IndexError:
                        await client.send_message(message.channel, 'Improperly formatted input, try again.')
                        stillgood = False
                        break
                    if ',' in nextitem:
                        if nextitem.split(',')[1]:
                            nextsplit = nextitem.split(',')
                            xval = nextsplit[0]
                            yval = nextsplit[1]
                        else:
                            xval = nextitem.replace(',','').strip()
                            try:
                                yval = msgsplit[index + 2]
                            except IndexError:
                                await client.send_message(message.channel, 'Improperly formatted input, try again.')
                                stillgood = False
                                break
                    else:
                        xval = nextitem
                        try:
                            yval = msgsplit[index + 2]
                        except IndexError:
                            await client.send_message(message.channel, 'Improperly formatted input, try again.')
                            stillgood = False
                            break

            if stillgood:
                try:
                    xval = int(xval)
                    yval = int(yval)
                    returnstring = 'https://pxls.space/#x=' + str(xval) + '&y=' + str(yval) + '&scale=20'
                    await client.send_message(message.channel, returnstring)
                except ValueError:
                    await client.send_message(message.channel, 'Tried to send non-number values, try again')
        else:
            await client.send_message(message.channel, 'This command only works in pxls rooms')



    elif message.content.lower().startswith('!help'):
        await client.send_message(message.channel, 'To request a role, just say "!role " and any number of the following options:\n' +
                                  'i am 18+ - gains you access to our NSFW room\n' +
                                  'dyn - sets you as a dynastic user\n' +
                                  'pxl - sets you as a pxls.space user\n' +
                                  'mobile - sets you as a place mobile user\n' +
                                  'All of the site specific roles will provide you access to their respective diplomacy channel\n' +
                                  'bl - Makes you a Black Tile User\n' +
                                  'dg - Makes you a Dark Green Tile User\n' +
                                  'lg - Makes you a Light Green Tile User\n' +
                                  'minecraft - Lets you get pinged for minecraft announcements')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(creds.GimmeCreds())
