import discord
import private_token
import gsheet
import crawl_data
token = private_token.discord_token
intents = discord.Intents.all()

# discord에서 받은 메세지를 기반으로 crawl_data.py에서 데이터를 가져와서 gsheet.py에서 스프레드시트로 업로드
def upload(news_url, message_author):
    date, title, offer, classification = crawl_data.get_data(news_url)
    gsheet.gsheet_upload(date, title, news_url, offer, message_author, classification)

# discord Client class를 생성합니다.
client = discord.Client(intents=intents)

# event decorator를 설정하고 on_ready function을 할당해줍니다.
@client.event
async def on_ready():  # on_ready event는 discord bot이 discord에 정상적으로 접속했을 때 실행됩니다.
    print('We have logged in as {}'.format(client))
    print('Bot name: {}'.format(client.user.name))  # 여기서 client.user는 discord bot을 의미합니다. (제가 아닙니다.)
    print('Bot ID: {}'.format(client.user.id))  # 여기서 client.user는 discord bot을 의미합니다. (제가 아닙니다.)

# event decorator를 설정하고 on_message function을 할당해줍니다.
@client.event
async def on_message(message):
    #채널 이름(링크복사하면 주소있음.)
    channel_id = 채널ID
    channel = client.get_channel(channel_id)

    if message.channel.id == channel_id:
        message = await channel.fetch_message(channel.last_message_id) #병렬처리용?
        if message.content[:5] == 'https' and 'youtu' in message.content or 'naver' in message.content:
            #메세지 정보
            print(message.content)
            message_author = message.author.nick #별명
            #별명이 없는 경우 
            if message_author == None:
                message_author = message.author.name #이름
            print(message_author)
            #스프레드시트 업로드
            upload(message.content, message_author)

        elif message.content[:5] != 'https' and 'youtu' in message.content or 'naver' in message.content:
            # message란 discord 채널에 올라오는 (bot이 보낸 message도 포함) 모든 message를 의미합니다.
            # 아래 조건은 message의 author가 bot(=clinet.user)이라면 그냥 return으로 무시하라는 뜻입니다.
            # bot의 채팅이 on_message에 의해 반복되는거 방지.
            if message.author == client.user:
                return
            else:
                await message.channel.send('https를 포함한 주소를 입력해주세요.')

        else:
            if message.author == client.user:
                return
            else:
                await message.channel.send('유튜브 혹은 네이버 링크를 올려주세요.')

        # #메세지 자동 삭제
        await message.delete()

# 위에서 설정한 client class를 token으로 인증하여 실행합니다.
client.run(token)