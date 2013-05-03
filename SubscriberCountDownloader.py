import time, praw


class subreddit_stat_collector:
	def __init__(fname=popular_subreddits.txt):
		user_string = "/u/cogware reddit subscriber counter"
		self.r = praw.Reddit(user_agent = user_string)

		with open(fname) as f:
			subreddit_names = f.readlines()
		self.subreddits = [r.get_subreddit(n) for n in subreddit_names]
		


def jsonFromURL(url):
	downloadedString = urllib2.urlopen(url).read()
	data = json.loads(downloadedString)
	return data

def downloadSubreddit(subredditName):
	# String -> {}
	url = "http://www.reddit.com/r/" + subredditName + "/about.json"
	return jsonFromURL(url)

def subredditCounts(subredditName):
	json = downloadSubreddit(subredditName)
	data = json["data"]
	nActive = data["accounts_active"]
	nSubscribers = data["subscribers"]
	return (nActive, nSubscribers)

