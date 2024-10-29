from wordcloud import WordCloud
import matplotlib.pyplot as plt

text = """
The organization.
Eliminating other work, focussing on the problem we chose to tackle.
Idea implementation.
Team collaboration and brainstorming.
Meeting new people and engaging with them.
Allows people to innovate and think outside the box for implementing their ideas.
Working with different people. New perspectives.
Teamwork, Excitement, Creative Ideas.
Networking and learning.
Everything.
Time management.
The mentors.
"""

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Plotting and saving the word cloud as an image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('static/images/surveywordcloud.png', bbox_inches='tight')
plt.show()
