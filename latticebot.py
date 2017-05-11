import discord
import asyncio

roledict = {'i am 18+': '18+',
            'dyn': 'dynastic',
            'pxl': 'pxls',
            'bl': 'black spaces',
            'dg': 'dark greens',
            'lg': 'light greens',
            'mobile': 'place_mobile'}
emojidict = {'grapu': 'grapu',
             'graypu': 'graypu',
             'greypu': 'graypu',
             'gaypu': 'gaypu',
             'cherru': 'cherru',
             'voidpu': 'voidpu',
             'owo': 'owo'}
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
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

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

    if message.content.lower().startswith('!role '):
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

    elif message.content.lower().startswith('!help'):
        await client.send_message(message.channel, 'To request a role, just say "!role " and any number of the following options:\n' +
                                  'i am 18+ - gains you access to our NSFW room\n' +
                                  'dyn - sets you as a dynastic user\n' +
                                  'pxl - sets you as a pxls.space user\n' +
                                  'mobile - sets you as a place mobile user\n' +
                                  'All of the site specific roles will provide you access to their respective diplomacy channel\n' +
                                  'bl - Makes you a Black Tile User\n' +
                                  'dg - Makes you a Dark Green Tile User\n' +
                                  'lg - Makes you a Light Green Tile User')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('no creds plz')
