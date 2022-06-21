import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents = intents)

# основные ключи их ИД (каналы роли и тп)
keys = {
    'channelCreate': 966766930033803335,
    'channelRPcategory': 966130119691337788,
    'messageIDEmoji': 966799197280043068,
    'emojiautoID': 966831758534381609,
    'playerRole': 966130611150524477,
    'bankOfarcihve': 966376462909308968,
    'xranitelhistory': 966789769092808824
}

# бот загружен
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# отправление ембеда от бота
@bot.command()
@commands.has_role("cavum nigrum")
async def embed(ctx, title: str, *args):
    await ctx.message.delete()
    embed = discord.Embed(description = ' '.join(args), colour = 0, title = title)
    await ctx.send(embed = embed)

# сообщение от бота
@bot.command()
@commands.has_role("cavum nigrum")
async def text(ctx, *args):
    await ctx.message.delete()
    await ctx.send(' '.join(args))

# архивирование канала
@bot.command()
@commands.has_role(keys['xranitelhistory'])
async def archive(ctx):
    if ctx.channel.category.id != keys['channelRPcategory']:
        print(f'{ctx.message.author} has been tryed to use archive command on not RP category!!')
        return

    await ctx.message.delete()
    overwrites_keys = list(ctx.message.channel.overwrites.keys())

    for foo in range(len(overwrites_keys)):
        if overwrites_keys[foo].name[0] == "|":
            await ctx.message.channel.set_permissions(overwrites_keys[foo].members[0], send_messages = False)
            await overwrites_keys[foo].delete()
            await ctx.channel.edit(category =  discord.utils.get(ctx.guild.categories, id = keys['bankOfarcihve']))

    embed = discord.Embed(description = f'Спасибо всем игрокам за участие в активности сообщества в этой ролевой игре! Надеемся увидеть вашу новую историю =)\n\nИстория архивирована.', colour = 0, title = 'Чёрная дыра затянула историю')
    await ctx.channel.send(embed = embed)

# авторизация
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != keys['messageIDEmoji']:
        return
    if payload.emoji.id != keys['emojiautoID']:
        return

    role = discord.utils.get(payload.member.guild.roles, id = keys['playerRole'])
    await payload.member.add_roles(role)

# изменение названия роли владельца рп канала
@bot.event
async def on_guild_channel_update(before, after):
    if before.category.id != keys['channelRPcategory']:
        return

    if before.name != after.name:
        overwrites_keys = list(before.overwrites.keys()) # просто так занимает ячейку памяти

        for foo in range(len(overwrites_keys)):
            if overwrites_keys[foo].name[0] == "|": # костыль для проверки 
                await overwrites_keys[foo].edit(name = f'| {after.name}')

# удаление роли при удалении канала 
@bot.event
async def on_guild_channel_delete(channel):
    if channel.category.id != keys['channelRPcategory']:
        return

    overwrites_keys = list(channel.overwrites.keys())

    for foo in range(len(overwrites_keys)): # костыль для проверки 
        if overwrites_keys[foo].name[2::] == channel.name:
            await overwrites_keys[foo].delete()

# создание текстового рп канала
@bot.event
async def on_voice_state_update(member, before, after):
    # checkup right channel
    if after.channel != bot.get_channel(keys['channelCreate']):
        return

    # проверка на кол-во созданных каналов
    count = 0
    for foo in range(len(member.roles)):
        if member.roles[foo].name[0] == '|':
            count += 1

    # если больше двух каналов -отказ (подсчёт по ролям)
    if count >= 2:
        embed = discord.Embed(description = f'Вы превысили ограничение на создание текстово-ролевых каналов (2) в сообществе {member.guild.name}. Пожалуйста, удалите ненужный текстовый канал, чтобы создать новый. \n\nХорошей игры!', colour = 0, title = 'Оповещение')
        await member.send(embed = embed)
        return 

    await member.move_to(None) # кик из войс канала

    # создание текстового канала
    guild = member.guild
    role = await guild.create_role(name = f'| история-{member.name}', colour = 1, mentionable = True) # НЕ РАБОТАЕТ ЕСЛИ ПОМЕНЯТЬ ФОРМАТ "история-{member.name}"
    overwrites = {
        guild.get_role(role.id): discord.PermissionOverwrite(
            manage_channels = True, 
            send_tts_messages = True, 
            manage_webhooks = True, 
            manage_messages = True,
            send_messages = True),

        guild.default_role: discord.PermissionOverwrite(
            read_messages = False),

        guild.get_role(keys['playerRole']): discord.PermissionOverwrite(
            read_messages = True),
        member: discord.PermissionOverwrite(
            read_messages = True)
    }

    channel = await guild.create_text_channel(name = f'История {member.name}', category = bot.get_channel(keys['channelRPcategory']), overwrites = overwrites)
    await member.add_roles(role)
    embed = discord.Embed(description = f'Спасибо, {member.mention}, за проявление активности в нашем сообществе! Тебе выданы полные права администрирования этого канала. Первым делом, советуем переназвать его! А всё остальное — твое творчество: вебхуки, создание веток для квент и тому подобное.\n\n Для определения концовки истории и архивации текстового канала необходимо обратиться к роли "Хранитель историй".\n\nХорошей игры!', colour = 0, title = '⠀')
    await channel.send(embed=embed)

bot.run('OTY2MzQ4ODgzNjE5ODcyNzc4.YmAchw.IyLod0sBH0d-wHZzWOOsLM1fXGA')