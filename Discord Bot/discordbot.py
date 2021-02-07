import discord
import time, asyncio
import requests,ast, json
import pytz
from pytz import timezone
from requests_oauthlib import OAuth1
from datetime import datetime, date, time
from backports.datetime_fromisoformat import MonkeyPatch
MonkeyPatch.patch_fromisoformat()
joined=messages=0

#'''

messages = joined = 0

token = "ODA3OTg3MDk2MTExMTUzMTcy.YB_-nw.24oj30-aJr8RNR0MoqCf41Z58xA"

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)



@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    global messages
    messages += 1

    #id = client.get_guild(807987096111153172)
    channels = ["commands", "general"]

    if str(message.channel) in channels:
        if message.content.find("!hello") != -1:
            await message.channel.send("Hi") 
        elif message.content=="!contest":
        	url = 'https://www.kontests.net/api/v1/all'
        	response=requests.get(url)
        	if response.status_code==200:
        		data=response.json()
        		contests=[] # only for CF, CodeChef, AtCoder
        		for i in data:
        			if i['site'] in ['codeChef', 'CodeForces', 'AtCoder']:
        				contests.append(i)
        		final_contest_list=list()
        		for i in contests:
        			contest_time = datetime.strptime(i['start_time'], '%Y-%m-%dT%H:%M:%S.%fz')
        			now_time = datetime.now()
        			if (contest_time.day>=now_time.day and contest_time.month>=now_time.month and contest_time.year>=now_time.year):
        				now_asia = contest_time.astimezone(timezone('Asia/Kolkata'))
        				d = datetime.fromisoformat(i['start_time'][:-1]).replace(tzinfo=pytz.utc) # we need to strip 'Z' before parsing
        				start_time = d.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d-%m-%Y %I:%M %p')
        				final_contest_list.append({'Name':i['name'], 'Site':i['site'], 'Time':start_time, 'Link':i['url']})
        				#print(json.dumps(final_contests_list,indent=1))
        				for i in final_contest_list:
        					for k,v in i.items():
        						await message.channel.send(f"{k}: {v}\n")
        			else:
        				await message.channel.send(f"Someting Went Wrong! Contact Administrator.")
        elif message.content=="!help":
        	embed=discord.Embed(title="Help on Bot", description="Some useful commands")
        	embed.add_field(name="!hello", value="Greets the user")
        	embed.add_field(name="!contest", value="Live/Upcoming Contest")
        	await message.channel.send(content=None, embed=embed)

client.loop.create_task(update_stats())
client.run(token)
#'''
