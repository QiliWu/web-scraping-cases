import requests
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
r = requests.get('https://www.lagou.com/jobs/4376797.html', headers=headers)
text = r.text
url = r.url