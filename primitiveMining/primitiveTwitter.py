#Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
#Proceedings of the ACM SIGKDD International Conference on Knowledge 
#Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, 
#Washington, USA, 

#Bing Liu, Minqing Hu and Junsheng Cheng. "Opinion Observer: Analyzing 
#and Comparing Opinions on the Web." Proceedings of the 14th 
#International World Wide Web conference (WWW-2005), May 10-14, 
#2005, Chiba, Japan.

from os import path
import twitter
from wordcloud import WordCloud

#Authentication for Twitter API
OAUTH_TOKEN = 'xxxx'
OAUTH_SECRET = 'xxxx'
CONSUMER_KEY = 'xxxx'
CONSUMER_SECRET = 'xxxx'

def binarySearch(alist,item):
	first = 0
	last = len(alist)-1
	found = False

	while first <= last and not found:
		midpoint = (first + last)
		if alist[midpoint] == item:
			found = True
			return found
		else:
			if item < alist[midpoint]:
				last = midpoint-1
			else:
				first = midpoint+1
	return found


def TwitterSearch(searchWord):
	try:
		# Create API object for calls
		twitterApi = twitter.Api(
		CONSUMER_KEY, CONSUMER_SECRET,
		OAUTH_TOKEN,OAUTH_SECRET)

		# Test results file
		# Make a search call to the API
		search = twitterApi.GetSearch(term=searchWord, lang='en', result_type='recent', count=100, max_id='')
		search += twitterApi.GetSearch(term=searchWord, lang='en', result_type='popular', count=100, max_id='')
		tweets = ""

		for t in search:
			# print t.user.screen_name + ' (' + t.created_at + ')'
			# Combining the tweets
			tweets += t.text.encode('utf-8')
			# Writing to a textfile for later API use
		# Split tweets by word
		tweetByWord = tweets.split()

		return tweetByWord

	except Exception as e:
		print e


def rateWordList(wordList):
	rating = 0
	posWords = open('positive-words.txt').read().splitlines()
	negWords = open('negative-words.txt').read().splitlines()
	f = open('results.txt','w')
	# Parse words
	for index in wordList:
		# Set everything to lowercase to correctly binary search
		index = index.lower()
		# Make sure the word is not a link
		if 'http' or 'RT' or 'rt' not in index:
			# Test results file
			# Remove non-alphabetic characters
			f.write(index + '\n')
			index = ''.join(ch for ch in index if ch.isalpha())
			# Binary searching to find words, very basic and primitive mass-sentiment analysis
			if binarySearch(posWords,index):
				rating+=1
			if binarySearch(negWords,index):
				rating-=1
		else:
			wordList.remove(index)
			print "Removed"
	f.close()
	return rating


def generateCloud():
	d = path.dirname(__file__)
	text = open(path.join(d,'results.txt')).read()

	wordcloud = WordCloud().generate(text)
	# Display the generated image:
	import matplotlib.pyplot as plt
	plt.imshow(wordcloud)
	plt.axis("off")

	# take relative word frequencies into account, lower max_font_size
	wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

while(True):
	searchTerm = raw_input("Search term: ")
	print rateWordList(TwitterSearch(searchTerm))
#	generateCloud()
