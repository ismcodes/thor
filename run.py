from flask import Flask, request, redirect
import os, twilio.twiml, praw
"""stuff"""
app = Flask(__name__)
r=praw.Reddit('reddit sms parser (j12coder)')
def check_subreddit(body):
	if len(body.split(" "))<2:
		return 'Sorry, it seems like you didn\'t type the message right. Here\'s an example: LearnPython 2'
	subreddit=body.split(" ")[0]
	num=body.split(" ")[1]
	try:
		num=int(num)
	except ValueError:
		return 'Sorry, looks like you didn\'t supply a number after the subreddit name.'
	if num>5:
		return 'Hold on there, partner. That\'s a lot of data! Try keeping it down to no more than 5 posts at a time.'
	if subreddit=="random":
		return get_posts(r.get_subreddit(subreddit),num)
	subs=r.search_reddit_names(subreddit)
	if len(subs)>0:
		for sub in subs:
			if sub.display_name.lower()==subreddit:
				return get_posts(sub,num)
		return 'Sorry, looks like I couldn\'t find that subreddit. Did you maybe mean reddit.com/r/%s?'%subs[0].display_name
	else:
		return 'Sorry, no subreddit found by that name.'

def get_posts(sub,num):
	#actual subreddit object
	sumstr="Hot posts on reddit.com/r/%s:\n\n"%sub.display_name
	new_posts=sub.get_hot(limit=num)
	for p in new_posts:
		if p.title>30:
			p.title=p.title[:28]+"..."
		sumstr+="%s\nby %s %s pts %d coms\n"%(p.title, p.author, p.ups, len(p.comments))
		sumstr+="%s\n\n"%str(p.short_link.replace("http://",""))
	return sumstr

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	msg=request.values.get('Body','- Wait a second... There\'s nothing in your message!?').lower()
	resp = twilio.twiml.Response()
	if msg=='wat' or msg=='what' or msg=='about' or msg=='help me' or msg=='hi' or msg=='hello':
		resp.message("This is Isaac's (bit.ly/1pI0K9B) SMS reddit parser, using Python, Twilio, PRAW, & Flask. \n Respond with the name of a subreddit and amount of results you want. Example: web_design 3")
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
