import time, praw, csv, os

SUBREDDIT_FILE_NAME = "/Data/popular_subreddits.txt"
DATA_FILE_NAME = "/Data/subreddit_activity_data.csv"
USER_STRING = "/u/cogware reddit subscriber counter"
DOWNLOAD_PERIOD = 16 # download every 300 secs or 5 mins

class SubredditActivityDownloader:
	# Uses a list of 100 popular subreddits from popular_subreddits.txt
	# Every 5 mins, it queries Reddit to get active user count from each subreddit
	# Records this info in a file "activity_data.csv"
	# Time is an integer representation of UTC
	def __init__(self):
		r = praw.Reddit(user_agent = USER_STRING)

		# Get the subreddits
		with open(SUBREDDIT_FILE_NAME, "r") as f:
			subreddit_names = f.readlines()

		subreddit_names = [n.strip() for n in subreddit_names]

		self.subreddits = [r.get_subreddit(n) for n in subreddit_names]
		header_strings = ["time"] + subreddit_names

		# Load the data
		try:
			with open(DATA_FILE_NAME, 'rb') as f:
				reader = csv.reader(f)
				self.data = [row for row in reader]
				data_headers = self.data[0]
				print data_headers
				print self.data
				assert data_headers == header_strings

		except IOError:
			print "No data found"
			self.data = [header_strings]

		except AssertionError as e:
			print "Headers did not match expected! Indicates data file must have had different spec"
			raise e 

		# Start the data download cycle - this loops ad infinitum while prog runs
		self.download_time = 0
		self.data_cycles = 0

		while True:
			self.downloadData()
			self.saveData()


	def downloadData(self):
		if time.time() - self.download_time < DOWNLOAD_PERIOD:
			time.wait(self.download_time + DOWNLOAD_PERIOD - time.time())
		elif self.download_time != 0:
			print "Warning: Downloads took longer than expected:"
			print "Time since last download: {0}".format(time.time() - self.download_time)
		self.download_time = time.time()

		newdata = [int(self.download_time)] + [sr.accounts_active for sr in self.subreddits]

		self.data.append(newdata)
		self.data_cycles += 1
		print self.data_cycles

	def saveData(self):
		with open(DATA_FILE_NAME+"_temp", "wb") as f:
			writer = csv.writer(f)
			print self.data
			writer.writerows(self.data)
		os.rename(DATA_FILE_NAME + "_temp", DATA_FILE_NAME) 

def main():
	SubredditActivityDownloader()

if __name__ == '__main__':
	main()
