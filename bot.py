from twitchio.ext import commands
from decouple import config

user_exist = 0


def delete_line(user):
    fn = 'data'
    f = open(fn)
    output = []
    for line in f:
        if not line.startswith(user):
            output.append(line)
    f.close()
    f = open(fn, 'w')
    f.writelines(output)
    f.close()


def calcul_tips(don):
    don = float(don.replace(',', '.'))
    # print(str(don))
    points = format(don * 0.3334, '.4f')
    # print(str(points))
    return points


def calcul_cheers(cheers):
    points = format(cheers * 0.0034, '.4f')
    # print(str(points))
    return points


def write_file(user, points):
    global user_exist
    # user = user.replace(' ', '')
    # points = points.replace(' ', '')
    data = open("data", "a+")
    Lines = open("data", "r").readlines()
    for line in Lines:
        line_split = line.split(':')
        user_list = line_split[0]
        if(user == user_list):
            old_points = line_split[1]
            total_points = float(old_points) + float(points)
            newLine = user + ': ' + str(total_points)
            delete_line(user)
            data.write(newLine + '\n')
            user_exist = 1
            print(user + ': ' + str(total_points))
    if(user_exist != 1):
        data.write(user + ':' + str(points) + '\n')
        print(user + ': ' + str(points))
    user_exist = 0


# api token can be passed as test if not needed.
# Channels is the initial channels to join, this could be a list, tuple or callable
bot = commands.Bot(
    irc_token=config('IRC_TOKEN'),
    api_token=config('API_TOKEN'),
    nick=config('NICKNAME'),
    prefix=config('PREFIX'),
    initial_channels=[config('CHANNEL')]
)


# Register an event with the bot
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')


@bot.event
async def event_message(message):
    # StreamLabs:
    # Don
    if(message.author.name == 'celestarien' or message.author.name == 'streamlabs'):
        if(message.content.find('just tipped') != -1):
            msg = message.content
            msg_split = msg.split('just tipped')
            user = msg_split[0]
            don = msg_split[1].replace('€', '')
            points = calcul_tips(don)
            # data = user + ':' + don
            write_file(user, points)

    # Sub
    # exemple: kaleb8653 just subscribed with Tier 1!
    if(message.author.name == 'celestarien' or message.author.name == 'streamlabs'):
        # "!= -1" car -1 est la valeur que ça renvois si la string n'est pas trouvée
        if(message.content.find('just subscribed with Tier') != -1):
            msg = message.content
            msg_split = msg.split('just subscribed with Tier')
            user = msg_split[0]
            tier = msg_split[1].replace('!', '')
            points = float(tier)
            # data = user + ':' + don
            write_file(user, points)

    # Cheers
    # exemple: ashitaka13400 has cheered 100 bits!
    if(message.author.name == 'celestarien' or message.author.name == 'streamlabs'):
        # "!= -1" car -1 est la valeur que ça renvois si la string n'est pas trouvée
        if(message.content.find('has cheered') != -1):
            msg = message.content
            msg_split = msg.split('has cheered')
            user = msg_split[0]
            cheers = msg_split[1].replace('bits!', '')
            points = calcul_cheers(float(cheers))
            # data = user + ':' + don
            write_file(user, points)

    # Sub Gift
    # exemple: inos___ just gifted Tier 1 subscriptions! (le nombre de gifts n'est pas indiqué)

    # SoundAlerts:
    # exemple: stiffmaester51 played You suck for 100 Bits
    if(message.author.name == 'celestarien' or message.author.name == 'soundalerts'):
        # "!= -1" car -1 est la valeur que ça renvois si la string n'est pas trouvée
        if(message.content.find('played') != -1):
            msg = message.content
            msg_split = msg.split('played')
            user = msg_split[0]
            msg_split_bits = msg_split[1].split('for')
            cheers = msg_split_bits[1].lower().replace('bits', '')
            points = calcul_cheers(float(cheers))
            # data = user + ':' + don
            write_file(user, points)

    # If you override event_message you will need to handle_commands for commands to work.
    await bot.handle_commands(message)


# Register a command with the bot
# @bot.command(name='test', aliases=['t'])
# async def test_command(ctx):
#     print('yes')
#     await ctx.send(f'Hello {ctx.author.name}')

bot.run()
