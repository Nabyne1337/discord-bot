import discord
from discord.ext import commands
import sqlite3
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    nickname TEXT,
    service_account TEXT,
    game_account TEXT,
    user_position TEXT,
    user_group TEXT,
    ares_balance INTEGER,
    activity_points INTEGER,
    bans INTEGER,
    mutes INTEGER
)''')
conn.commit()
conn.close()

@bot.command(name='menu')
async def send_menu(ctx):
    user_id = ctx.author.id
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Проверка на инфу бд
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if user_data:
        username = user_data[1]
        nickname = user_data[2]
        service_account = user_data[3]
        game_account = user_data[4]
        user_position = user_data[5]
        user_group = user_data[6]
        ares_balance = user_data[7]
        activity_points = user_data[8]
        bans = user_data[9]
        mutes = user_data[10]
    else:
        await ctx.send("Вы не зарегистрированы в базе данных. Пожалуйста, зарегистрируйтесь, введя следующие данные:\nВведите ваше имя:")
        
        def check(message):
            return message.author == ctx.author
        
        try:
            response = await bot.wait_for('message', check=check, timeout=60)
            username = response.content
            user_position = "Нету"
            user_group = "Нету"
            ares_balance = 0
            activity_points = 0
            bans = 0
            mutes = 0
            await ctx.send("Введите ваш служебный аккаунт:")
            response = await bot.wait_for('message', check=check, timeout=60)
            service_account = response.content
            await ctx.send("Введите ваш игровой аккаунт:")
            response = await bot.wait_for('message', check=check, timeout=60)
            game_account = response.content
            nickname = ctx.author.nick or ctx.author.name
            cursor.execute('INSERT INTO users (user_id, username, nickname, service_account, game_account, user_position, user_group, ares_balance, activity_points, bans, mutes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, username, nickname, service_account, game_account, user_position, user_group, ares_balance, activity_points, bans, mutes))
            conn.commit()
        except asyncio.TimeoutError:
            await ctx.send("Время на регистрацию истекло.")
            conn.close()
            return
    embed = discord.Embed(title="Информация о пользователе", color=0x3498db)
    embed.add_field(name="", value=f'**👨‍💼Имя**: {username}')
    embed.add_field(name="", value=f'**⚜️Должность**: {user_position}')
    embed.add_field(name="", value=f'**🔅Группа**: {user_group}')
    embed.add_field(name="", value=f'**🔥Служебный аккаунт**: {service_account}')
    embed.add_field(name="", value=f'**⚡️Игровой аккаунт**: {game_account}')
    embed.add_field(name="", value=f'**⌚️Дискорд**: {nickname}')
    embed.add_field(name="", value=f'**💳Баланс аресов**: {ares_balance}')
    embed.add_field(name="", value=f'**💎Баллы активности**: {activity_points}')
    embed.add_field(name="", value=f'**:speech_balloon:Баны**: {bans}')
    embed.add_field(name="", value=f'**:speech_balloon:Муты**: {mutes}')
    await ctx.send(embed=embed)
    conn.close()

TOKEN = ''
bot.run(TOKEN)
