import praw,requests
from run import check_subreddit, hello_monkey
r=praw.Reddit('thor testing file')
for sub in ['learnpython','drums','nosleep','fifthworldproblems','funny','science','web_design']:
	print(check_subreddit('%s 1'%sub))
	print(check_subreddit('%s post 1'%sub))
print('checking error cases')
print(check_subreddit('learnpython pos 2'))
print(check_subreddit('learnpython post a'))
print(check_subreddit('learnpython'))
print(check_subreddit('learnpython 0'))
print(check_subreddit('learnpython post 10'))
print(check_subreddit('notactualsubredditnamejustforerror 4'))
print(check_subreddit('learnpytho 1'))
print('checking twilio cases')
print(hello_monkey('wat'))
print(hello_monkey('thanks'))
print(hello_monkey('this rocks'))
print(hello_monkey('keeping it alive!'))
print(hello_monkey('hello 1'))

print('Done')