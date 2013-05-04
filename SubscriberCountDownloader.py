import time, praw, csv, os

SUBREDDIT_FILE_NAME = "popular_subreddits.txt"
DATA_FILE_NAME = "subreddit_activity_data.csv"
USER_STRING = "/u/cogware reddit subscriber counter"
DOWNLOAD_PERIOD = 300 # download every 300 secs or 5 mins

	# Uses a list of 100 popular subreddits from popular_subreddits.txt
	# Every 5 mins, it queries Reddit to get active user count from each subreddit
	# Records this info in a file "activity_data.csv"
	# Time is an integer representation of UTC
r = praw.Reddit(user_agent = USER_STRING)

# Get the subreddits
with open(SUBREDDIT_FILE_NAME, "r") as f:
	subreddit_names = f.readlines()

subreddit_names = [n.strip() for n in names]

subreddits = [r.get_subreddit(n) for n in subreddit_names]
header_strings = ["time"] ++ subreddit_names

# Load the data
try:
	with open(DATA_FILE_NAME, 'rb') as f:
		reader = csv.reader(f)
		data_headers = reader.next()
		data = [row for row in reader]
		assert data_headers == header_strings

except IOError:
	print "No data found"
	data = [header_strings]

except AssertionError as e:
	print "Headers did not match expected! Indicates data file must have had different spec"
	raise e 

# Start the data download cycle - this loops ad infinitum while prog runs
download_time = 0
data_cycles = 0

while True:
	downloadData()
	saveData()

def downloadData():
	if time.time() - download_time < DOWNLOAD_PERIOD:
		wait(download_time + DOWNLOAD_PERIOD - time.time())
	else:
		print "Warning: Downloads took longer than expected:"
		print "Time since last download: {0}".format(time.time() - download_time)
	download_time = time.time()

	newdata = [int(download_time)] ++ [sr.accounts_active for sr in subreddits]

	data.append(newdata)
	data_cycles += 1
	print data_cycles

def saveData():
	with open(DATA_FILE_NAME+"_temp", "rb") as f:
		writer = csv.writer(f)
		writer.writerows(data)
	os.rename(DATA_FILE_NAME + "_temp", DATA_FILE_NAME) 