from flask import Flask, request
""", redirect"""
import os, twilio.twiml, praw, random
app = Flask(__name__)
r=praw.Reddit('reddit sms parser (j12coder) %d'%random.randint(1,100000))
def check_subreddit(body):
	sp=body.split(" ")
	if len(sp)<2:
		return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython 2'	
	elif len(sp)==2:
		return fetch_stuff(sp[0],sp[1],'posts')
	else:
		if sp[1]=="post":
			return fetch_stuff(sp[0],sp[2],'post')
		else:
			return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython post 2'
	
def fetch_stuff(try_name,num,ttype):
	try:
		num=int(num)
	except ValueError:
		return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython post 2'
	if num>5:
		return 'Uh oh. This could jam up the system; how about limiting it to the 5th post?'
	elif num<=0:
		return 'Well, here are the 0 results you wanted!'
	subred=r.get_subreddit(try_name)
	res=list(subred.get_hot(limit=num))
	if len(res)==num:
		if ttype=='posts':
			return format_posts(res)
		else:
			return format_post(res[-1])
	else:
		if len(res)!=0:
			return "There are not %d posts in that subreddit."%num
		namez=list(r.search_reddit_names(try_name))
		if len(namez)>0:
			return 'Sorry, looks like I couldn\'t find that subreddit. Did you maybe mean reddit.com/r/%s?'%namez[0].display_name
		else:
			return 'Sorry, no subreddit found by that name.'		
def safe(s):
	return str(s.encode("ascii", errors='ignore'))
def format_post(p):
	sumstr=""
	if p.is_self:
		sumstr+="%s\nby %s %s pts %d coms\n\n%s\n"%(safe(p.title), p.author, p.ups, len(p.comments),safe(p.selftext))
	else:
		sumstr+="%s\nby %s %s pts %d coms\n"%(safe(p.title), p.author, p.ups, len(p.comments))	
	sumstr+="\n%s\n\n"%str(p.short_link.replace("http://",""))
	return sumstr
def format_posts(new_posts):
	sumstr="Hot posts on reddit.com/r/%s:\n\n"%new_posts[0].subreddit.display_name
	for p in new_posts:
		p.title=safe(p.title)
		if len(p.title)>45:
			p.title=p.title[:43]+"..."
		sumstr+="%s\nby %s %s pts %d coms\n"%(p.title, p.author, p.ups, len(p.comments))
		sumstr+="%s\n\n"%str(p.short_link.replace("http://",""))
	return sumstr

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	msg=request.values.get('Body','Empty message?').lower()
	resp = twilio.twiml.Response()
	if msg=='wat' or msg=='what' or msg=='about' or msg=='help me' or msg=='hi' or msg=='hello':
		resp.message("bit.ly/1pI0K9B SMS Reddit parser. \n Txt subreddit name and # of results you want. Ex: science 3 . Put post before # to get back specific post Ex: ruby post 2")
	elif msg=="thanks" or msg=="thx" or msg=="thanx":
		resp.message("No problem! Let me know your opinion at hi@isaacmoldofsky.com!")
	elif msg=="this rocks" or msg=="this is great" or msg=="great":
		resp.message("Thanks! Let me know your opinion at hi@isaacmoldofsky.com!")
	elif msg=="keeping it alive!":
		resp.message('ok')
	else:
		resp.message(check_subreddit(msg))
	return str(resp)
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
