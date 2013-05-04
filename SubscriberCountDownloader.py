import time, praw, csv

SUBREDDIT_FILE_NAME = "popular_subreddits.txt"
DATA_FILE_NAME = "subreddit_activity_data.csv"
USER_STRING = "/u/cogware reddit subscriber counter"

class Subreddit_stat_collector:
	# Uses a list of 100 popular subreddits from popular_subreddits.txt
	# Every 5 mins, it queries Reddit to get active user count from each subreddit
	# Records this info in a file "activity_data.csv"
	# Time is an integer representation of UTC
	def __init__():
		self.r = praw.Reddit(user_agent = USER_STRING)

		with open(SUBREDDIT_FILE_NAME, "r") as f:
			subreddit_names = f.readlines()

		self.subreddits = [r.get_subreddit(n) for n in subreddit_names]
		self.header_strings = "time," ++ ",".join(subreddit_names)

		try:
			with open(DATA_FILE_NAME, 'rb') as f:
				reader = csv.reader(f)
				data_headers = reader.next()
				self.data = [row for row in reader]
				assert data_headers == self.header_strings

		except IOError:
			print("No data found")
			self.data = []

	def get_active_users(subreddit):


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

