# Python program to generate WordCloud

# importing all necessary modules
from wordcloud import WordCloud
import matplotlib.pyplot as plt


#create fucntion for printing wordcloud
def print_wordcloud(text):
	wordcloud = WordCloud().generate(text)

	# plot the WordCloud image
	plt.figure(figsize = (10, 5), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()
