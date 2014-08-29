import praw
from run import check_subreddit
r=praw.Reddit('thor testing file')
print(check_subreddit('learnpython 2'))
print(check_subreddit('learnpython post 2'))
print(check_subreddit('learnpython 0'))
print(check_subreddit('learnpython post 10'))
print(check_subreddit('learnpython 10'))
print('going into other loop')
for sub in ['basketball','nosleep','fifthworldproblems','funny','science','web_design']:
	print(check_subreddit('%s 1'%sub))
print('Done')