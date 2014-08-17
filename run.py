from flask import Flask, request, redirect
import os, twilio.twiml, praw
app = Flask(__name__)
r=praw.Reddit('reddit sms parser (j12coder)')
def check_subreddit(body):
	sp=body.split(" ")
	if len(sp)<2:
		return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython 2'	
	if len(sp)==2:
		subreddit=sp[0]
		num=sp[1]
		try:
			num=int(num)
		except ValueError:
			return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython 2'
		if num>3:
			return 'Hold on there, partner. That\'s a lot of data! Try keeping it down to no more than 3 posts at a time.'
		if subreddit=="random":
			return get_posts(r.get_subreddit(subreddit),num)
		subs=r.search_reddit_names(subreddit)
		if len(subs)>0:
			for sub in subs:
				if sub.display_name.lower()==subreddit:
					return get_posts(sub,num)
			return 'Sorry, looks like I couldn\'t find that subreddit. Did you maybe mean reddit.com/r/%s? Or, the sub could be inactive. Maybe it moved to a different name?'%subs[0].display_name
		else:
			return 'Sorry, no subreddit found by that name. The sub could be inactive, maybe it migarted to a different name?'
	# else:
	# 	subreddit=sp[0]
	# 	post=sp[1]
	# 	num=sp[2]
	# 	try:
	# 		num=int(num)
	# 	except ValueError:
	# 		return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython 2'
	# 	if post !='post':
	# 		return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython 2'
	# 	if num>3:
	# 		return 'Uh oh. This could jam up the system; how about limiting it to the 3rd post?'
	# 	else if num<=0:
	# 		return 'Well, here are the 0 results you wanted!'
	# 	if subreddit=="random":
	# 		return get_post(r.get_subreddit(subreddit),num)
	# 	subs=r.search_reddit_names(subreddit)
	# 	if len(subs)>0:
	# 		for sub in subs:
	# 			if sub.display_name.lower()==subreddit:
	# 				return get_post(sub,num)
	# 		return 'Sorry, looks like I couldn\'t find that subreddit. Did you maybe mean reddit.com/r/%s? Or, the sub could be inactive. Maybe it moved to a different name?'%subs[0].display_name
	# 	else:
	# 		return 'Sorry, no subreddit found by that name. The sub could be inactive, maybe it migarted to a different name?'

def safe(s):
	return str(s.encode("ascii", errors='ignore'))[2:-1]
def get_post(sub,num):
	sumstr=""
	p=list(sub.get_hot(limit=num))[-1]
	sumstr+="%s\nby %s %s pts %d coms\n\n%s"%(safe(p.title), safe(p.author), p.ups, len(p.comments),safe(p.selftext))
	sumstr+="%s\n\n"%str(p.short_link.replace("http://",""))
	return sumstr
def get_posts(sub,num):
	#actual subreddit object
	sumstr="Hot posts on reddit.com/r/%s:\n\n"%sub.display_name
	new_posts=sub.get_hot(limit=num)
	for p in new_posts:
		if p.title>45:
			p.title=p.title[:43]+"..."
		sumstr+="%s\nby %s %s pts %d coms\n"%(safe(p.title), p.author, p.ups, len(p.comments))
		sumstr+="%s\n\n"%str(p.short_link.replace("http://",""))
	return sumstr

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	msg=request.values.get('Body','- Wait a second... There\'s nothing in your message!?').lower()
	resp = twilio.twiml.Response()
	if msg=='wat' or msg=='what' or msg=='about' or msg=='help me' or msg=='hi' or msg=='hello':
		resp.message("This is Isaac's (bit.ly/1pI0K9B) SMS Reddit parser application. \n Respond with the name of a subreddit and amount of results you want. Example: web_design 3 . put 'post' before the number to only get back the hot post with that ranking.")
	elif msg=="thanks" or msg=="thx" or msg=="thanx":
		resp.message("No problem! Let me know your opinion at hi@isaacmoldofsky.com!")
	elif msg=="this rocks" or msg=="this is great" or msg=="great":
		resp.message("Thanks! Let me know your opinion at hi@isaacmoldofsky.com!")
	else:
		resp.message(check_subreddit(msg))
	return str(resp)
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
