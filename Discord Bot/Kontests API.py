#Import Dependencies
import requests,ast, json
from pytz import timezone
from requests_oauthlib import OAuth1
from datetime import datetime
import pytz
url = 'https://www.kontests.net/api/v1/all'
response = requests.get(url)
if response.status_code==200:
	data = response.json()
	contests = [] # only for codeforces, codechef and atcoder
	for i in data:
		if i['site'] in ['codeChef', 'CodeForces', 'AtCoder']:
			contests.append(i)
	final_contest_list = list()
	for i in contests:
		contest_time = datetime.strptime(i['start_time'], '%Y-%m-%dT%H:%M:%S.%fz')
		now_time = datetime.now()
		if (contest_time.day>=now_time.day and contest_time.month>=now_time.month and contest_time.year>=now_time.year):
			now_asia = contest_time.astimezone(timezone('Asia/Kolkata'))
			d = datetime.fromisoformat(i['start_time'][:-1]).replace(tzinfo=pytz.utc) # we need to strip 'Z' before parsing
			start_time=d.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%d-%m-%Y %I:%M %p')
			final_contest_list.append({'Name':i['name'], 'Site':i['site'], 'Time':start_time, 'Link':i['url']})
	#print(json.dumps(final_contest_list, indent=1))
	for i in final_contest_list:
		for k,v in i.items():
			print(f"{k}: {v}")
			print(' ')

		


else:
	print('Something went wrong!')


